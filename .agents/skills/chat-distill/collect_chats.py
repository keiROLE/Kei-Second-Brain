# -*- coding: utf-8 -*-
"""chat-distill collection script.

Scan Claude Code / Codex / DoubaoWork conversation logs and write a
session list for the last N days to
0_Inbox/chat-distill/_raw/YYYY-WW-session-list.md (used by Step 1 triage).

Usage:
  python collect_chats.py                 # last 7 days
  python collect_chats.py --days 30      # last 30 days
  python collect_chats.py --agent codex   # one agent only (claude-code/codex/doubao)
  python collect_chats.py --all           # all time
"""
import argparse, glob, io, json, os, re, sys
from datetime import datetime, timedelta
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Vault root = repo root (this file lives at .agents/skills/chat-distill/collect_chats.py)
VAULT = Path(__file__).resolve().parents[3]
RAW_DIR = VAULT / '0_Inbox' / 'chat-distill' / '_raw'

_home = os.path.expanduser('~')
SOURCES = {
    'claude-code': os.path.join(_home, '.claude', 'projects', '*', '*.jsonl'),
    'codex': os.path.join(_home, '.codex', 'sessions', '**', 'rollout-*.jsonl'),
    'doubao': os.path.join(_home, 'AppData', 'Local', 'DoubaoWork', 'User Data', 'Default',
                           '.doubaowork', 'agent_mode', 'workspace', '.sessions', '*',
                           'agents', '*', 'system', 'trajectory.jsonl'),
}

ROLE_KEYWORDS = ('user', 'assistant', 'human', 'ai')

# System-injected / instruction content — not a real user question (skip when picking the topic)
NOISE_MARKERS = (
    '<system-reminder>', '<agents_md', 'AGENTS.md instructions', '<INSTRUCTIONS>',
    '<usage>', '<retained_skills>', '<current-state>', '<subagent-result>',
    '<usage_guide>', 'skill://',
    'This is the AG', '# AGENTS.md',
)


def is_noise(text):
    t = text.strip()
    if not t or len(t) < 3:
        return True
    for m in NOISE_MARKERS:
        if t.startswith(m) or m in t[:120]:
            return True
    return False


def extract_text(obj):
    """Recursively extract readable text (only strings; caller filters tool-result/code noise)."""
    if isinstance(obj, str):
        return obj
    if isinstance(obj, dict):
        for k in ('text', 'content', 'message', 'input'):
            if k in obj:
                r = extract_text(obj[k])
                if r:
                    return r
        for v in obj.values():
            r = extract_text(v)
            if r:
                return r
    if isinstance(obj, list):
        parts = [extract_text(x) for x in obj]
        joined = '\n'.join(p for p in parts if p)
        return joined
    return ''


def safe_lines(path):
    """Read a jsonl line by line, tolerating bad / non-JSON lines."""
    try:
        with open(path, encoding='utf-8') as f:
            for ln in f:
                ln = ln.strip()
                if not ln:
                    continue
                try:
                    yield json.loads(ln)
                except Exception:
                    continue
    except Exception:
        return


def ts_to_dt(ts):
    if isinstance(ts, (int, float)):
        return datetime.fromtimestamp(ts)
    s = str(ts)
    s = s.replace('Z', '+00:00')
    try:
        dt = datetime.fromisoformat(s)
    except Exception:
        return None
    if dt.tzinfo is not None:
        dt = dt.astimezone().replace(tzinfo=None)  # convert to local naive for cutoff comparison
    return dt


def parse_session(path, agent):
    """Return (min_dt, max_dt, first_user_msg, msg_count)."""
    min_dt, max_dt = None, None
    first_user = ''
    msg_count = 0
    for d in safe_lines(path):
        role = None
        text = ''
        ts = None
        if agent == 'claude-code':
            role = d.get('type')
            text = extract_text(d.get('content', ''))
            ts = d.get('timestamp')
        elif agent == 'codex':
            if d.get('type') == 'response_item':
                p = d.get('payload', {})
                role = p.get('role')
                text = extract_text(p.get('content', ''))
                ts = d.get('timestamp')
            elif d.get('type') == 'event_msg':
                role = None
                text = extract_text(d.get('payload', {}).get('message', ''))
                ts = d.get('timestamp')
        elif agent == 'doubao':
            role = d.get('role')
            text = extract_text(d.get('content', ''))
        if role and any(k in str(role).lower() for k in ROLE_KEYWORDS):
            msg_count += 1
            if not first_user and 'user' in str(role).lower():
                t = text.strip()
                if len(t) >= 3 and not is_noise(t):
                    first_user = t
        elif text and text.strip():
            msg_count += 1
        dt = ts_to_dt(ts)
        if dt:
            if min_dt is None or dt < min_dt:
                min_dt = dt
            if max_dt is None or dt > max_dt:
                max_dt = dt
    if min_dt is None:
        try:
            min_dt = datetime.fromtimestamp(os.path.getmtime(path))
        except Exception:
            min_dt = datetime.now()
    if max_dt is None:
        max_dt = min_dt
    topic = re.sub(r'\s+', ' ', first_user).strip()[:80] if first_user else '(no user message)'
    return min_dt, max_dt, topic, msg_count


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--days', type=int, default=7)
    ap.add_argument('--agent', choices=list(SOURCES) + ['all'], default='all')
    ap.add_argument('--all', action='store_true', help='ignore time filter, scan everything')
    args = ap.parse_args()

    cutoff = None
    if not args.all:
        cutoff = datetime.now() - timedelta(days=args.days)

    rows = []
    for agent, pattern in SOURCES.items():
        if args.agent != 'all' and args.agent != agent:
            continue
        for path in glob.glob(pattern, recursive=True):
            try:
                size = os.path.getsize(path)
            except Exception:
                continue
            min_dt, max_dt, topic, n = parse_session(path, agent)
            if cutoff and max_dt < cutoff:
                continue
            rows.append({
                'agent': agent,
                'path': path,
                'min': min_dt,
                'max': max_dt,
                'size': size,
                'n': n,
                'topic': topic,
            })

    rows.sort(key=lambda r: r['max'], reverse=True)
    now = datetime.now()
    iso_week = now.isocalendar()
    out_name = f'{now.year}-W{iso_week.week:02d}-session-list.md'
    os.makedirs(RAW_DIR, exist_ok=True)
    out_path = os.path.join(RAW_DIR, out_name)

    lines = [
        f'# AI Session List (last {args.days} days, ISO week {now.year}-W{iso_week.week:02d})',
        '',
        f'> Scanned: {now:%Y-%m-%d %H:%M} ｜ Agent: {"all" if args.agent == "all" else args.agent} ｜ Sessions found: {len(rows)}',
        '',
        '| # | agent | file | last time | msgs | size | topic (first user message) |',
        '|---|-------|------|-----------|------|------|-----------------------------|',
    ]
    for i, r in enumerate(rows, 1):
        rel = os.path.basename(r['path'])
        lines.append(
            f"| {i} | {r['agent']} | {rel} | {r['max']:%m-%d %H:%M} | {r['n']} | {r['size']//1024}KB | {r['topic']} |"
        )
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

    print(f'Sessions found: {len(rows)}')
    for r in rows[:15]:
        print(f"  [{r['agent']}] {r['max']:%m-%d} | {r['n']} msgs | {r['topic'][:40]}")
    print(f'List written to: {out_path}')


if __name__ == '__main__':
    main()

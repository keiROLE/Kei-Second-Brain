# -*- coding: utf-8 -*-
"""
review_status.py — wr-1 companion (deterministic part)
  List which diaries are missing `weekly_reviewed` per week; batch-mark after review.

Usage:
  python review_status.py status               # per-week review status
  python review_status.py mark 2026-09-14 ...  # add weekly_reviewed (never overwrite existing)

Path resolution: this script lives at <vault>/.agents/skills/wr-1/review_status.py
                 so the vault root is 3 parents up from this file.
"""
import sys, re, os, io, datetime
from pathlib import Path

VAULT = Path(__file__).resolve().parents[3]
DIARY = VAULT / "0_Inbox" / "diary"


def read_text(p):
    with io.open(p, "r", encoding="utf-8-sig") as f:
        return f.read()


def get_field(text, key):
    m = re.search(r"^" + re.escape(key) + r"\s*:\s*(\S+)", text, re.M)
    return m.group(1).strip().strip('"') if m else None


def monday_of(d):
    return d - datetime.timedelta(days=d.weekday())


def cmd_status():
    weeks = {}
    for f in os.listdir(DIARY):
        if not f.endswith(".md"):
            continue
        try:
            d = datetime.date.fromisoformat(f[:-3])
        except ValueError:
            continue
        wr = get_field(read_text(DIARY / f), "weekly_reviewed")
        weeks.setdefault(monday_of(d).isoformat(), []).append((f[:-3], wr))
    for wk in sorted(weeks):
        days = sorted(weeks[wk])
        missing = [x for x, w in days if not w]
        status = "all marked" if not missing else f"missing {len(missing)}: {', '.join(missing)}"
        print(f"  week starting {wk} ({len(days)} days): {status}")


def cmd_mark(days):
    for day in days:
        p = DIARY / (day + ".md")
        if not p.exists():
            print(f"  not found: {day}")
            continue
        txt = read_text(p)
        if get_field(txt, "weekly_reviewed"):
            print(f"  already marked, skipped: {day}")
            continue
        m = re.match(r"^(---\s*\n)(.*?)(\n---\s*\n)", txt, re.S)
        if not m:
            print(f"  no frontmatter, skipped: {day}")
            continue
        body = m.group(2).rstrip("\n") + f"\nweekly_reviewed: {day}"
        new = m.group(1) + body + m.group(3) + txt[m.end():]
        with io.open(p, "w", encoding="utf-8", newline="") as f:
            f.write(new)
        print(f"  marked: {day}")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "mark":
        cmd_mark(sys.argv[2:])
    else:
        cmd_status()

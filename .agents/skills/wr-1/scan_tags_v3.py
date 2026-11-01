# -*- coding: utf-8 -*-
"""
scan_tags_v3.py — report tags with bad characters on either side.

Like scan_tags_v2.py but checks both the character before `#` and
the character after the tag name. Flags when the tag is glued to
non-whitespace on either side (or both).

Path: this script lives at <vault>/.agents/skills/wr-1/<script>.py
      so the vault root is 3 parents up from this file.
"""
import re
import os
from collections import defaultdict
from pathlib import Path

VAULT = Path(__file__).resolve().parents[3]

problems = []

SKIP_DIRS = ["archive", ".agents", ".git", "node_modules", ".claude"]

for root, dirs, files in os.walk(VAULT):
    if any(s in root for s in SKIP_DIRS):
        continue

    for fname in files:
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(root, fname)
        relpath = os.path.relpath(fpath, VAULT)

        try:
            with open(fpath, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception:
            continue

        in_frontmatter = False
        in_codeblock = False

        for lineno, line in enumerate(lines, 1):
            if lineno == 1 and line.strip() == "---":
                in_frontmatter = True
                continue
            if in_frontmatter and line.strip() == "---":
                in_frontmatter = False
                continue
            if in_frontmatter:
                continue

            stripped = line.strip()
            if stripped.startswith("```"):
                in_codeblock = not in_codeblock
                continue
            if in_codeblock:
                continue

            # strip inline code
            line_clean = re.sub(r"`[^`]*`", "", line)
            # strip link URLs
            line_clean = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"[\1]", line_clean)

            # find every #xxx candidate regardless of what precedes it
            all_hash = re.finditer(r"#([\w\u4e00-\u9fff/-]+)", line_clean)

            for m in all_hash:
                tag_name = m.group(1)
                full_tag = "#" + tag_name
                start = m.start()
                end = m.end()

                prev_char = line_clean[start - 1] if start > 0 else "\n"
                prev_ok = prev_char in (" ", "\t", "\n", "") or start == 0

                next_char = line_clean[end] if end < len(line_clean) else "\n"
                ok_next = (" ", "\t", "\n", "", "，", "。", "：", "；", "、",
                           "）", "】", "」", "』", "!", "?", ".", ",", ":", ";",
                           ")", "]", "}", "#", "/", "|", "-", "（", "【", "*")
                next_ok = next_char in ok_next

                issue = None
                if not prev_ok and not next_ok:
                    issue = f"bad both sides: prev='{prev_char}' next='{next_char}'"
                elif not prev_ok:
                    issue = f"preceded by '{prev_char}'"
                elif not next_ok:
                    issue = f"followed by '{next_char}'"

                if issue:
                    problems.append((relpath, lineno, full_tag, issue, line.strip()[:100]))

print(f"Found {len(problems)} tag format issue(s) (both-sides check)")
print()

by_file = defaultdict(list)
for p in problems:
    by_file[p[0]].append(p)

for fpath, items in sorted(by_file.items(), key=lambda x: -len(x[1])):
    print(f"=== {fpath} ({len(items)} issue(s)) ===")
    for item in items[:5]:
        print(f"  line {item[1]}: {item[2]} - {item[3]}")
        print(f"    {item[4]}")
    if len(items) > 5:
        print(f"  ... {len(items) - 5} more")
    print()

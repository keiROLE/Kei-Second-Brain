# -*- coding: utf-8 -*-
"""
scan_tags_v2.py — report tags immediately followed by non-whitespace.

Like scan_tags.py but only flags the trailing-glue issue (a tag
whose next character is not whitespace, end-of-line, or common
punctuation). Strips inline code and link URLs before checking.

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

            # strip inline code `xxx`
            line_no_inline = re.sub(r"`[^`]*`", "", line)
            # strip link URLs, keep [text]
            line_no_inline = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"[\1]", line_no_inline)

            tag_pattern = re.compile(r"(?:^|\s)#([\w\u4e00-\u9fff/-]+)")

            for m in tag_pattern.finditer(line_no_inline):
                tag_name = m.group(1)
                full_tag = "#" + tag_name
                end_pos = m.end(1)

                next_char = line_no_inline[end_pos] if end_pos < len(line_no_inline) else "\n"

                ok_next = (" ", "\t", "\n", "", "，", "。", "：", "；", "、",
                           "）", "】", "」", "』", "!", "?", ".", ",", ":", ";",
                           ")", "]", "}", "#", "/", "|", "-", "（", "【")

                if next_char not in ok_next:
                    problems.append((relpath, lineno, full_tag,
                                     f"followed by '{next_char}'",
                                     line.strip()[:100]))

print(f"Found {len(problems)} tag format issue(s)")
print()

by_file = defaultdict(list)
for p in problems:
    by_file[p[0]].append(p)

for fpath, items in sorted(by_file.items(), key=lambda x: -len(x[1])):
    print(f"=== {fpath} ({len(items)} issue(s)) ===")
    for item in items:
        print(f"  line {item[1]}: {item[2]} - {item[3]}")
        print(f"    {item[4]}")
    print()

# -*- coding: utf-8 -*-
"""
scan_tags.py — full-vault tag scan.

Lists every distinct tag Obsidian recognizes, flags weird ones
(6-digit hex colors, pure numbers, number-prefixed alphanumerics),
and reports tags glued to adjacent non-whitespace characters.

Path: this script lives at <vault>/.agents/skills/wr-1/<script>.py
      so the vault root is 3 parents up from this file.
"""
import re
import os
from collections import defaultdict
from pathlib import Path

VAULT = Path(__file__).resolve().parents[3]

# real Obsidian tag: preceded by line start or whitespace
tag_pattern = re.compile(r"(?:^|\s)#([\w\u4e00-\u9fff/-]+)")

problems = []
all_tags = set()

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
                content = f.read()
                lines = content.split("\n")
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

            for m in tag_pattern.finditer(line):
                tag_name = m.group(1)
                full_tag = "#" + tag_name
                end = m.end(1)

                all_tags.add(tag_name)

                next_char = line[end] if end < len(line) else "\n"

                if next_char not in (" ", "\t", "\n", "", "，", "。", "：", "；",
                                      "、", "）", "】", "」", "』", "!", "?", ".",
                                      ",", ":", ";", ")", "]", "}", "#", "/", "|", "-"):
                    problems.append((relpath, lineno, full_tag,
                                     f"followed by '{next_char}'",
                                     line.strip()[:80]))

# classify weird tags
color_tags = [t for t in all_tags if re.match(r"^[0-9a-fA-F]{6}$", t)]
digit_tags = [t for t in all_tags if re.match(r"^\d+$", t)]
digit_start_tags = [t for t in all_tags if re.match(r"^\d", t) and not re.match(r"^\d+$", t)]

print(f"Scan complete: {len(all_tags)} distinct tags found")
print()
print("=== Weird tag statistics ===")
print(f"Hex color values (6 hex digits): {len(color_tags)}")
for t in sorted(color_tags)[:15]:
    print(f"  #{t}")
if len(color_tags) > 15:
    print(f"  ... {len(color_tags) - 15} more")

print(f"\nPure number tags: {len(digit_tags)}")
for t in sorted(digit_tags)[:15]:
    print(f"  #{t}")

print(f"\nNumber-prefixed tags: {len(digit_start_tags)}")
for t in sorted(digit_start_tags)[:15]:
    print(f"  #{t}")

print(f"\n=== Tags glued to following text: {len(problems)} issue(s) ===")
by_file = defaultdict(list)
for p in problems:
    by_file[p[0]].append(p)

for fpath, items in sorted(by_file.items(), key=lambda x: -len(x[1]))[:20]:
    print(f"\n  {fpath}: {len(items)} issue(s)")
    for item in items[:3]:
        print(f"    line {item[1]}: {item[2]} - {item[3]}")
        print(f"      {item[4]}")
    if len(items) > 3:
        print(f"    ... {len(items) - 3} more")

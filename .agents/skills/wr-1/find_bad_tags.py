# -*- coding: utf-8 -*-
"""
find_bad_tags.py — find the "#tag):" pattern in vault notes.

Problem: a tag immediately followed by a closing paren and a colon,
e.g. `#tag）：content` or `#tag): content`. Obsidian swallows the
paren and colon into the tag name.

Path: this script lives at <vault>/.agents/skills/wr-1/<script>.py
      so the vault root is 3 parents up from this file.
"""
import re
import os
from collections import defaultdict
from pathlib import Path

VAULT = Path(__file__).resolve().parents[3]

# tag chars, then closing paren (Chinese or ASCII), then colon (Chinese or ASCII)
problem_pattern = re.compile(r"#([\w\u4e00-\u9fff/-]+)[）)][：:]")

problems = defaultdict(list)

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

            # strip inline code and wiki links
            line_clean = re.sub(r"`[^`]*`", "", line)
            line_clean = re.sub(r"\[\[[^\]]*\]\]", "", line_clean)

            for m in problem_pattern.finditer(line_clean):
                tag_name = m.group(1)
                full_match = m.group(0)
                problems[relpath].append((lineno, full_match, line.strip()[:100]))

total = sum(len(v) for v in problems.values())
print(f"Found {total} '#tag):' pattern issues")
print(f"across {len(problems)} files:")
print()

for fpath, items in sorted(problems.items(), key=lambda x: -len(x[1])):
    print(f"=== {fpath} ({len(items)} issues) ===")
    for lineno, match, content in items[:5]:
        print(f"  line {lineno}: {match}")
        print(f"    {content}")
    if len(items) > 5:
        print(f"  ... {len(items) - 5} more")
    print()

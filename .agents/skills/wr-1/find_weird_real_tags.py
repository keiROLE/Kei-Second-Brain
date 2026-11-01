# -*- coding: utf-8 -*-
"""
find_weird_real_tags.py — find "weird" tags that Obsidian actually recognizes.

A real tag starts at line start or after whitespace. This script flags
real tags that look like hex color values, pure numbers, or
number-prefixed alphanumeric strings.

Path: this script lives at <vault>/.agents/skills/wr-1/<script>.py
      so the vault root is 3 parents up from this file.
"""
import re
import os
from collections import defaultdict
from pathlib import Path

VAULT = Path(__file__).resolve().parents[3]

# real Obsidian tag: preceded by line start or whitespace
real_tag_pattern = re.compile(r"(?:^|\s)#([\w\u4e00-\u9fff/-]+)")

weird_tags = defaultdict(list)  # tag_name -> [(file, line, reason, content)]

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

            # strip [[links]] (the # inside is an anchor, not a tag)
            line_no_links = re.sub(r"\[\[[^\]]*\]\]", "", line)
            # strip inline code
            line_clean = re.sub(r"`[^`]*`", "", line_no_links)
            # strip URLs
            line_clean = re.sub(r"https?://\S+", "", line_clean)

            for m in real_tag_pattern.finditer(line_clean):
                tag_name = m.group(1)

                is_weird = False
                reason = ""

                # hex color: 6 hex digits
                if re.match(r"^[0-9a-fA-F]{6}$", tag_name):
                    is_weird = True
                    reason = "hex color value"
                # pure number
                elif re.match(r"^\d+$", tag_name):
                    is_weird = True
                    reason = "pure number"
                # number-started alphanumeric
                elif re.match(r"^\d", tag_name) and re.match(r"^[0-9a-zA-Z]+$", tag_name) and len(tag_name) >= 4:
                    is_weird = True
                    reason = "number-prefixed alphanumeric"

                if is_weird:
                    weird_tags[tag_name].append((relpath, lineno, reason, line.strip()[:100]))

print("=== Weird tags summary ===")
print(f"{len(weird_tags)} weird tags found:")
print()

for tag, locations in sorted(weird_tags.items()):
    reason = locations[0][2]
    print(f"#{tag} ({reason}) - {len(locations)} occurrence(s)")
    for loc in locations[:3]:
        print(f"  {loc[0]}:{loc[1]}")
        print(f"    {loc[3]}")
    if len(locations) > 3:
        print(f"  ... {len(locations) - 3} more")
    print()

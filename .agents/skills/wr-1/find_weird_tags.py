# -*- coding: utf-8 -*-
"""
find_weird_tags.py — search for a hardcoded list of known problematic tags.

Adjust the `weird_tags` list below to match tags you know are wrong
(e.g. hex color values accidentally used as tags, stray number tags).

Path: this script lives at <vault>/.agents/skills/wr-1/<script>.py
      so the vault root is 3 parents up from this file.
"""
import re
import os
from pathlib import Path

VAULT = Path(__file__).resolve().parents[3]

# Known problematic tags — adjust as needed.
weird_tags = ["#2584ff", "#1", "#17"]

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

            for tag in weird_tags:
                pattern = r"(?:^|\s)" + re.escape(tag) + r"(?=\s|$|，|。|：|；|、|）|】|」|』|!|\?|\.|,|:|;|\]|\}|#|/|\||-)"
                if re.search(pattern, line):
                    print(f"{relpath}:{lineno}: {tag}")
                    print(f"  {line.strip()[:100]}")
                    print()

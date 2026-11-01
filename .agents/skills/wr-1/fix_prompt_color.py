# -*- coding: utf-8 -*-
"""
fix_prompt_color.py — wrap 6-digit hex color values in backticks (stricter).

Variant of fix_color_values.py with stricter lookbehind/lookahead:
the color value must not be adjacent to word characters either.
Use this when the file contains prose where `#rrggbb` might be
embedded in a larger word.

Usage:
  python fix_prompt_color.py <file.md>

Path: this script lives at <vault>/.agents/skills/wr-1/<script>.py
      so the vault root is 3 parents up from this file.
"""
import re
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[3]

# match #RRGGBB not adjacent to backticks or word chars
color_pattern = re.compile(r"(?<![`\w])#([0-9a-fA-F]{6})(?![`\w])")

if len(sys.argv) < 2:
    print("Usage: python fix_prompt_color.py <file.md>")
    sys.exit(1)

fpath = Path(sys.argv[1])
if not fpath.is_absolute():
    fpath = VAULT / fpath

with open(fpath, "r", encoding="utf-8") as f:
    content = f.read()

matches = color_pattern.findall(content)
print(f"Found {len(matches)} color value(s) to wrap in backticks")

new_content = color_pattern.sub(r"`#\1`", content)

with open(fpath, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Done")

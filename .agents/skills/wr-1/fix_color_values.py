# -*- coding: utf-8 -*-
"""
fix_color_values.py — wrap 6-digit hex color values in backticks in a file.

Color values like `#2584ff` are mistaken by Obsidian for tags. This
script wraps every bare 6-digit hex color value in backticks
(e.g. `#2584ff` becomes `` `#2584ff` ``) so Obsidian treats it as code.

Usage:
  python fix_color_values.py <file.md>

Path: this script lives at <vault>/.agents/skills/wr-1/<script>.py
      so the vault root is 3 parents up from this file.
"""
import re
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[3]

# match #RRGGBB not already wrapped in backticks
color_pattern = re.compile(r"(?<![`])#([0-9a-fA-F]{6})(?![`])")

if len(sys.argv) < 2:
    print("Usage: python fix_color_values.py <file.md>")
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

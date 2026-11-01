# -*- coding: utf-8 -*-
"""
fix_backup_tags.py — rewrite tag placement in backup weekly-review files.

Converts lines of the form:
    - #type title (#tag1 #tag2): content
into:
    - #type #tag1 #tag2 title: content

so that classification tags sit right after the leading type tag
(space-separated) instead of being trapped inside parentheses.

Path: this script lives at <vault>/.agents/skills/wr-1/<script>.py
      so the vault root is 3 parents up from this file.
"""
import re
import os
from pathlib import Path

VAULT = Path(__file__).resolve().parents[3]

# Backup directory — adjust if your archive layout differs.
BACKUP_DIR = VAULT / "1_Wiki" / "archive" / "weekly-review-tag-fix-backup"

# - #type  title（#tag1 #tag2...）: content
# supports both Chinese and ASCII parens/colons
pattern = re.compile(
    r"^(-\s+#\w+)\s+(.+?)[（(](#[\w\s/-]+)[）)][：:](.*)$"
)

total_fixed = 0

if not BACKUP_DIR.is_dir():
    print(f"backup directory not found: {BACKUP_DIR}")
    raise SystemExit(0)

for fname in sorted(os.listdir(BACKUP_DIR)):
    if not fname.endswith(".md"):
        continue
    fpath = BACKUP_DIR / fname

    with open(fpath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    fixed_count = 0

    for line in lines:
        m = pattern.match(line.rstrip("\n"))
        if m:
            type_tag = m.group(1)
            title = m.group(2)
            tags = m.group(3)
            rest = m.group(4)
            new_line = f"{type_tag} {tags} {title}:{rest}\n"
            new_lines.append(new_line)
            fixed_count += 1
        else:
            new_lines.append(line)

    if fixed_count > 0:
        with open(fpath, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        total_fixed += fixed_count
        print(f"  {fname}: fixed {fixed_count} line(s)")

print(f"\nTotal fixed in backup directory: {total_fixed}")

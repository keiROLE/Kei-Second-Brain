# -*- coding: utf-8 -*-
"""
check_weekly_tags.py — check tag format issues in weekly-review files.

Problem patterns detected:
  1. Tags inside parentheses right after the title: title (#tag #tag):
  2. Tags with no space between them: #tag1#tag2
  3. Tag immediately glued to preceding text: text#tag
  4. Tag immediately glued to following text: #tagtext

Path: this script lives at <vault>/.agents/skills/wr-1/<script>.py
      so the vault root is 3 parents up from this file.
"""
import re
import os
from pathlib import Path

VAULT = Path(__file__).resolve().parents[3]
WEEKLY_DIR = VAULT / "0_Inbox" / "weekly-review"


def main():
    if not WEEKLY_DIR.is_dir():
        print(f"weekly-review directory not found: {WEEKLY_DIR}")
        return

    print("=== Weekly review tag format check ===")
    print()

    for fname in sorted(os.listdir(WEEKLY_DIR)):
        if not fname.endswith(".md"):
            continue
        fpath = WEEKLY_DIR / fname

        with open(fpath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        issues = []

        for lineno, line in enumerate(lines, 1):
            # skip frontmatter
            if lineno <= 10:
                continue

            # check 1: tags inside parentheses （#xxx #xxx） or (#xxx #xxx)
            if re.search(r"[（(]#\w+", line):
                issues.append((lineno, "tags inside parentheses", line.strip()[:80]))

            # check 2: no space between tags #xxx#xxx
            if re.search(r"#\w+#\w+", line):
                issues.append((lineno, "no space between tags", line.strip()[:80]))

            # check 3: tag glued to preceding non-space text
            for m in re.finditer(r"#([\w\u4e00-\u9fff/-]+)", line):
                start = m.start()
                prev_char = line[start - 1] if start > 0 else "\n"

                if prev_char not in (" ", "\t", "\n", "", "-", "*", "#", "|", ">",
                                      "（", "(", "：", ":", "；", ";", "，", ",",
                                      "。", ".", "、"):
                    # check if inside [[link]]
                    before = line[:start]
                    if before.count("[[") <= before.count("]]"):
                        issues.append((lineno, f"tag glued to preceding '{prev_char}'", line.strip()[:80]))
                        break  # report once per line

        if issues:
            print(f"--- {fname} ({len(issues)} issues) ---")
            for lineno, typ, content in issues[:5]:
                print(f"  line {lineno}: [{typ}] {content}")
            if len(issues) > 5:
                print(f"  ... {len(issues) - 5} more")
            print()


if __name__ == "__main__":
    main()

---
name: wr-1
description: Weekly review — compile the last complete week (Monday–Sunday) of 7 diary notes into a concise weekly review document in 0_Inbox/weekly-review/, and mark each diary frontmatter with weekly_reviewed. Also ships tag-hygiene scripts. Triggers on "/wr-1", "weekly review" or "last week review".
---

> This skill is part of the Kei-Second-Brain ecosystem. System overview is in `README.md`.

# wr-1 — Weekly Review

Compile the last complete week (Monday–Sunday) of 7 diary notes into a concise weekly review document. Raw diary notes only get a frontmatter marker appended — their body is never rewritten. Usually run on Monday morning.

## Trigger

User says "/wr-1", "weekly review", "last week review", or asks to compile the last week's diary notes.

## Before starting

> **Run the deterministic script first:**
> `python .agents/skills/wr-1/review_status.py` — lists, per week, which diaries already carry `weekly_reviewed` and which weeks are missing the marker. The LLM does not need to read frontmatter itself.
> After the review, batch-mark with: `python .agents/skills/wr-1/review_status.py mark <date...>` (existing markers are not overwritten).

1. Confirm "today" from the system's current date.
2. Default target: the last **completed** Monday–Sunday. If today is Monday, last week = today-7 .. today-1. If today is not Monday, still take the previous complete Monday–Sunday and tell the user the chosen range.
3. Check whether the 7 diary notes exist and whether they are already marked `weekly_reviewed`; skip marked ones and say so.

## Files to read

- Diary notes: `0_Inbox/diary/YYYY-MM-DD.md`, Monday–Sunday (7 notes).
- Format reference: `2_Schema/templates/weekly-review-template.md`.
- Example: the most recent weekly review in `0_Inbox/weekly-review/`.

## Compile flow

1. Read all 7 diary notes; extract key events, thoughts, quotes, methods, inputs and unfinished tasks.
2. Merge by day into daily entries, keeping the diary's tag conventions (e.g. `#event`, `#thought`, `#quote`, `#method`, `#learn`, `#next`, `#question`, `#project` — adjust the list as needed). **Classification/category tags (e.g. `#concept`, `#domain`, `#theme`) go after the leading type tag on the same line, space-separated**, in the format `- #method #tag1 #tag2 title: content`. **Do not put classification tags inside parentheses right after the title** (e.g. `title (#concept #theme):`) — Obsidian will fail to parse the tags correctly.
3. Cross-week summary: key events, insights & reflections, unresolved questions.
4. Write the output, named `MMDD-last-week-review.md` (MMDD = the Monday of the reviewed week), into `0_Inbox/weekly-review/`.

## Output format

Frontmatter:

```yaml
---
title: "MMDD Last Week Review"
created: YYYY-MM-DD
tags:
  - weekly-review
  - inbox/raw
---
```

Body:

- `# MMDD Last Week Review (Mon YYYY-MM-DD ~ Sun YYYY-MM-DD)`
- `## Week Overview`: 3-5 lines on the week's main thread
- `## Monday MM-DD` ... `## Sunday MM-DD`: each section starts with the `[[YYYY-MM-DD]]` link, then bullet points
- `## Key Events`
- `## Insights & Reflection`
- `## Unresolved Questions`

## Update diary notes

Append `weekly_reviewed: YYYY-MM-DD` to each compiled diary's frontmatter — **use `review_status.py mark` for batch marking**, do not edit by hand. Only append the field; never rewrite the body; never overwrite an existing value.

## Tag hygiene scripts

Auxiliary scripts in this directory that scan the vault for malformed tags. All paths are derived from `Path(__file__).resolve().parents[3]` (the vault root).

| Script | Purpose |
|---|---|
| `review_status.py` | Per-week review status; batch-mark `weekly_reviewed`. |
| `check_weekly_tags.py` | Check tag format issues in `0_Inbox/weekly-review/` files (tags in parentheses, missing spaces, tags glued to adjacent text). |
| `scan_tags.py` | Full-vault tag scan: lists all tags, flags weird ones (6-digit hex colors, pure numbers, number-prefixed alphanumerics) and tags glued to adjacent text. |
| `scan_tags_v2.py` | Like `scan_tags.py` but only reports tags immediately followed by a non-whitespace character. |
| `scan_tags_v3.py` | Reports tags with bad characters on either side (both leading and trailing glue). |
| `find_weird_real_tags.py` | Among tags Obsidian actually recognizes, find weird ones (hex colors, pure numbers, number-started alphanumerics). |
| `find_weird_tags.py` | Search for a hardcoded list of known problematic tags (adjust the list in the script as needed). |
| `find_bad_tags.py` | Find the `#tag):` pattern — a tag immediately followed by a closing paren and colon, which Obsidian swallows into the tag name. |
| `fix_backup_tags.py` | Rewrite `- #type title (#tag1 #tag2): content` lines to `- #type #tag1 #tag2 title: content` in a backup directory. |
| `fix_color_values.py` | Wrap 6-digit hex color values (e.g. `#2584ff`) in backticks in a given file, so Obsidian does not treat them as tags. Takes a file path as argument. |
| `fix_prompt_color.py` | Variant of the above with stricter lookbehind/lookahead. Takes a file path as argument. |

## Rules

1. Do not fabricate or expand content not in the diary notes.
2. Compile only the specified week; do not mix other weeks in.
3. File name and title date ranges must be consistent.
4. Report: reviewed range, output file path, whether all 7 notes existed, which unresolved questions were kept.

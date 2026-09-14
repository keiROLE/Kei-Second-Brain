---
name: wr-1
description: Weekly review — compile the last complete week (Monday-Sunday) of 7 diary notes into a concise weekly review document in 0_Inbox/weekly-review/, and mark each diary frontmatter with weekly_reviewed. Triggers on "/wr-1", "weekly review" or "last week review".
---

> This skill is part of the Kei-Second-Brain ecosystem. System overview is in `README.md`.

# wr-1 — Weekly Review

Compile the last complete week (Monday–Sunday) of 7 diary notes into a concise weekly review document. Raw diary notes only get a frontmatter marker appended — their body is never rewritten. Usually run on Monday morning.

## Trigger

User says "/wr-1", "weekly review", "last week review", or asks to compile the last week's diary notes.

## Before starting

1. Confirm "today" from the system's current date.
2. Default target: the last **completed** Monday–Sunday. If today is Monday, last week = today-7 .. today-1. If today is not Monday, still take the previous complete Monday–Sunday and tell the user the chosen range.
3. Check whether the 7 diary notes exist and whether they are already marked `weekly_reviewed`; skip marked ones and say so.

## Files to read

- Diary notes: `0_Inbox/diary/YYYY-MM-DD.md`, Monday–Sunday (7 notes).
- Format reference: `2_Schema/templates/weekly-review-template.md`.
- Example: the most recent weekly review in `0_Inbox/weekly-review/`.

## Compile flow

1. Read all 7 diary notes; extract key events, thoughts, quotes, methods, inputs and unfinished tasks.
2. Merge by day into daily entries, keeping the diary's tag conventions.
3. Cross-week summary: key events, cognition & reflections, unresolved questions.
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
- `## Cognition & Reflection`
- `## Unresolved Questions`

## Update diary notes

Append `weekly_reviewed: YYYY-MM-DD` to each compiled diary's frontmatter. Only append the field; never rewrite the body; never overwrite an existing value.

## Rules

1. Do not fabricate or expand content not in the diary notes.
2. Compile only the specified week; do not mix other weeks in.
3. File name and title date ranges must be consistent.
4. Report: reviewed range, output file path, whether all 7 notes existed, which unresolved questions were kept.

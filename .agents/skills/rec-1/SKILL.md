---
name: rec-1
description: Append a tagged block per distinct outcome to today's diary. Triggers on "/rec-1", "log it", "note it down", "write it to today's diary", or when an AI task produces an outcome worth logging.
---

> This skill is part of the Kei-Second-Brain ecosystem. The authoritative system entry is `AGENTS.md` (skill inventory + operating rules); `README.md` is the project showcase for GitHub visitors.

# rec-1 — Minimal Diary Logging

A lightweight wrap-up action for task outcomes and project progress. Append to today's diary log and keep the user's existing entries intact.

## Trigger

- User says "/rec-1", "log it", "note it down", "write it to today's diary", "record this", etc.
- An AI task wraps up with a recordable outcome / project progress (default: auto-append; skip only for pure chat with no output).
- If unsure whether it is worth logging, ask in one sentence: "Want me to log this to today's diary?" — no elaboration.

## Before starting

1. Use the user's local date (YYYY-MM-DD).
2. Locate `0_Inbox/diary/<today>.md`. If it does not exist, create it from `2_Schema/templates/diary-template.md` and fill in the date placeholder.
3. Read the topic-tag registry in `2_Schema/naming.md` before choosing tags.

## What to write (style: minimal)

- Write one block per distinct matter. Summarize multiple rounds on the same matter in one block and put independent matters in the order they occurred.
- Start each block with a type tag such as `#event`, then `#project` if useful, then at least one topic tag and the text. Keep the same topic tag across days. Choose a short, reusable tag when the registry has no match. Update the registry when the user asks.
- State what was done, its result or current status, and link any usable vault output with `[[links]]`.
- Use one sentence when it captures the outcome. Keep lines for the same block contiguous and separate blocks with a blank line.

Good examples:

```
#event #knowledge-base Compiled the research notes into [[Source-verification-guide]] .

#event #project #learning Set the exercise order and linked it from [[Learning-plan]] .
```

## Write flow

1. Read today's diary. Find the log using the heading conventions in `2_Schema/diary-system.md`. If it is absent, add the canonical log before the input or other known section, or at the end when there is no later section.
2. Leave one blank line between log blocks: append after existing content in that section; if empty, write directly under the heading.
3. Never overwrite, move or delete anything the user wrote.
4. Re-read the file after writing to confirm the append position is correct and section boundaries are intact.

## Diary rules

- The diary is the raw material layer: append only, never rewrite, never overwrite.
- Keep all input, output, task, and plan sections intact.
- Do not fabricate anything that did not happen in this task.

## Report

One sentence: what was logged, and into which day's diary (with file path). No elaboration.

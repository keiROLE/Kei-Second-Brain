---
name: rec-1
description: Minimal diary logging — at task wrap-up or project progress, append a one-line record of "what AI did and where things stand" to the `## Log` section of today's diary note 0_Inbox/diary/YYYY-MM-DD.md. Triggers on "/rec-1", "log it", "note it down", "write it to today's diary".
---

> This skill is part of the Kei-Second-Brain ecosystem. System overview is in `README.md`.

# rec-1 — Minimal Diary Logging

A lightweight wrap-up action: when a task finishes or a project moves forward, append a short entry to today's diary's `## Log` section. Append only — never rewrite or overwrite. Keep the style minimal.

## Trigger

- User says "/rec-1", "log it", "note it down", "write it to today's diary", "record this", etc.
- An AI task wraps up with a recordable outcome / project progress (default: auto-append; skip only for pure chat with no output).
- If unsure whether it is worth logging, ask in one sentence: "Want me to log this to today's diary?" — no elaboration.

## Before starting

1. Confirm "today" from the system's current date (YYYY-MM-DD).
2. Locate `0_Inbox/diary/<today>.md`; if it does not exist, create it from the diary template (`2_Schema/templates/diary-template.md`).

## What to write (style: minimal)

- One line per item: "what was done + result/progress", no filler words.
- Tags (`#event`, `#project` etc.) go at the **front of the log block** (before the text). Use `#event` for progress/results; multiple lines on the same matter stay contiguous with no blank lines between.
- Linkable outputs (wiki entries, documents, files) get `[[links]]`.
- Project context → add a bare `#project` at the front of the block.
- Default 1-3 lines; one sentence if one is enough.

Good examples:

```
#event Removed opencode, kept [[Full-OpenCode-Conversation-Value]]

#event #project Rebuilt plan_2 with AI; phase 1 split into 7 subtasks
```

## Write flow

1. Read today's diary; locate the `## Log` section.
2. Leave one blank line between log blocks: append after existing content in that section; if empty, write directly under the heading.
3. Never overwrite, move or delete anything the user wrote.
4. Re-read the file after writing to confirm the append position is correct and section boundaries are intact.

## Diary rules

- The diary is the raw material layer: append only, never rewrite, never overwrite.
- Do not touch other sections (`## Tasks`, `## Thoughts`, `# PLAN` etc.).
- Do not fabricate anything that did not happen in this task.

## Report

One sentence: what was logged, and into which day's diary (with file path). No elaboration.

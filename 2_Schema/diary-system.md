---
abstract: "Diary note conventions: paragraph structure, line-level tags, and the rules AI follows when compiling raw daily notes into wiki entries."
author: Kei
created: 2026-07-19
updated: 2026-11-18
tags:
  - diary
  - knowledge-base
  - operating-rules
---

# Diary System

> **System entry point**: This document is part of the Kei-Second-Brain ecosystem. For the full system overview, see `README.md`; for AI behavior rules, see `AGENTS.md` (repo root); for global rules, see `2_Schema/TheSchema.md`.

A diary note is a raw personal record of life — not a wiki entry, not a task list.

Templates: `2_Schema/templates/diary-template.md` (daily note), `2_Schema/templates/weekly-review-template.md` (weekly review).

## 1. Paragraph Structure

Every diary note is fixed to the following sections, in this order:

| Section | Role | Who writes |
|---------|------|------------|
| `# Log:` | Today's events, thoughts, excerpts, and progress in tagged blocks | User handwritten + AI append (`/rec-1`) |
| `# Input:` | Reading notes, excerpts, other knowledge consumed today, and `#learn` tasks | User pastes / AI organizes |
| `# Output:` | Optional section for content produced today | User / AI |
| `# Plan:` | Today's tasks, including any `## Temporary Plan:` checklist | User |

- The template ships empty section headings only; when AI appends content, it must not reorder the sections or touch what the user handwrote.
- Recognize older section headings at level 1 or 2, including `Log`, `记录`, `记录 / Log` and the equivalents for Input, Output, and Plan. Trailing colons are optional and English labels are case-insensitive. A known peer section ends the current section even if an older note mixes levels. Preserve the existing headings.
- Create only the section needed for the current append.

## 2. How to Write

### Line-level tag quick reference (put at the front of a block)

> Tags are mentioned in backticks throughout this document (e.g. `#event`) so they do not render as headings; **when actually writing a diary note, write the tag without backticks**.

| Tag | Meaning | When to use |
|-----|---------|-------------|
| `#event` | Things that happened / progress / results | Project moves, meetings, attempts, outcomes, incidents |
| `#thought` | Thoughts / judgments / reflections / feelings / inspiration | Your own conclusions, feelings, insights |
| `#quote` | Excerpts | Exact words from books, articles, courses, other people |
| `#question` | Open questions / to research | No answer yet; something to look up later |
| `#next` | Next step | A concrete action you mean to do later |
| `#method` | Methodology | A summarized or acquired method / workflow |
| `#learn` | Things learned | Common-knowledge takeaways |
| `#project` | Project context (bare `#project`, no `/project-name`) | When a block needs project context |
| `#prompt` | Prompts | Prompts given to AI |
| `#script` | Script text | A script drafted for a video / audio piece |
| `#OMC` | Others' Media Copy | Content others publish on public or private platforms with a clear commercial purpose: building trust through persona and storytelling, then inserting a call-to-action (joining a group, DMing, etc.) to convert public traffic into private assets |
| `#life` | Life stream | Daily records that need no output or conclusion |
| `#personal-theory` | Your own original theory | A theory you proposed, possibly after discussing it with AI; may be unconventional |

The list above is the baseline set. You may extend it with your own domain tags as needed.

### Category tags (subject matter)

Category tags describe what the block is about. Put them after the type tag and optional `#project`, separated by spaces. AI log blocks use the topic-tag registry in `2_Schema/naming.md` so the same matter stays findable across days.

### Basic principles

- Tags go at the **front** of the block, before the text; when one thing needs multiple lines, keep the lines consecutive with no blank line between them.
- One line = one thing, one thought, or one excerpt.
- Consecutive non-blank lines belong to the same block; a blank line is the boundary between blocks.
- You may write a single sentence or a messy stream; there is no requirement to log everything every day.
- You do not have to write only for "value" — a life record with no output is worth keeping too.
- No manual filing into projects, tasks, or the wiki; the later AI compilation decides that.
- Tags are optional. When the meaning is obvious, you may skip them.
- Locked / finalized content (a finalized statement, a finalized plan, a locked external messaging line) goes under `#event` (project progress / outcome), **not** `#method`. When the text is long, put the tag on its own line below rather than cramming it at the end of a long line.
- Combine updates on the same matter into one AI log block with the action, result, and any output link. Give independent outcomes their own blocks in the order they occurred.

### Example

```md
#event Ran a deep-work block on the draft: finished the first outline and saved it to [[draft-outline]]

#event #project Restructured the project plan; phase one was split into 7 subtasks

- Don't treat an unvalidated direction as a long-term commitment. #thought
- Spent most of the day reading, nothing shipped. #life
- Why did the build fail silently? Need to look into it later. #question
- Add the scope notes tomorrow. #next
- Final report outline locked: three sections + short abstract, saved into today's 记录 / Log.
  #event
```

## 3. Rules for AI: Compiling Diary Notes

### What a diary note is

- A diary note is the raw-material layer: preserve the original text — do not edit, do not move, do not overwrite.
- When parsing, split blocks by blank lines: consecutive non-blank lines (including a tag-only line) are one thing; a blank line starts the next.
- The diary's value is judged by the AI at compile time; the user carries no pre-classification burden.
- Never delete or rewrite content just because it is fragmented, emotional, or has no "action value".
- Never mechanically split one diary note into many wiki entries. Only content that is reusable and stands on its own deserves to be distilled.

### Tag interpretation & handling

If a tag line appears on its own, it binds to the most recent consecutive block above it — never treat it as a standalone event.

| Tag | How AI should read it | Possible output |
|-----|-----------------------|-----------------|
| `#event` | Facts, project status, attempts and results | Update the project entity / project record; extract transferable lessons |
| `#thought` | The user's personal judgments and reflections | Judge whether it can be compiled into a concept or framework; preserve personal voice and qualifiers |
| `#quote` | Exact words or excerpts from external sources | Mark as an external viewpoint; do not treat it as the user's stance or as fact by default |
| `#question` | Unresolved questions | Collect into a to-research list; never write into the wiki as a conclusion before it is verified |
| `#next` | The user's intentions and next actions | Move into the task system only when the user explicitly asks for task cleanup; otherwise keep it in the diary |
| `#method` | Summarized methodology | Prioritize compiling into framework / concept entries |
| `#learn` | Newly learned common knowledge | Judge whether it is worth distilling into a resource entry |
| `#project` | Project context anchor | Prefer linking to the matching project entity, framework, or raw project material |
| `#life` | Life facts and personal experiences | Not compiled by default; suggest distilling only when it reveals a long-term pattern, an important relationship, or a reusable lesson |
| `#personal-theory` | The user's original theory | Keep original attribution and personal voice; never generalize it as universal fact |

### Compilation criteria

Prioritize extracting:

1. Methods, judgments, or workflows that recur and have been tested in practice.
2. Key events that clearly changed project direction, strategy, or outcomes.
3. Concepts, frameworks, resources, or comparisons that outlive the day and stay useful in the future.
4. Open questions worth tracking — kept in a "to be verified" state.

Do not compile directly:

- Pure life stream, one-off emotions, gaming sessions.
- Unverified guesses, retellings, or excerpts.
- Temporary tasks and to-do arrangements that belong only to that day.
- Fragments that lack context and cannot be explained on their own.

### Compilation output rules

- Follow `[[TheSchema]]` for directory layout, naming, frontmatter, and link conventions.
- When creating a new wiki entry, `source` must link back to the diary note it came from.
- When the user's original words are a personal judgment, keep its qualifiers — do not generalize it into a fact.
- Quotes and external viewpoints must keep their source context; an unknown source is flagged as low-confidence or kept as to-be-verified material only.
- Before compiling, check whether the wiki already has an entry on the same topic: prefer supplementing or linking it; avoid creating duplicate cards.
- When unsure whether something is worth compiling, do not create entries unilaterally — list it as a suggestion in the compile report for the user to confirm.

## 4. Division of Labor: Diary / Weekly Review / Wiki

| Document | Role | How it is written |
|----------|------|-------------------|
| Diary note (`0_Inbox/diary/YYYY-MM-DD.md`) | Raw events, thoughts, excerpts, life records | Written anytime, one line per item, optional line-level tags |
| Weekly review (`0_Inbox/weekly-review/`) | Goal progress, time ROI, problem review, next week's focus | Compiled weekly by `/wr-1` from the last full week of diary notes, answering fixed questions |
| `1_Wiki` | Reusable knowledge after judgment | Maintained by AI compilation (`/by-1`, `/by-a`) |

# AGENTS.md — Kei-Second-Brain Vault Guide

This directory is an Obsidian vault. This file is the **project-level behavior contract** for any AI agent working inside this vault; it lives at the repo root so an AI client reads it first. Read it together with `README.md` (system entry) and `2_Schema/TheSchema.md` (global rules).

> 🔗 **This file is the master entry of the vault system**: directory structure / skill inventory (single source of truth) / operating rules / command cheatsheet all live here. Rule details (link types, quality red lines, frontmatter fields, naming, pipeline) live under `2_Schema/` (TheSchema, frontmatter, naming, pipeline, diary-system). Any AI task must read this file first.

---

## Project Skills (single source of truth)

This project ships **9 project-level skills** in `.agents/skills/`.

> **Single source of truth**: this inventory (name / trigger / responsibility / output) is maintained **only in this file**. TheSchema references it but does not copy it — when the two disagree, this file wins. After changing any skill, you must update this inventory in the same change.

| Skill | Trigger | Responsibility | Output |
|-------|---------|----------------|--------|
| `by-1` | `/by-1` — "compile this note" | Read a single raw note → extract knowledge → compile into `1_Wiki/` | A wiki entry + index update |
| `by-a` | `/by-a` — "compile everything" | Scan the vault for uncompiled notes and batch-compile them (run `find_uncompiled.py` first) | Wiki entries + index + compile report |
| `kbi` | `/kbi` — "health check" / "vault iteration" | Scan the whole vault: gaps, uncompiled notes, broken links, hallucinations, islands (run `audit_links.py` first) | Iteration report (read-only) |
| `jh-1` | `/jh-1` — "aggregate topic X" | Scan related entries by topic → build a knowledge map → suggest merges / new entries | Knowledge map |
| `wr-1` | `/wr-1` — "weekly review" | Take the last full week's diary notes → produce a weekly review doc | Weekly review note |
| `chat-distill` | `/chat-distill` — "distill conversations" | Collect → filter → archive → compile → link reusable AI conversations | chat-distill raw notes + wiki entries |
| `chiselplan` | `/chiselplan` — "plan my project" / "phase review" | Goal → task phases → update the plan file | Updated plan file |
| `blog-1` | `/blog-1` — "make a blog post" | Generate blog docs — articles, project write-ups, share posts | Markdown doc in `4_Outputs/` |
| `rec-1` | `/rec-1` — "log to diary" | Append-only minimal log of the current task to today's diary log section | Diary append (never rewrite) |

## Operating Rules (mandatory)

1. **Archive before delete/overwrite**: any deletion, overwrite or rewrite of vault files must first move the original into `1_Wiki/archive/` (prepend `YYYY-MM-DD-` on name conflict), then apply the change. **Permanent deletion is forbidden** (no un-recoverable removal). Archived files are treated as deprecated and may be cleaned up by later passes.
2. **Only touch what was named**: do not expand the task scope. Read the original file before modifying it; keep content that was not asked to be changed.
3. **Formatting rules**: tags mentioned in prose must be wrapped in backticks (e.g. `#event`; example code blocks excluded). When writing tags and wiki links, always keep a space before and after them — never glue them to text, Chinese brackets or punctuation (e.g. `标题（#认知）：` or `文字[[链接]]` are both wrong).

## Git Workflow

This repo is a git repository: commit small, reviewable steps. The skill inventory above and the actual `.agents/skills/` folder must stay in sync — a skill change is not done until this table is updated.

## Core Directory Conventions

- **Naming**: document / entry / file names contain no spaces — join words with `-` (e.g. `monitor-selection-guide.md`); the human-readable title may keep spaces.

| Path | Role |
|------|------|
| `0_Inbox/` | Raw material layer: unprocessed input (diary/, weekly-review/, chat-distill/, clippings/). Read-only — AI may only append frontmatter marker fields. |
| `1_Wiki/` | Knowledge compilation layer: compiled entries (concepts/, entities/, comparisons/, frameworks/, resources/), templates/, archive/; entry point `index.md`. |
| `2_Schema/` | Configuration layer: TheSchema, frontmatter, naming, pipeline, `diary-system.md` (diary system spec), `templates/`, and `memory/` (AI working memory — see below). |
| `3_KBI-log/` | Iteration layer: compile reports, iteration reports, link audits, other AI analysis outputs. |
| `4_Outputs/` | Output layer: content compiled from wiki entries (articles, scripts, posts). |
| `.agents/skills/` | The 9 project skills. Read the corresponding SKILL.md before using a skill. |

## Memory — AI Working Memory

`2_Schema/memory/` is the working-memory module for AI agents: a master index (`memory-index.md`) plus one snapshot doc per active work domain — current status, key asset entry points, red lines. **Usage rules**: read the matching domain doc before acting on that domain; write new status back to it before continuing; red lines are hard constraints; when unsure, ask. Full contract: `2_Schema/memory/README.md`.

## Document-Type Tasks

Before creating or modifying documents (PDF / Word / PPT / HTML), follow the quality red lines in `2_Schema/TheSchema.md` §8 and the operating manual in `2_Schema/pipeline.md` — no fabrication, traceable facts, structure over decoration.

## Command Cheatsheet

| You want to… | Trigger |
|--------------|---------|
| Compile a single note | `/by-1` |
| Compile all uncompiled notes | `/by-a` |
| Vault health check / iteration analysis | `/kbi` |
| Topic knowledge map | `/jh-1` |
| Weekly review | `/wr-1` |
| Log this task to today's diary | `/rec-1` |
| Distill AI conversations | `/chat-distill` |
| Project planning / phase review | `/chiselplan` |
| Generate a blog doc | `/blog-1` |

## Diary Frontmatter

Diary notes use `weekly_reviewed: YYYY-MM-DD` after being covered by a weekly review; reviewed notes are skipped and not re-processed.

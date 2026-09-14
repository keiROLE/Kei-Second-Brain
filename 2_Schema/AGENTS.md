# AGENTS.md — Kei-Second-Brain Vault Guide

This file is the project-level behavior contract for AI agents working inside this vault. Follow it together with `README.md` (system entry) and `TheSchema.md` (global rules).

---

## Operating Rules (mandatory)

1. **Archive before delete/overwrite**: any deletion, overwrite or rewrite of vault files must first move the original into `1_Wiki/archive/` (prepend `YYYY-MM-DD-` on name conflict), then apply the change. **Permanent deletion is forbidden** (no un-recoverable removal).
2. **Only touch what was named**: do not expand the task scope. Read the original file before modifying it; keep content that was not asked to be changed.

## Core Directory Conventions

| Path | Role |
|------|------|
| `0_Inbox/` | Raw material layer: unprocessed input (diary/, weekly-review/, chat-distill/, clippings/). Read-only, never edited in place. |
| `1_Wiki/` | Knowledge compilation layer: compiled entries (concepts/entities/comparisons/frameworks/resources), templates/, archive/, index.md |
| `2_Schema/` | Configuration layer: TheSchema, AGENTS, frontmatter, naming, pipeline, templates |
| `3_KnowledgeBaseIterationLog/` | Compile reports, iteration reports, link audits, other AI analysis outputs |
| `.agents/skills/` | Project skills (SKILL.md files). Read the corresponding SKILL.md before using a skill. |

## Document-Type Tasks

Before creating or modifying PDF / Word / PPT documents, read the relevant style requirements in this vault first and follow them strictly, minimizing revision rounds.

## Skill Inventory

The authoritative skill list (name / trigger / responsibility / output) is maintained **only** in `README.md`. This file does not copy the list. When in doubt, follow README.

## Diary Frontmatter

Diary notes use `weekly_reviewed: YYYY-MM-DD` after being covered by a weekly review; reviewed notes are skipped and not re-processed.

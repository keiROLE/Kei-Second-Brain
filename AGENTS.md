# AGENTS.md — Kei-Second-Brain Vault Guide

This file is the authoritative entry point for the vault's operating rules, directory conventions, and skill inventory. Read it before working in the vault. Detailed rules live in `2_Schema/`. The README introduces the project.

## Project skills

Skills live under `.agents/skills/<name>/`. Read the relevant `SKILL.md` before using it. Update this inventory in the same change as any skill addition or change to its trigger, responsibility, or output.

| Skill | Trigger | Responsibility | Output |
|---|---|---|---|
| `by-1` | `/by-1`, “compile this” | Extract reusable knowledge from one source | Wiki entries and index update |
| `by-a` | `/by-a`, “compile everything” | Scan eligible sources and compile them in batches | Wiki entries, index update, and compile report |
| `kbi` | `/kbi`, “health check”, `/kbi repair` | Audit the vault and apply verified low-risk changes when repair is requested | Iteration report and any applied repairs |
| `jh-1` | `/jh-1`, “topic map” | Map entries for a topic and propose improvements | Knowledge map |
| `wr-1` | `/wr-1`, “weekly review” | Review the last complete Monday–Sunday week | Weekly review and diary markers |
| `rec-1` | `/rec-1`, “log it”, task wrap-up | Append one topic-tagged block per distinct matter | Today's diary log |
| `chat-distill` | `/chat-distill`, “distill conversations” | Select and compile reusable conclusions from conversations | Source notes and Wiki entries |
| `chiselplan` | `/chiselplan`, “re-plan”, “phase review” | Define a goal and its phases, or review progress | Project plan in `2_Schema/chiselplan/` |
| `kbr` | `/kbr`, “recall a batch” | Quiz the user on important, overdue, and new Wiki concepts | Local scores and history, plus first-review tags |
| `blog-1` | `/blog-1`, “make a blog post” | Draft articles, project pages, and shares | Markdown in `4_Outputs/` |

## Operating rules

1. **Archive before delete or overwrite.** Move original vault files into `1_Wiki/archive/` before deletion, overwrite, or rewrite. Use a `YYYY-MM-DD-` prefix when names collide. Keep archived originals recoverable. Never permanently delete vault files.
2. **Keep scope narrow.** Read the original before editing. Preserve the user's unrelated text, tasks, and metadata.
3. **Limit routine writes to the designated fields.** Compilation preserves source bodies and writes only processing markers. Diary changes follow `2_Schema/diary-system.md`. `/kbr` may add a single first-review tag without changing other frontmatter or the body. KBI repairs require the requested repair mode and a recoverable original.
4. **Format tags and links.** In prose, put literal tags in backticks, such as `#event`. In vault entries, keep spaces around tags and wikilinks, including next to punctuation.
5. **Keep public settings portable.** Shared configurations use vault-relative paths. Store local paths, credentials, and generated recall state outside tracked public files.

## Git workflow

Commit small, reviewable steps. Keep the skill inventory synchronized with the skill directories.

## Directory conventions

Use hyphens in filenames. Display titles may contain spaces.

| Path | Role |
|---|---|
| `0_Inbox/` | Raw notes, including `diary/`, `weekly-review/`, `chat-distill/`, and `clippings/` |
| `1_Wiki/` | Compiled concepts, entities, comparisons, frameworks, and resources, navigated from `index.md` |
| `2_Schema/` | Rules, templates, plans, and AI working memory |
| `3_KBI-log/` | Compile reports, iteration reports, and audits |
| `4_Outputs/` | Drafts and analyses derived from the wiki |

Weekly reviews add `weekly_reviewed: YYYY-MM-DD` to each covered diary. Skip diaries already marked with this field.

## Working memory

Use `2_Schema/memory/memory-index.md` to find a domain snapshot. Read the matching domain before acting. Update it when its state changes, preserve its red lines, and ask when its instructions are unclear. See `2_Schema/memory/README.md` for the contract.

## Document tasks

Before creating or editing PDF, Word, slides, or HTML, read the quality red lines in `2_Schema/TheSchema.md` and the operating instructions in `2_Schema/pipeline.md`. Keep facts traceable and prioritize the structure users need.

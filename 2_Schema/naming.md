---
title: "Naming Conventions & PARA Classification"
type: schema
updated: 2026-11-01
tags:
  - config
  - naming
  - PARA/resource
---

# Naming Conventions & PARA Classification

---

## 1. Directory layer numbering

The layer number *is* the layer. All names are short English with a numeric prefix; multi-word names use hyphens, never spaces.

| Layer | Directory | Role | Read/Write |
|-------|-----------|------|------------|
| 0 | `0_Inbox/` | Raw material layer | Compilation preserves source text. Diary edits follow `diary-system.md`. |
| 1 | `1_Wiki/` | Knowledge compilation layer | AI read/write |
| 2 | `2_Schema/` | Configuration layer | AI read/write |
| 3 | `3_KBI-log/` | Iteration layer (compile / iteration / link-audit reports) | AI write |
| 4 | `4_Outputs/` | Output layer (content compiled from entries) | AI write |

### Subdirectory rules

- Lowercase English, hyphenated: `weekly-review/`, `chat-distill/`.
- `0_Inbox/`: `diary/`, `weekly-review/`, `chat-distill/`, `clippings/`.
- `1_Wiki/`: `concepts/`, `entities/`, `comparisons/`, `frameworks/`, `resources/`, `templates/`, `archive/` + `index.md`.
- `2_Schema/`: rule files + `templates/` (templates) + `chiselplan/` (planning skill workspace).
- Pre-existing legacy folders are kept in place and are **not** part of the numbering system.

## 2. Skill naming

Uniform format: **`<verb-short>-<optional number>`** (this open-source release uses no vault prefix).

- Keep function names short, such as `kbi` for iteration analysis, `kbr` for active recall, or `chiselplan` for planning.
- Use `-1` for single-item actions such as `by-1` and `-a` for bulk actions such as `by-a`.
- Forbidden: full verb names (e.g. `kb-iter`), mixed languages, meaningless numbers.

## 3. Files & entries

- English filenames, short and clear. No "untitled", "misc" or vague prefixes.
- Concept entries use the core term: `barrier-to-entry-as-profit.md`
- Framework entries use the core term: `sdd-workflow.md`
- Comparison entries use "A vs B": `student-mindset-vs-money-mindset.md`
- Resource entries use the resource name: `obsidian-plugins.md`
- Dates always `YYYY-MM-DD`
- Diaries: `0_Inbox/diary/YYYY-MM-DD.md`
- Weekly reviews: `0_Inbox/weekly-review/MMDD-weekly-review.md`
- Reports: see TheSchema §6 (Output File Storage Rules)
- Same skill run multiple times a day: append a sequence number (`jh-1-topic-2026-06-24-2.md`)

### Repo / vault level

- Directories: `0_Inbox`, `1_Wiki`, `2_Schema`, `3_KBI-log`, `4_Outputs` — fixed, do not rename.
- Subdirectories: lowercase with hyphens (`weekly-review`, `chat-distill`).

### Skill directories

- Project skills live in `.agents/skills/<short-name>/`. Short names use a lowercase abbreviation, optionally with a number: `by-1` (single compile), `by-a` (bulk compile), `kbi` (KB iteration), `jh-1` (topic map), `wr-1` (weekly review), `rec-1` (diary record), `chat-distill`, `chiselplan` (planning), `blog-1` (blog output).
- The `name` field in each SKILL.md must match its directory name.
- Companion scripts (deterministic parts) live in the same directory; SKILL.md must reference them with a **run-first** instruction using a relative path from the vault root (e.g. `python .agents/skills/by-a/find_uncompiled.py`), never an absolute path — the repo is cloned anywhere.

---

## 4. PARA Classification Criteria

Every note gets a PARA tag. Classification is by *what the note is for*, not by topic.

| Category | Tag | Criterion | Examples |
|----------|-----|-----------|----------|
| **Project** | `#para/project` | Has a defined end state and deadline | "Launch the newsletter", "Learn Python" |
| **Area** | `#para/area` | Ongoing responsibility, no end date | Health, finances, career growth |
| **Resource** | `#para/resource` | Reference material for future use | Tutorials, tools, articles, concepts |
| **Archive** | `#para/archive` | Inactive items from the other three | Finished projects, old areas |

**Decision flow for a new note:**
1. Is it tied to a specific outcome with an end? → `#para/project`
2. Is it a standing responsibility you maintain? → `#para/area`
3. Is it reference material to be consulted later? → `#para/resource`
4. Is it inactive / done / shelved? → `#para/archive`

- Mixed-type notes may carry more than one PARA tag.
- The tag system is governed by TheSchema §2.

> Note: the PARA taxonomy is a classification skeleton; this system's added value is the AI compilation layer on top of it (see README "Comparison with other methods").

---

## 5. Tags

- Type tags: `#concept` `#entity` `#comparison` `#framework` `#resource`
- Status tags: `#inbox/raw` (unprocessed material), `#compiled` (organized documents)
- Topic tags: free-form, descriptive, lowercase (`#media`, `#sales`, `#ai-tools`)
- Every 1_Wiki entry carries ≥ 3 tags: type + topic + PARA.

## 6. Diary topic-tag registry

Use one topic tag per AI log block by default. Reuse it for the same matter across days. Add a second when the block advances both topics. Put topic tags after the type tag and the optional `#project`.

| Tag | Use for |
|---|---|
| `#knowledge-base` | Vault rules, note capture, compilation, and maintenance |
| `#learning` | Study plans, exercises, and learning progress |
| `#content-creation` | Research, drafts, editing, and publishing |
| `#software` | Code, tools, integrations, and testing |
| `#planning` | Goals, schedules, and phase reviews |

Extend this registry with the user's stable topic names when requested.

---

> Core principle: **one name says one thing** — the directory says the layer, the skill name says its function, the entry name says its content. Inconsistent naming is where maintenance cost comes from: change one place and update every reference.

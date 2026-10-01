---
title: "Naming Conventions & PARA Classification"
type: schema
updated: 2026-10-01
tags:
  - config
  - naming
---

# Naming Conventions & PARA Classification

---

## 1. Naming Conventions

### Files & entries

- English filenames, short and clear. No "untitled", "misc" or vague prefixes.
- Concept entries use the core term: `barrier-to-entry-as-profit.md`
- Framework entries use the core term: `sdd-workflow.md`
- Comparison entries use "A vs B": `student-mindset-vs-money-mindset.md`
- Resource entries use the resource name: `obsidian-plugins.md`
- Dates always `YYYY-MM-DD`
- Diaries: `0_Inbox/diary/YYYY-MM-DD.md`
- Reports: see TheSchema §6 (Output File Storage Rules)

### Repo / vault level

- Directories: `0_Inbox`, `1_Wiki`, `2_Schema`, `3_KBI-log`, `4_Outputs` — fixed, do not rename.
- Subdirectories: lowercase with hyphens (`weekly-review`, `chat-distill`).

### Skill directories

- Project skills live in `.agents/skills/<short-name>/`. Short names use a lowercase abbreviation, optionally with a number: `by-1` (single compile), `by-a` (bulk compile), `kbi` (KB iteration), `jh-1` (topic map), `wr-1` (weekly review), `rec-1` (diary record), `chat-distill`, `chiselplan` (planning), `blog-1` (blog output).
- The `name` field in each SKILL.md must match its directory name.
- Companion scripts (deterministic parts) live in the same directory; SKILL.md must reference them with a **run-first** instruction using a relative path from the vault root (e.g. `python .agents/skills/by-a/find_uncompiled.py`), never an absolute path — the repo is cloned anywhere.

---

## 2. PARA Classification Criteria

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

> Note: the PARA taxonomy is a classification skeleton; this system's added value is the AI compilation layer on top of it (see README "Comparison with other methods").

---

## 3. Tags

- Type tags: `#concept` `#entity` `#comparison` `#framework` `#resource`
- Status tags: `#inbox/raw` (unprocessed material), `#compiled` (organized documents)
- Topic tags: free-form, descriptive, lowercase (`#media`, `#sales`, `#ai-tools`)
- Every 1_Wiki entry carries ≥ 3 tags: type + topic + PARA.

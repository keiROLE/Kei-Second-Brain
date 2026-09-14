---
title: "TheSchema — Global Configuration"
type: schema
updated: 2026-09-14
tags:
  - config
  - knowledge-base
  - operating-rules
---

# TheSchema

The global rules, naming conventions and AI workflows of the knowledge base.

> **System entry point**: This specification is part of the Kei-Second-Brain ecosystem. For the full system overview, see `README.md`.
> This document is the "operating system" of the Obsidian vault. Every AI task and every human action must follow it.
> Detailed rules live in the sibling documents under `2_Schema/`; this file is the index and the authority.

---

## 1. Directory Structure

### Three-layer architecture

| Layer | Directory | Role | Read/Write |
|-------|-----------|------|------------|
| 0_Inbox/ | Raw material layer | Source of truth; never edited in place | Read-only |
| 1_Wiki/ | Knowledge compilation layer | The core knowledge base, maintained by AI | AI read/write |
| 2_Schema/ | Configuration layer | The operating system of the vault | AI read/write |
| 3_KnowledgeBaseIterationLog/ | Iteration layer | Compile reports, iteration reports, link audits | AI write |

### 0_Inbox/ — Raw material layer

All unprocessed input lands here.

**What goes in**: web clippings, PDF exports/screenshots, voice-to-text drafts, raw AI conversation logs, anything "save it for later".

**What does not**: thought-out notes (→ 1_Wiki/), action plans (stay where they are), creative works (stay where they are).

**Core rule**: files in 0_Inbox/ are not edited. When the user says "compile the inbox", AI reads files → extracts knowledge → compiles into 1_Wiki/.

Subdirectories:

| Directory | Content |
|-----------|---------|
| diary/ | Daily notes `YYYY-MM-DD.md` |
| weekly-review/ | Weekly review documents |
| chat-distill/ | Distilled AI conversations (raw logs go here first) |
| clippings/ | Web clippings |

### 1_Wiki/ — Knowledge compilation layer

The core knowledge base maintained by AI. Content is **compiled, not stored**.

| Subdirectory | Content | Answers the question |
|--------------|---------|----------------------|
| concepts/ | Concept cards | What is this? |
| entities/ | Entity cards | Which thing / person / organization? |
| comparisons/ | Comparison cards | What is the difference between A and B? |
| frameworks/ | Methodology cards | How to do it? |
| resources/ | Resource cards | Which tools / websites exist? |
| templates/ | 5 entry templates | Template to use when creating an entry |
| archive/ | Processed / discarded | Historical versions |
| index.md | Global navigation | Entry point |

### 2_Schema/ — Configuration layer

Everything the system needs to operate: this file, AGENTS.md, frontmatter.md, naming.md, pipeline.md, templates/.

---

## 2. Tag System

| Tag | Use | Example |
|-----|-----|---------|
| `#concept` | Concept entries | `#concept` |
| `#entity` | Entity entries | `#entity` |
| `#comparison` | Comparison entries | `#comparison` |
| `#framework` | Methodology | `#framework` |
| `#resource` | Tools & resources | `#resource` |
| `#para/project` | Active project | `#para/project` |
| `#para/area` | Ongoing area of responsibility | `#para/area` |
| `#para/resource` | Reference material | `#para/resource` |
| `#para/archive` | Archived / inactive | `#para/archive` |
| `#inbox/raw` | Unprocessed raw material | `#inbox/raw` |
| `#compiled` | Organized / compiled documents | `#compiled` |

Every 1_Wiki entry carries at least 3 tags: type + topic + PARA category.

---

## 3. Link Rules — the only link channel

**All inter-entry links live in a `## See also` section at the end of the entry** (the frontmatter `related`/`links` fields are deprecated — do not use them). Every link must carry one English type label:

```
## See also
- [[barrier-to-entry-as-profit]] apply
- [[underlying-logic-of-making-money]] prerequisite
- [[combining-self-analysis-with-business]] background
```

**The 8 link types (authoritative list):**

| Type | Meaning | Example |
|------|---------|---------|
| `apply` | B is an application/practice of A | discipline-gambling → barrier-to-entry-as-profit |
| `contrast` | A and B contrast / oppose | student-mindset vs money-mindset |
| `cause` | A is the cause or result of B | short-video-algorithm → attention-economics |
| `example` | B is an example of A | five-dimension-formula → information-arbitrage |
| `part-of` | B is a component/sub-concept of A | three-levers → underlying-logic-of-making-money |
| `background` | B is background knowledge needed to understand A | LLM-core-concepts → RAG-principles |
| `related` | Same topic, no more specific relationship | recruiting-mindset → team-communication-system |
| `prerequisite` | B is a prerequisite for A | ml-basics → supervised-learning |

- **A link you cannot label is probably a fake link — do not write it, do not force it.**
- New links must always carry a type label.
- The type list is extensible; when extending, update by-1 / by-a / kb-iter / jh-1 skills accordingly.

### Source section (mandatory traceability)

Every entry starts with a `## Source` section right after the title (`# Title`), before any other section:

```
## Source
- [[making-money-mindset]] (0_Inbox/clippings/making-money-mindset.md)
- [[action-system]] (0_Inbox/chat-distill/action-system.md)
```

- Source is one or more files → one `[[filename]]` link per line (the source filename is the Obsidian link name), with the full path as a comment.
- Source is descriptive text (e.g. "combined RAG knowledge") → write the text as-is, no link.
- The frontmatter `source` field is kept; it and the `## Source` section coexist as cross-references.

---

## 4. Frontmatter Field Spec

All entry templates (in `1_Wiki/templates/`) must include:

| Field | Required | Notes |
|-------|----------|-------|
| title | Yes | Entry title |
| type | Yes | Matches the containing directory: concept/entity/comparison/framework/resource |
| created | Yes | YYYY-MM-DD |
| source | Yes | Full path of source file(s) (compile traceability) |
| confidence | Yes | `high` / `medium` / `low` |
| tags | Yes | At least 3 (type + topic + PARA) |
| aliases | Optional | Alias array, reduces navigation ambiguity |
| author | Yes | `agent` — AI-compiled entries are authored by the compiling agent; never a personal handle |

**Additional required for entities**: `entity_kind` (`person` / `organization` / `project` / `product`).

**Deprecated fields**: `related` / `links` (removed; cross-links live in `## See also`).

Full field inventory: see `frontmatter.md`.

---

## 5. Naming Conventions

- English filenames, short and clear; no "untitled", "misc" or vague prefixes.
- Concept names use the core term: `barrier-to-entry-as-profit.md`
- Framework names use the core term: `sdd-workflow.md`
- Comparison names use "A vs B": `student-mindset-vs-money-mindset.md`
- Dates: `YYYY-MM-DD`

See `naming.md` for the full spec and PARA classification criteria.

---

## 6. Output File Storage Rules

AI skill outputs fall into two groups: **reports** (compile reports, iteration reports incl. link audit) and **other analysis outputs** (single-entry compiles, topic maps).

| Skill | Output file naming | Location |
|-------|--------------------|----------|
| by-1 single compile | `by-1-[topic]-[date].md` | `3_KnowledgeBaseIterationLog/analysis/` |
| by-a compile all | `YYYY-MM-DD-compile-report.md` | `3_KnowledgeBaseIterationLog/` |
| kb-iter iteration | `YYYY-MM-DD-iteration-report.md` (incl. link audit) | `3_KnowledgeBaseIterationLog/` |
| jh-1 topic map | `jh-1-[topic]-[date].md` | `3_KnowledgeBaseIterationLog/analysis/` |

**Naming rules**:
- Date format: `YYYY-MM-DD`
- Topic uses a short keyword, no spaces
- Same skill run multiple times a day: append a sequence number: `jh-1-topic-2026-06-24-2.md`

**Content requirements**: every output file starts with YAML frontmatter:

```yaml
---
title: "[Report Title]"
type: analysis-report
created: YYYY-MM-DD
source_skill: "/by-1" | "/by-a" | "/kb-iter" | "/jh-1"
tags:
  - analysis
  - para/resource
---
```

Body includes: execution time, scan scope, number of issues found, list of recommended actions. Reports **do not modify wiki entries directly** — they output recommendations; the user confirms before changes are applied.

---

## 7. AI Compilation Workflows (user-triggered)

All compilation operations are **explicitly triggered by the user**. Nothing runs automatically.

### 7.1 Compile inbox

Trigger: user says "compile the inbox" or "tidy the inbox".

Steps:
1. Scan 0_Inbox/ for files with `processed: false` **or missing the `processed` field**
2. For each file, extract knowledge units: concepts, entities, frameworks, resources, comparisons
3. Use the corresponding templates in `1_Wiki/templates/`
4. Build cross-references in `## See also` with type labels (8 types; no label → no link)
5. Update `1_Wiki/index.md`
6. Mark the source file `processed: true` (or move to `1_Wiki/archive/`)
7. Write the compile report

### 7.2 Cross-directory compile

Trigger: user says "compile [folder]" or "tidy [folder]".

AI scans all .md files in the given folder and follows the 7.1 flow.

### 7.3 Fragment sorting

Trigger: user says "sort fragments" or "tidy misc".

Scan files whose names contain "misc"/"untitled" fragments, split by blank-line paragraphs, classify each paragraph.

### 7.4 Link completion

Trigger: user says "check links" or "complete links".

Traverse all entries in 1_Wiki/, detect concepts mentioned in the text, add to `## See also` (with type labels; no label → skip) or output a "suggested new entries" list.

### 7.5 Create a new entry

Trigger: user says "create an entry about [topic]".

Determine entry type → use the corresponding template → search existing entries for references → update `index.md`.

---

## 8. Quality Red Lines

- **0_Inbox/ is read-only**: compilation never edits the original (only appends frontmatter markers).
- **No fabrication**: content not present in the source is not written. When unsure, mark `confidence: low`.
- **AI supplements must be labeled**: `> 💡 AI note: ...`
- **Numbers / dates / facts are traceable**: distinguish "verified" from "claimed by one party".
- **Author marker**: AI-compiled content uses `author: agent` (the compiling agent). Raw material written by the vault owner keeps the owner's own handle (e.g. `author: Kei` in diaries).

---

## 9. Standard Workflow

```
Record → Review → Compile → Iterate → Distill → Plan
```

1. **Record**: daily note (`0_Inbox/diary/YYYY-MM-DD.md`); AI appends via `/rec-1`.
2. **Review**: weekly, `/wr-1` compiles the last full week of diary notes into a weekly review.
3. **Compile**: `/by-1` for single docs, `/by-a` for bulk.
4. **Iterate**: `/kb-iter` health check (gaps, broken links, islands, hallucinations, link audit) — read-only report.
5. **Distill**: `/chat-distill` filters AI conversations into the knowledge base.
6. **Plan**: `/chiselplan` for project planning; optional daily loop via the `plan-1` skill it can create.

The end-to-end pipeline (input → compile → maintain → output) with concrete operating steps: see `pipeline.md`.

---

## 10. Document Index (2_Schema/)

| Document | Responsibility |
|----------|----------------|
| TheSchema.md (this file) | Architecture, tags, links, quality lines, workflows |
| AGENTS.md | AI behavior rules for agents working in this vault |
| frontmatter.md | Full frontmatter field inventory |
| naming.md | Naming conventions + PARA classification criteria |
| pipeline.md | End-to-end operating procedure: input → output |
| templates/ | Diary template, weekly review template |

---

> **This document is the global operating manual for AI agents in the Kei-Second-Brain Obsidian vault.**
> **Core principles: pragmatic, direct, structured, never substitute for the user's decisions.**
> **Updated: 2026-09-14**

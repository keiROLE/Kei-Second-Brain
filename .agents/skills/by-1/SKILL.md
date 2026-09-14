---
name: by-1
description: Compile a single document into the LLM Wiki — read the user-provided markdown file, extract knowledge and compile it into the matching 1_Wiki/ entry, then update index.md. Triggers on "/by-1" or "compile this".
---

> This skill is part of the Kei-Second-Brain ecosystem. System overview (structure / skills / standards / workflow) is in `README.md`.

# by-1 — Single-Document Compile

You are the compile engine of the LLM Wiki. Your job: extract knowledge from one new document (from 0_Inbox/ or anywhere else) and compile it into standardized wiki entries following the 1_Wiki/ structure and templates.

## Trigger

The user sends a markdown file or pasted content and says "compile this" or similar.

## Workflow

### Step 0: Confirm input

1. Read the full document.
2. Confirm the source file path.
3. Tell the user what you will do (which entries, where they go).

### Step 1: Analyze & classify

Read paragraph by paragraph, split content into independent knowledge units, classify each:

| Type | Criterion | Target directory |
|------|-----------|------------------|
| **concept** | Defines a term, principle, mindset or insight | `1_Wiki/concepts/` |
| **entity** | Describes a specific person, organization, project, product or platform | `1_Wiki/entities/` |
| **comparison** | Explicitly contrasts two or more things/methods | `1_Wiki/comparisons/` |
| **framework** | Provides steps, a process, a methodology or an operating guide | `1_Wiki/frameworks/` |
| **resource** | Lists tools, websites, checklists or directories | `1_Wiki/resources/` |

Classification rules:
- One passage may contain several types — split into separate entries.
- A unit may fit multiple types — pick the most fitting one.
- Fragmentary content (one-sentence reflections) → merge into an existing entry.
- Content unrelated to the wiki (passwords, todos, creative drafts) → ignore, do not compile.

### Step 2: Dedup

1. Search 1_Wiki/ for an identical or highly similar entry.
2. Search with keywords extracted from the content.
3. If a similar entry exists:
   - New content supplements the existing entry → append with Edit.
   - Exact duplicate → skip, tell the user.
4. Otherwise → create a new entry.

### Step 3: Compile the entry

Use the matching template (in `1_Wiki/templates/`) and follow:

**Required frontmatter**:

```yaml
---
title: "[Entry Title]"
type: concept | entity | comparison | framework | resource
created: YYYY-MM-DD
source: "[full path of source file]"
confidence: high | medium | low
tags:
  - [type tag]
  - [topic tag]
  - para/resource
aliases:
  - [alias]
author: agent
---
```

**Body rules**:
- Use tables for structured info (comparisons, steps, categories).
- Cross-links only in the final `## See also` section, each with an English type label (8 types: apply/contrast/cause/example/part-of/background/related/prerequisite — see `2_Schema/TheSchema.md` §3). No label → no link.
- Stay concise; do not expand content that is not in the source.
- Keep core insights, key quotes and critical data from the source.
- Never add fabricated content.

**Naming**: see `2_Schema/naming.md` (concept: core term; comparison: `A vs B`; framework: core term; entity: subject name; resource: topic + list).

### Step 4: Update index.md

1. Read `1_Wiki/index.md`.
2. Add new entries to the quick-nav table under the matching type.
3. Update the statistics at the top.
4. Group logically when multiple entries were created.

### Step 5: Output the compile report

```
## Compile Complete

| Action | Detail |
|--------|--------|
| Source | original file path |
| New entries | X |
| Supplemented entries | X |
| Skipped (duplicate) | X |
| Ignored (non-wiki) | X |

### New entries
- [[entry1]]
- [[entry2]]

### Supplemented entries
- [[entry3]] — added XX content

### Next steps
- Suggested [[missing related concept]] (no source found this round)
- Links to complete: entry XX mentions YY but has no link
```

## Rules

1. **Never modify the original**: 0_Inbox/ files are never edited.
2. **No fabrication**: compile only what is in the source; no AI expansion.
3. **Label AI supplements**: use `> 💡 AI note: ...`.
4. **Links are earned, not assigned**: cross-links only in `## See also` with type labels; no label → no link; never create a link just to have one.
5. **Minimal change**: when supplementing an existing entry, only append; do not rewrite the whole entry.
6. **Date format**: always `YYYY-MM-DD`.

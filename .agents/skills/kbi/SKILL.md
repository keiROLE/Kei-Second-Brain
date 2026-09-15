---
name: kbi
description: Knowledge-base iteration analysis — scan the whole vault, find coverage gaps, unprocessed content, isolated entries, broken links and hallucinations, and output an iteration report with recommendations. Triggers on "/kbi", "knowledge base iteration", "health check" or "analyze the knowledge base".
---

> This skill is part of the Kei-Second-Brain ecosystem. System overview is in `README.md`.

# kbi — Knowledge-Base Iteration Analysis

## Trigger

User says "/kbi", "knowledge base iteration", "analyze the knowledge base", "health check", or similar.

## Role

You are the knowledge-base iteration analyst. Analyze the Obsidian vault comprehensively and find:

1. **Coverage gaps** — areas the user cares about but lacks systematic entries for
2. **Uncompiled content** — raw notes with knowledge value not yet extracted into wiki entries
3. **Wiki health issues** — broken links, hallucinations, structural violations, duplicate entries
4. **Graph weaknesses** — isolated entries, weak/fake links, under-linked areas, link-audit findings
5. **Actionable improvements** — recommendations that strengthen the user's knowledge and methods

## Input

- User profile (optional): `2_Schema/user-profile.md` if present — the reference for "what matters"
- Global config: `2_Schema/TheSchema.md`
- Wiki index: `1_Wiki/index.md`
- All raw notes (0_Inbox/ and other source folders)
- All wiki entries (1_Wiki/ subdirectories)

## Workflow

### Phase 1: Vault overview

1. List all .md files in 1_Wiki/ (excluding templates/ and index.md).
2. Group by type: concepts/, entities/, comparisons/, frameworks/, resources/.
3. Count entries per type.
4. Read `1_Wiki/index.md` for reference relationships.

### Phase 2: Coverage gap analysis

Against the user profile's "core domains" (or the user's stated focus areas if no profile file exists), check:

- How many entries does each domain have in 1_Wiki/?
- Which subtopics are clearly missing?
- Which capability/knowledge domains relevant to the user's goals have zero coverage?
- Do current exploration/experiment projects have supporting knowledge entries?

### Phase 3: Uncompiled content scan

Scan 0_Inbox/ and other source folders for valuable-but-uncompiled notes:

- Check whether each .md file is already referenced in `1_Wiki/index.md`.
- For unreferenced files, extract potential concepts, frameworks, resources.
- Pay attention to: quotes/methods in raw notes, lessons from weekly reviews, SOPs.

### Phase 4: Wiki health check

#### 4.1 Broken link detection

Traverse all wiki entries; check `[[xxx]]` links in:
1. The final `## See also` section
2. The body text (wiki-links)

For each link target, check whether a matching wiki file exists (exact title / aliases / filename). If not → broken link.

**Broken-link disposition** (instead of "just fix it"): classify each broken link with a decision-tree — break type (alias/rename typo, genuinely missing concept, forced unrelated link from compile, formatting error) + disposition (fix pointer / create entry / delete link / fix format). **Never "repair" a broken link by pointing it at a semantically close unrelated entry.**

#### 4.2 Source cross-check (completeness)

For each wiki entry, trace back to its source:

1. Get the "Source" column from `1_Wiki/index.md`.
2. Read the source file.
3. Compare item by item:
   - Source has it, wiki does not → MISSING (content loss)
   - Wiki has it, source does not → ERROR (possible AI hallucination)
   - Both have it, consistent → OK

#### 4.3 Structural compliance

| Check | Requirement |
|-------|-------------|
| title | present, double-quoted |
| type | present, matches directory |
| created | present, YYYY-MM-DD |
| tags | ≥ 3 (type + topic + PARA) |
| aliases | recommended when filename ≠ title |
| See also links | each with an English type label; unlabeled = to-label/weak |
| Body | matches the template's required sections |

#### 4.4 Duplicate detection

1. Entries with highly similar content (close titles, overlapping definitions).
2. Duplicate references in index.md.
3. aliases conflicting with existing titles.

### Phase 5: Graph analysis

#### 5.1 Connectivity

For each entry compute:
- **outgoing**: links to other entries (See also + body wiki-links)
- **incoming**: entries linking to it

#### 5.2 Problem classification

Low connectivity is **no longer automatically a problem** — an island may be an intentionally independent topic. Everything goes into a "confirm list" for human/AI judgment:

| Type | Condition | Nature | Question |
|------|-----------|--------|----------|
| **Island** | incoming == 0 and outgoing == 0 | 🟡 confirm | Intentionally independent? If not, what is its real missing link? |
| **Half-island** | incoming == 0 and outgoing <= 1 | 🟡 confirm | Should other entries reference it? |
| **Single-point** | incoming + outgoing <= 2 | 🟡 confirm | Does the single link hold? Does it need a second real link? |
| **Low density** | outgoing < 3 | 🟢 observe | No action unless a real relation exists |
| **Skeleton** | body wiki-links < 2 | 🟢 observe | No action unless a real relation exists |

#### 5.3 Semantic link suggestion (real links only)

**Core principle**: links are earned, not assigned. Shared tags / same directory / same source are **not** sufficient grounds for a link.

**Suggestion rules**:
1. **Body-mention principle**: entry A's body genuinely discusses entry B's concept (not as a wiki-link) → may suggest a link.
2. **Semantic verification (mandatory)**: for every candidate link, answer — "Is B an apply/contrast/cause/example/part-of/background of A? State the relationship in one sentence." **Drop any link you cannot articulate.**
3. **Reason required**: a "high confidence" link must carry a verifiable reason; unreasoned links cannot be high.
4. **Landing format**: confirmed links go into `## See also` with English type labels (8 types — see `2_Schema/TheSchema.md` §3).

**Suggested-output format** (Reason column mandatory):

```
| Entry A | Suggested link | Relationship | Reason (required) | Confidence |
|---------|----------------|--------------|-------------------|------------|
| [[A]] | [[B]] | apply | B is A applied to a specific scenario | high |
| [[A]] | [[C]] | ? | cannot articulate → drop | - |
```

### Phase 6: Output the iteration report

Write `3_KBI-log/YYYY-MM-DD-iteration-report.md`.

```yaml
---
title: "Knowledge Base Iteration Report YYYY-MM-DD"
type: iteration-report
created: YYYY-MM-DD
tags:
  - analysis
  - iteration
---
```

Report sections:
1. Vault overview (counts)
2. Coverage gaps (high/medium priority, each with: current state, why it matters, suggested entries)
3. Uncompiled content (file → potential type → suggested entry)
4. Wiki health:
   - 🔴 Broken links (disposition table)
   - 🟡 Missing content (entry → source → what is missing)
   - 🔴 Hallucinations (entry → content not in source → delete or label)
   - 🟢 Structural violations (optional fixes)
   - 🟠 Duplicates (merge suggestions)
   - 🟣 Weak-link list (link audit — unlabeled links, unclassifiable links)
5. Graph analysis (islands to confirm; semantic link suggestions with reasons)
6. Action items, prioritized:
   - P0 fix broken links · P1 delete/label hallucinations · P2 handle islands (only non-intentional) · P3 add second real links to single-point entries · P4 apply reasoned link suggestions · P5 supplement missing core content · P6 fix structural issues · P7 create entries for coverage gaps · P8 compile uncompiled content
7. One-sentence insight of the day

### Phase 7: Link audit (existing links, read-only)

Audit all existing `## See also` links (results merged into Phase 6 — no separate file):

1. Traverse all See also links (labeled = justified; unlabeled → "to-label" list).
2. Try to assign one of the 8 types to each:
   - Classifiable → real link (optionally label it)
   - Unclassifiable / strained → weak link, list under "candidates to remove"
3. **Read-only**: removal/modification happens only after user confirmation.

## Rules

- Report facts and recommendations; no empty praise.
- Every recommendation needs a concrete reason tied to the user's profile/goals.
- Priority ordering: things that directly affect goals first.
- If nothing significant found, still output a "no major changes" report.
- **Read-only**: iteration analysis reports problems and findings; it does not modify files unless the user explicitly asks for fixes.
- **Broken-link fixes go through the decision tree** (fix pointer / create entry / delete link / fix format); never fake-repair with a semantically close unrelated entry.
- **Links are earned, not assigned**: See also links carry type labels; no label → no link.

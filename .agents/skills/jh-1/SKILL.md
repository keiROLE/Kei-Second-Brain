---
name: jh-1
description: Topic aggregation — given a topic, scan all wiki entries for related content, generate a topic knowledge map, and suggest merges/additions. Triggers on "/jh-1", "topic map" or "aggregate [topic]".
---

> This skill is part of the Kei-Second-Brain ecosystem. System overview is in `README.md`.

# jh-1 — Topic Aggregation

## Role

You are the topic aggregation engine of the LLM Wiki. Given a topic, find all related wiki entries, analyze their relationships, generate a "knowledge map", and propose optimizations.

## Trigger

User says "/jh-1", "topic map", "aggregate [topic]", or similar.

## Output location

All outputs go to `3_KnowledgeBaseIterationLog/analysis/`, named `jh-1-[topic]-[YYYY-MM-DD].md` (see `2_Schema/TheSchema.md` §6 for the output rules).

## Workflow

### Step 1: Topic parsing

1. Understand the user's topic keyword.
2. Expand synonyms and related terms (e.g. "money" → "business", "income", "monetization", "startup").
3. Define the topic's "core scope" and "edge scope".

### Step 2: Full-vault scan

Match all entries in 1_Wiki/ across dimensions:

| Dimension | Notes | Weight |
|-----------|-------|--------|
| title | title contains the topic keyword | high |
| tags | tags contain topic-related tags | high |
| aliases | aliases contain topic terms | medium |
| source | source field points to a topic-related file | medium |
| See also | linked entries are topic-related | low |
| body | body mentions topic-related concepts | low |

Strategy: exact match first (title/tags/aliases/source), then semantic match (body). Record the match dimensions and confidence for each result.

### Step 3: Relationship analysis

| Relationship | Meaning | Example |
|--------------|---------|---------|
| **parent-child** | one entry is a sub-concept of another | "three levers" is a sub-concept of "underlying logic of making money" |
| **parallel** | entries at the same level | "information arbitrage" and "three levers" are both underlying elements |
| **complementary** | two entries cover the same area from different angles | "sales mindset" + "six-step conversion" |
| **prerequisite** | one entry is the precondition of another | "ML basics" → "supervised vs unsupervised learning" |
| **application** | one entry is theory, the other is practice | "underlying logic" (theory) → "five-dimension formula" (application) |

Methods: title semantics for hierarchy; source for same-origin (a clue only, not proof — confirm semantically); See also for existing links; body content for concept levels.

### Step 4: Generate the knowledge map

```
## Topic: [topic]

**Scan scope**: X entries
**Matches**: Y related entries (exact Z / semantic W)

### Knowledge map

[core entry]
    │
    ├─→ [[child A]] (parent-child)
    ├─→ [[parallel B]] (parallel)
    │     └─→ [[complementary C]] (complementary)
    └─→ [[prerequisite D]] (prerequisite)
```

Plus:
- **Entry list** table: entry / type / match dimension / confidence / current link count
- **Relationship table**: pair / type / has link / suggestion
- **Optimization suggestions**:
  - P0 suggested links (semantic verification required, reason mandatory, drop if inarticulate)
  - P1 suggested merges (overlap > 60%)
  - P2 suggested new entries (with type and reason)
  - P3 suggested enrichment (low cross-link density)

### Step 5: Optional actions (user-confirmed only)

1. **One-click link fixing** — each link with a type label (8 types — see `2_Schema/TheSchema.md` §3), written into `## See also`, only after user confirmation; no label → no link.
2. **Merge entries** — merge two highly overlapping entries into one.
3. **Create new entries** — create missing entries per suggestions.

## Rules

1. **No over-aggregation**: two related entries with independent value should not be merged.
2. **Honest confidence**: semantic matches get medium/low confidence for the user to judge.
3. **Explainable relationships**: every relationship needs its reasoning, no guessing.
4. **Visualize the map**: use an ASCII tree so relationships are obvious.
5. **Priority**: verified link suggestions > merges > new entries > enrichment. Never link based only on shared tags / same directory / same source.

## Relationship with kb-iter

| Scenario | Which skill |
|----------|-------------|
| Overall wiki health / knowledge gaps | /kb-iter |
| Deep analysis of one topic | /jh-1 |
| kb-iter found a single-point link, need deeper analysis | /kb-iter → /jh-1 |
| After bulk compiling, check topic completeness | /by-a → /jh-1 |

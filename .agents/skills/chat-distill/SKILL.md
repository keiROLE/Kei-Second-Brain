---
name: chat-distill
description: AI conversation distillation — filter agent conversation logs by value, then land them into the knowledge base (0_Inbox/chat-distill → 1_Wiki), following the link ecosystem rules (See also + 8 type labels, no fake links). Triggers on "/chat-distill", "distill conversations", "tidy up AI conversations".
---

> This skill is part of the Kei-Second-Brain ecosystem. System overview is in `README.md`.

# chat-distill — AI Conversation Distillation

## Role

A dedicated compile pipeline for **agent conversations**: Collect → Triage → Land → Compile → Link → Log. Difference from `/by-a` (vault-wide compile): this skill only processes conversation logs; entry, screening and landing are tailored to conversation data.

## Trigger

- User says "/chat-distill", "distill conversations", "tidy up AI conversations", "put the AI conversation into the knowledge base", etc.
- Weekly routine: recommended once a week, default to only the last 7 days of new sessions.

## Three principles (read first)

1. **Conversation is raw material, not knowledge.** Operational steps, debugging, back-and-forth corrections do not enter the knowledge base. Only conversations that yield a **reusable conclusion** (method / framework / decision basis / lesson learned / new knowledge) are worth distilling.
2. **Better few than many.** From 8-20 candidates per round, keep only 3-8. Knowledge-base health is maintained by "few and true".
3. **Links are earned, not assigned.** Never create a link to fill space; **a link that cannot carry a type label is not written** (link rules: `2_Schema/TheSchema.md` §3).

---

## Step 0: Collect — where the logs are, how to read them

Locations vary by AI client and environment. Configure yours:

| Agent | Typical location | Format |
|-------|------------------|--------|
| Claude Code | `~/.claude/projects/<project>/` | JSONL, one event per line |
| Codex | `~/.codex/sessions/YYYY/MM/DD/` | JSONL (payload: role/content, messages) |
| DoubaoWork / other agents | your agent runtime's session/workspace traces | JSONL (role/content) |
| Others | export from your client | varies |

**Action**:
1. Scan the configured log locations for sessions from the last 7 days.
2. For each session, extract: first user message (truncated), message count, file size, file path.
3. Produce a session list for triage.

**Session-list format** (one line per session):

```markdown
| # | agent | file (relative) | time | msgs | topic (first user message, ~80 chars) |
|---|-------|-----------------|------|------|----------------------------------------|
| 1 | claude-code | xxx.jsonl | 08-30 | 42 | Refactoring a script, comparing two approaches |
```

---

## Step 1: Triage — three gates

Run every candidate session through three questions; fail any gate → drop:

| Gate | Question | Pass criteria | Reject examples |
|------|----------|---------------|-----------------|
| ① Conclusion | Did this conversation produce a **reusable conclusion**? | Can state in one sentence: method / framework / decision basis / lesson / new knowledge | Only operational steps, code debugging, unrelated chat |
| ② Dedup | Does the knowledge base **already have** this conclusion? | No equivalent entry found in 1_Wiki/ (check title/aliases/concept terms) | Existing entry covers it; the conversation just repeats |
| ③ Level | Is it worth an **entry**, or just **supplement material**? | Standalone entry: concept/framework/comparison/resource; supplement: one paragraph for an existing entry | Mere logs, emotions, ad-hoc decisions |

**Triage output** (candidate list):

```markdown
| # | agent | session topic | conclusion in one sentence | suggested type | relation to existing entries |
|---|-------|---------------|----------------------------|----------------|------------------------------|
| 1 | claude-code | script refactor | "Pattern X is faster than Y" → reusable judgment | concept | new, no duplicate |
| 2 | doubao | resume discussion | supplement [[resume-wording-table]] | resource (supplement) | exists, supplement |
```

> Suggested: from 8-20 candidates per round, keep only 3-8.

---

## Step 2: Land — become raw material first

Write the **essence excerpts** (not the full log) of selected conversations as standard raw notes in `0_Inbox/chat-distill/`.

File naming: `YYYY-MM-DD-<agent>-<short-topic>.md`

Frontmatter template (**no `related` / no `links` fields** — deprecated):

```yaml
---
title: "Distilled: <topic>"
author: agent
created: YYYY-MM-DD
tags:
  - chat-distill
  - inbox/raw
processed: false
source_type: chat
source_agent: claude-code | codex | doubao | other
source_file: "<path to original log>"
source_time: YYYY-MM-DD
---
```

Body structure (only excerpts with incremental value):
- **Background**: what problem this conversation was solving (1-2 lines)
- **Conclusion/Method**: the reusable conclusion (core)
- **Quotes**: 1-3 key excerpts (for traceability)
- **My notes**: your judgment / follow-up plans

> Constraint: 0_Inbox is the raw material layer — write-only, discardable. Do not stuff non-selected conversations in here.

---

## Step 3: Compile — conversation → wiki entries

**Reuse the existing compile capability**: single entries via `/by-1`, batches via `/by-a`'s grouped-parallel approach. Conversation-specific additions:

1. **Type judgment as usual**: concept (new concept in the conversation) / framework (method/process produced) / comparison / resource (tool, checklist, template).
2. **Traceability as usual**: `source` = `0_Inbox/chat-distill/...md`; `confidence` self-rated on "does the conclusion come directly from your judgment + does it match the source conversation" (second-hand conclusions relayed in conversation → downrate one level).
3. **Conversation-specific hallucination risk**: AI "suggestions" in a conversation may be unverified by you → distinguish **adopted conclusions** from **AI proposals (unverified)**; the latter are labeled in the entry as `> 💡 AI proposal (unverified): ...`.
4. **De-AI-ify and condense**: do not copy conversation text verbatim; rewrite per entry template as "definition + key points + when to use + see also".

---

## Step 4: Link — the final link rules, real links only

- Cross-links **only in the final `## See also` section**, each with an English type label (8 types: apply/contrast/cause/example/part-of/background/related/prerequisite — `2_Schema/TheSchema.md` §3):

```
## See also
- [[barrier-to-entry-as-profit]] apply
- [[underlying-logic-of-making-money]] prerequisite
```

- **A link you cannot label is a suspected fake link — do not write it.** Never create a link just to have one.
- Body mentions of existing concepts may be wiki-linked, but forced linking is unnecessary.

**Output**: new entries + updated `1_Wiki/index.md` (statistics + quick nav).

---

## Step 5: Log & review

1. Per the `/by-a` compile report convention, write the compile report to `3_KnowledgeBaseIterationLog/YYYY-MM-DD-compile-report.md` with an extra "Conversation distillation stats" section:
   - Sessions scanned / candidates / selected / new entries / supplemented entries
   - Duplicates blocked by the dedup gate (a good sign — the knowledge base already covers them)
   - Which agents/scenarios **consistently** produce valuable conclusions → mark "worth following"
2. Per `/rec-1`, append one line to today's diary `## Log` (how many distilled, which entries created, outputs linked).

---

## Rules

- Conversation is raw material, not knowledge; better few than many; links are earned, not assigned.
- `0_Inbox/chat-distill` is write-only and discardable; only selected conversations land.
- Compiling must distinguish "adopted conclusions" from "AI proposals (unverified)" and label them.
- Every compile must update index.md **and** the compile report — neither may be skipped.

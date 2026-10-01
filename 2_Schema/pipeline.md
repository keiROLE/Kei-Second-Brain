---
title: "Pipeline — End-to-End Operating Procedure"
type: schema
updated: 2026-10-01
tags:
  - config
  - pipeline
---

# Pipeline: From Input to Output — End-to-End Operating Procedure

The system overview lives in `AGENTS.md` (single authoritative entry); **this document is what an AI (or a human) actually follows** — the concrete operating manual for the full pipeline.

The pipeline has seven stages. Every stage is **user-triggered** — nothing runs automatically.

```
① Capture → ② Review → ③ Compile → ④ Iterate → ⑤ Distill → ⑥ Plan → ⑦ Output
   acquire      weekly      AI extracts    health-check   AI chats     goals →      knowledge →
   material     reflection  knowledge      & link audit   → entries     task phases   new content
```

---

## ① Capture — acquire material

**Goal**: raw material lands in 0_Inbox/, classified by type.

| Input | Where it goes |
|-------|---------------|
| Video / audio from any platform | 0_Inbox/ (to be transcribed, or clip into clippings/) |
| Web clipping | `0_Inbox/clippings/` |
| AI conversation log | `0_Inbox/chat-distill/` |
| Daily note | `0_Inbox/diary/YYYY-MM-DD.md` |

Rules:
- Store first, organize later. No editing in 0_Inbox.
- Tag raw material `#inbox/raw`; leave `processed` unset or `false`. Use `processed: skip` for files that must **never** be compiled (passwords, fiction drafts).

### Transcription (audio/video → text)

1. Prefer official subtitles (platform-provided) when available.
2. Otherwise use a transcription tool (Whisper-class or commercial).
3. Proofread names, brands, products and technical terms against context.
4. For long content, transcribe in segments and merge; do not truncate.
5. Mark inaudible parts as `[inaudible 00:01:23]`; distinguish speakers when multiple.

Output: transcript file in `0_Inbox/` (or the appropriate subdirectory).

---

## ② Review — weekly reflection

**Goal**: the last complete week of diary notes becomes one concise weekly review.

Use `/wr-1` (usually Monday morning).

1. Confirm "today" from the system date; default target is the last **completed** Monday–Sunday.
2. Run the companion script first: `python .agents/skills/wr-1/review_status.py` — lists which diaries carry `weekly_reviewed` and which weeks are missing marks (the LLM does not read frontmatter itself).
3. Read the 7 diary notes (`0_Inbox/diary/YYYY-MM-DD.md`); extract key events, thoughts, quotes, methods, inputs, unfinished tasks.
4. Merge by day into daily entries; add a cross-week summary: key events, cognition & reflections, unresolved questions.
5. Write the output, named `MMDD-last-week-review.md` (MMDD = the Monday of the reviewed week), into `0_Inbox/weekly-review/`.
6. Mark each compiled diary with `weekly_reviewed: YYYY-MM-DD` via the script's `mark` command (append-only, never overwrite an existing value, never rewrite the diary body).

---

## ③ Compile — AI extracts knowledge units

**Goal**: raw material becomes structured entries in 1_Wiki/.

Use `/by-1` for a single document, `/by-a` for bulk.

Steps (by-a):
1. **Run the scanner first**: `python .agents/skills/by-a/find_uncompiled.py` — outputs the candidate list (already excludes `processed: skip`, entries already in index.md's Source column, and `processed: true`). The LLM groups and judges; it does not re-scan files.
2. For each file, extract knowledge units:
   - concepts → `1_Wiki/concepts/`
   - entities → `1_Wiki/entities/`
   - comparisons → `1_Wiki/comparisons/`
   - frameworks → `1_Wiki/frameworks/`
   - resources → `1_Wiki/resources/`
3. Use the matching template in `1_Wiki/templates/`.
4. Add a `## Source` section (mandatory traceability).
5. Add a `## See also` section; every link carries one of the 8 type labels. No label → no link.
6. Update `1_Wiki/index.md`.
7. Mark the source file `processed: true` **in the same pass** (via the script's `mark` command — never manually).
8. Write the compile report to `3_KBI-log/YYYY-MM-DD-compile-report.md`.

Quality red lines apply throughout: no fabrication, `confidence` marks uncertainty, AI supplements labeled `> 💡 AI note:`.

---

## ④ Iterate — health check & link audit

**Goal**: keep the knowledge base healthy and honest.

Use `/kbi`.

1. **Run the audit script first**: `python .agents/skills/kbi/audit_links.py` — outputs the broken-link list, island/half-island stats, incoming/outgoing connectivity and entry counts. The LLM makes semantic judgments on the script output instead of parsing links itself.
2. Scan scope (on top of the script output):
   - Coverage gaps (topics missing)
   - Unprocessed files
   - Broken-link disposition (decision tree: fix pointer / create entry / delete link / fix format — never fake-repair with a semantically close entry)
   - Island entries (confirm list, not auto-problem)
   - Hallucination candidates (unsourced claims)
   - Link audit (entries without type labels)
3. Output: `3_KBI-log/YYYY-MM-DD-iteration-report.md` — **read-only recommendations**. Fixes are applied only after user confirmation.

---

## ⑤ Distill — AI conversations become entries

**Goal**: valuable AI conversations are filtered into the knowledge base instead of being lost.

Use `/chat-distill`.

1. Collect the conversation log (raw log goes to `0_Inbox/chat-distill/` with traceability frontmatter: `source_type`, `source_agent`, `source_file`, `source_time`).
2. Pass it through the 3-gate filter (worth keeping? genuinely new? compilable?).
3. Store the distilled note; compile knowledge units into 1_Wiki/ with the normal compile rules (Source section, typed `## See also` links).
4. Mark the raw log `processed: true`.

---

## ⑥ Plan — goals become task phases

**Goal**: long-term goals are broken into current task phases.

Use `/chiselplan`.

1. Read the goal (or the current plan file) and the user's stated timeline.
2. Break it into ordered task phases; each phase has a clear outcome.
3. Write the plan to the plan file (e.g. `plan.md`, or a dedicated plan file the skill manages; chiselplan can create its own skill for a repeated loop).
4. Review the phase state regularly (phase review): what finished, what changed, what moves next.

---

## ⑦ Output — knowledge back into content

**Goal**: compiled knowledge becomes new content in `4_Outputs/` (the Output layer).

Use `/blog-1` to generate articles / project pages / shares into `4_Outputs/`, or adapt entries into video scripts / posts manually or with an AI client of your choice. Output-layer rules and naming: `2_Schema/TheSchema.md` §1 (4_Outputs), `2_Schema/naming.md`.

Rules:
- Output derives from entries; entries remain the source of truth.
- No fabrication: anything not backed by an entry must be marked as inference.

---

## Quality red lines (apply to every stage)

- 0_Inbox/ is read-only (only frontmatter markers are appended).
- No fabrication; mark uncertainty with `confidence`.
- Numbers / dates / facts are traceable: "verified" vs "claimed by one party".
- AI supplements labeled `> 💡 AI note:`.
- AI-compiled content uses `author: agent`.

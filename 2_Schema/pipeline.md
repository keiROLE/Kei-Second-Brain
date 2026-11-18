---
title: "Pipeline — End-to-End Operating Procedure"
type: schema
updated: 2026-11-18
tags:
  - config
  - pipeline
---

# Pipeline: From Input to Output — End-to-End Operating Procedure

The system overview lives in `AGENTS.md` (single authoritative entry); **this document is what an AI (or a human) actually follows** — the concrete operating manual for the full pipeline.

The pipeline has seven stages. Start it on request. `/rec-1` can also append a log block after an AI task produces a recordable outcome.

```
① Record → ② Review → ③ Compile → ④ Maintain → ⑤ Distill → ⑥ Plan → ⑦ Output
```

**What lands in 0_Inbox/ (intake):**

| Input | Where it goes |
|-------|---------------|
| Daily note | `0_Inbox/diary/YYYY-MM-DD.md` |
| Web clipping | `0_Inbox/clippings/` |
| AI conversation log | `0_Inbox/chat-distill/` |
| Video / audio | `0_Inbox/` (transcribe first, or clip into `clippings/`) |

Intake rules: store first, organize later; no editing inside 0_Inbox; tag raw material `#inbox/raw`; leave `processed` unset or `false`; use `processed: skip` for files that must **never** be compiled (passwords, fiction drafts).

### Transcription (audio/video → text)

1. Prefer official platform subtitles when available.
2. Otherwise transcribe with a Whisper-class or commercial tool.
3. Proofread names, brands, products and technical terms against context.
4. For long content, transcribe in segments and merge; do not truncate.
5. Mark inaudible parts `[inaudible 00:01:23]`; distinguish speakers when multiple.

---

## ① Record — daily note capture

**Goal**: scattered input enters 0_Inbox/ — in, never edited in place.

| Item | Detail |
|------|--------|
| Trigger | Daily diary; say "log this" at task wrap-up |
| Skill | `/rec-1` (minimal append) |
| Output | `0_Inbox/diary/YYYY-MM-DD.md` — appended under the `# Log:` section; append-only, never rewrite |
| Rule | Use the diary system's scoped append rules for new log blocks. Preserve the existing text and use the topic-tag registry. |

## ② Review — weekly review

**Goal**: a week of diary notes compiled into a scannable weekly review.

| Item | Detail |
|------|--------|
| Trigger | "weekly review" / "last week's review" (usually every Monday) |
| Skill | `/wr-1` |
| Input | The 7 diary notes of the last full week (Mon–Sun) |
| Output | `0_Inbox/weekly-review/MMDD-last-week-review.md` |
| Writeback | Mark reviewed diaries `weekly_reviewed: YYYY-MM-DD`; skip notes already marked |

Workflow:
1. Confirm "today" from the system date; default target is the last **completed** Monday–Sunday.
2. **Run the deterministic script first**: `python .agents/skills/wr-1/review_status.py` — lists which diaries carry `weekly_reviewed` and which weeks are missing marks (the LLM does not read frontmatter itself).
3. Read the 7 diary notes; extract key events, thoughts, quotes, methods, inputs, unfinished tasks.
4. Merge by day into daily entries; add a cross-week summary: key events, cognition & reflections, unresolved questions.
5. Write the output, named `MMDD-last-week-review.md` (MMDD = the Monday of the reviewed week), into `0_Inbox/weekly-review/`.
6. Mark each compiled diary with `weekly_reviewed: YYYY-MM-DD` via the script's `mark` command (append-only, never overwrite an existing value, never rewrite the diary body).

---

## ③ Compile — AI extracts knowledge units

**Goal**: raw material becomes structured entries in 1_Wiki/ (the core step).

| Item | Detail |
|------|--------|
| Trigger | "compile this" (single) / "compile all" (bulk) |
| Skill | `/by-1` (single) / `/by-a` (bulk; runs the deterministic uncompiled-file scan first) |
| Scan scope | `processed: false` or missing the field. Skip today's diary, `processed: skip`, and sources with existing compiled entries. |
| Output | The five entry types in `1_Wiki/` + `index.md` updated |
| Report | `3_KBI-log/YYYY-MM-DD-compile-report.md` (stats / entry details / skip categories) |
| Writeback | Original file `processed: true`; body unchanged; `skip` files are never written back |

Steps (by-a):
1. **Run the scanner first**: `python .agents/skills/by-a/find_uncompiled.py`. It honors `processed: skip` and `processed: true` and checks the index and entry provenance. Hold back today's diary for the user's local date if it differs from the machine date.
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

Quality red lines apply throughout: no fabrication (`confidence: low` when unsure), AI supplements labeled `> 💡 AI note:`, numbers/dates/facts traceable, `author: agent`, links carry the 8 type labels (see TheSchema §3).

## ④ Maintain — health check & link audit

**Goal**: keep the knowledge base honest — health check, gap analysis, link audit.

| Item | Detail |
|------|--------|
| Trigger | "iterate the KB" / "health check" |
| Skill | `/kbi` for the audit, `/kbi repair` for verified low-risk fixes after the audit |
| Checks | coverage gaps / unprocessed files / broken links / hallucination candidates / island entries / link audit |
| Output | `3_KBI-log/YYYY-MM-DD-iteration-report.md` with findings and any applied repairs |

Workflow:
1. **Run the audit script first**: `python .agents/skills/kbi/audit_links.py` — outputs the broken-link list, island/half-island stats, incoming/outgoing connectivity and entry counts. The LLM makes semantic judgments on the script output instead of parsing links itself.
2. Scan scope (on top of the script output):
   - Coverage gaps (topics missing)
   - Unprocessed files
   - Broken-link disposition (decision tree: fix pointer / create entry / delete link / fix format — never fake-repair with a semantically close entry)
   - Island entries (confirm list, not auto-problem)
   - Hallucination candidates (unsourced claims)
   - Link audit (entries without type labels)
3. In repair mode, archive affected originals, apply only the verified fixes allowed by the KBI skill, and rerun the checks. Record applied fixes separately from proposals for individual review.
4. Write `3_KBI-log/YYYY-MM-DD-iteration-report.md`.

## ⑤ Distill — AI conversations into the KB

**Goal**: AI conversations (any client) are filtered into the knowledge base instead of being lost.

| Item | Detail |
|------|--------|
| Trigger | "distill conversations" / "tidy AI chats" |
| Skill | `/chat-distill` |
| Flow | collect conversation logs → three-gate filter → land in `0_Inbox/chat-distill/` → compile → link |
| Report | The compile report appends a "chat-distill stats" section |

Workflow:
1. Collect the conversation log (raw log goes to `0_Inbox/chat-distill/` with traceability frontmatter: `source_type`, `source_agent`, `source_file`, `source_time`).
2. Pass it through the 3-gate filter (worth keeping? genuinely new? compilable?).
3. Store the distilled note; compile knowledge units into 1_Wiki/ with the normal compile rules (Source section, typed `## See also` links).
4. Mark the raw log `processed: true`.

---

## ⑥ Plan — goal breakdown and phase review

**Goal**: break a goal into ordered phases and review progress against the current phase.

| Item | Detail |
|------|--------|
| Trigger | "re-plan" or "phase review" |
| Skill | `/chiselplan` for a selected plan under `2_Schema/chiselplan/` |
| Output | A new or updated plan in `2_Schema/chiselplan/` |

Workflow:
1. Read the goal (or the current plan file) and the user's stated timeline.
2. Break it into ordered task phases; each phase has a clear outcome.
3. Write the selected plan file.
4. Review the phase state regularly (phase review): what finished, what changed, what moves next.

## ⑦ Output — knowledge back into content

**Goal**: compiled knowledge becomes new content — articles, scripts, shares.

| Item | Detail |
|------|--------|
| Trigger | Per blog / content needs |
| Skill | `/blog-1` (articles / project pages / shares; auto frontmatter + English slug) |
| Output | `4_Outputs/` — also where `/by-1` single compiles and `/jh-1` topic maps land |

Rules:
- Output derives from entries; entries remain the source of truth.
- No fabrication: anything not backed by an entry must be marked as inference.

## Optional active recall

Use `/kbr` after compilation to review important, overdue, and new concepts. The skill reads `1_Wiki/` by default. It keeps scores and history in local state and adds a `recall` tag to an existing tags list on the first recorded review.

---

## Quality red lines (apply to every stage)

- Compilation preserves original inbox text and may write processing markers. Diary logging follows the append rules in `2_Schema/diary-system.md`.
- No fabrication; mark uncertainty with `confidence`.
- Numbers / dates / facts are traceable: "verified" vs "claimed by one party".
- AI supplements labeled `> 💡 AI note:`.
- AI-compiled content uses `author: agent`.

> `/wr-1` produces the weekly review. `/kbi` reports findings and applies verified low-risk fixes only in requested repair mode.

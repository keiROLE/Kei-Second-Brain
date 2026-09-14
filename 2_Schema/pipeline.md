---
title: "Pipeline — End-to-End Operating Procedure"
type: schema
updated: 2026-09-15
tags:
  - config
  - pipeline
---

# Pipeline: From Input to Output — End-to-End Operating Procedure

This is the concrete operating manual for the full pipeline. The README gives a one-paragraph overview; **this document is what an AI (or a human) actually follows**.

The pipeline has five stages. Every stage is **user-triggered** — nothing runs automatically.

```
① Capture → ② Transcribe → ③ Compile → ④ Maintain → ⑤ Output
   acquire      audio→text     AI extracts    health-check   knowledge →
   material                    knowledge      & link audit   new content
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
- Tag raw material `#inbox/raw`; leave `processed` unset or `false`.

---

## ② Transcribe — audio/video to text

**Goal**: spoken content becomes a text transcript in 0_Inbox.

Steps:
1. Prefer official subtitles (platform-provided) when available.
2. Otherwise use a transcription tool (Whisper-class or commercial).
3. Proofread names, brands, products and technical terms against context.
4. For long content, transcribe in segments and merge; do not truncate.
5. Mark inaudible parts as `[inaudible 00:01:23]`; distinguish speakers when multiple.

Output: transcript file in `0_Inbox/` (or the appropriate subdirectory).

---

## ③ Compile — AI extracts knowledge units

**Goal**: raw material becomes structured entries in 1_Wiki/.

Use `/by-1` for a single document, `/by-a` for bulk.

Steps (by-a):
1. Scan 0_Inbox/ for files with `processed: false` **or missing the `processed` field**.
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
7. Mark the source file `processed: true` (or move to `1_Wiki/archive/`).
8. Write the compile report to `3_KnowledgeBaseIterationLog/YYYY-MM-DD-compile-report.md`.

Quality red lines apply throughout: no fabrication, `confidence` marks uncertainty, AI supplements labeled `> 💡 AI note:`.

---

## ④ Maintain — health check & link audit

**Goal**: keep the knowledge base healthy and honest.

Use `/kb-iter`.

Scope of the scan:
- Coverage gaps (topics missing)
- Unprocessed files
- Broken links
- Island entries (no inbound links)
- Hallucination candidates (unsourced claims)
- Link audit (entries without type labels)

Output: `3_KnowledgeBaseIterationLog/YYYY-MM-DD-iteration-report.md` — **read-only recommendations**. Fixes are applied only after user confirmation.

---

## ⑤ Output — knowledge back into content

**Goal**: compiled knowledge becomes new content in `4_outputs/` (the Output layer).

Use `/blog-1` to generate articles / project pages / shares into `4_outputs/`, or adapt entries into video scripts / posts manually or with an AI client of your choice. Output-layer rules and naming: `2_Schema/TheSchema.md` §1 (4_outputs), `2_Schema/naming.md`.

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

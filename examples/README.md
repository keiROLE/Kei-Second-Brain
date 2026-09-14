# Sample Knowledge Base — Xiaojian Guo Studio

> **Fictional content disclaimer**: This sample knowledge base is entirely fictional and created for demonstration. It is not related to any real account or person. 示例内容全部为虚构演示，与任何真实账号无关。

This folder is a complete, runnable example of the Kei-Second-Brain system — a small Obsidian vault that shows how one person (here: a fictional DIY-PC seller and self-media creator, "Xiaojian Guo") runs the full pipeline: **input → compile → maintain → output**.

## How the sample maps to the pipeline

| Pipeline stage | Where in this sample |
|----------------|----------------------|
| ① Input (capture) | `0_Inbox/` — diary notes, a weekly review, a distilled AI conversation, a web clipping |
| ② Transcribe | (implied — the diary mentions watching reviews; transcripts would land in `0_Inbox/` too) |
| ③ Compile | `1_Wiki/` — 8 entries (concept/entity/comparison/framework/resource) compiled from `0_Inbox/` |
| ④ Maintain | `3_KnowledgeBaseIterationLog/2026-09-13-iteration-report.md` — health check + link audit |
| ⑤ Output | `output-sample.md` — an article compiled from the wiki entries |

## Suggested reading order

1. `README.md` (repo root) — what the system is and how to set up your own
2. `2_Schema/TheSchema.md` — the rules that govern this vault
3. This folder, in order:
   - `0_Inbox/diary/2026-09-10.md` — raw material, unprocessed
   - `3_KnowledgeBaseIterationLog/2026-09-13-compile-report.md` — what /by-a produced
   - `1_Wiki/` — the compiled entries
   - `3_KnowledgeBaseIterationLog/2026-09-13-iteration-report.md` — what /kb-iter found
   - `output-sample.md` — the output article

## The loop, in one paragraph

A customer question appears in the diary (input). The compile skill turns it into a wiki entry (compile). The iteration skill checks the vault and suggests what is missing (maintain). A video script or article pulls from the entries (output). Next week's diary records what that content brought back — and the loop runs again.

> All entries are in English because the system's configuration layer is English. The Chinese version of this README explains the same structure for Chinese readers.

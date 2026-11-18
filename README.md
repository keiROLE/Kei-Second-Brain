# Kei-Second-Brain

**An AI-compiled second brain.** A complete, open methodology for running a personal knowledge base where **AI compiles, maintains and outputs** — not just stores.

This repository includes a documented architecture, 10 reusable AI skills, and a sample knowledge base that demonstrates the pipeline.

> Chinese version: [README.zh.md](README.zh.md)（中文版，以英文版为准）

---

## What this is

Kei-Second-Brain is a personal knowledge-base methodology turned into a reusable system. The core idea:

> **Knowledge is not stored — it is compiled.**

Raw material (diary notes, clippings, AI conversations, transcripts) flows into an inbox. An AI agent compiles it into structured knowledge entries. A health-check pass keeps the vault honest. And the compiled knowledge feeds back into new content — articles, video scripts, posts.

The repo contains three things:

| Part | Location | What it is |
|------|----------|------------|
| **The system** | `2_Schema/` | The rules: architecture, frontmatter spec, naming, link rules, pipeline manual, diary system, AI working memory |
| **The skills** | `.agents/skills/` | 10 AI skills for compilation, maintenance, recall, planning, and related tasks |
| **The example** | `0_Inbox/` `1_Wiki/` `3_KBI-log/` `4_Outputs/` | A sample vault with five bilingual Wiki topics drawn from a monitor-buying transcript |

## How it differs from other methods

| Method | What it gives you | What this system adds |
|--------|-------------------|-----------------------|
| **PARA** | A classification skeleton (Projects / Areas / Resources / Archive) — this system **borrows its tag system**; most entries carry PARA tags | PARA only says *where things go*. Kei-Second-Brain adds an **AI compile layer** (raw material becomes knowledge entries automatically), a **maintain layer** (health checks, link audits, hallucination detection) and an **output layer** (knowledge feeds back into content). |
| **Zettelkasten** | Atomic notes linked into a web of thought — this system **borrows the linking idea** (typed `## See also` links) | ZK is handwritten. Here entries are **compiled by AI**, with quality red lines (no fabrication, source traceability, confidence levels) to prevent hallucination. |

**In one sentence**: PARA provides the skeleton, Zettelkasten provides the linking idea, Kei-Second-Brain provides the **AI compile pipeline + active maintenance + knowledge-backed output** — the three things that make a knowledge base actually grow.

## Prerequisites

To open the vault and use its skills:

1. **Obsidian** — the vault runs in Obsidian (free). Any recent version works.
2. **An AI client that supports custom skills** — for example, Claude Code or another agent that can read Markdown instructions and operate on files. Each skill starts with a `SKILL.md`.

Install Python 3.9 or newer to run the bundled scripts. Active recall additionally uses PyYAML (`python -m pip install PyYAML`).

## Architecture

```
0_Inbox/                             1_Wiki/                            2_Schema/
Raw material layer (read-only)       Knowledge compilation layer        Configuration layer
diary/  weekly-review/               concepts/  entities/               TheSchema (rules)
chat-distill/  clippings/            comparisons/  frameworks/          AGENTS (AI behavior)
                                      resources/  index.md              frontmatter/naming
                                                                        pipeline (operating manual)
                                                                        diary-system (diary spec)
                                                                        memory (AI working memory)

3_KBI-log/
Iteration layer
compile reports / iteration reports / link audits

4_Outputs/
Output layer
articles, scripts, posts
```

| Layer | Role | Who writes |
|-------|------|------------|
| `0_Inbox/` | Raw material — source of truth | You (append-only) |
| `1_Wiki/` | Compiled knowledge entries | AI (via skills) |
| `2_Schema/` | The rules the vault runs on | You + AI |
| `3_KBI-log/` | Reports: compiles, health checks, audits | AI |
| `4_Outputs/` | Content compiled from entries | AI (from wiki) |

## The pipeline (one paragraph)

Video transcripts, web clippings, AI conversations, and daily notes land in `0_Inbox/`. `/by-1` and `/by-a` compile them into sourced entries in `1_Wiki/`. `/kbi` reports vault issues, and `/kbi repair` applies verified low-risk fixes on request. `/kbr` helps you recall what you learned. `/blog-1` turns entries into drafts. See the full operating manual in `2_Schema/pipeline.md`.

## A real example — capture → compile

The sample vault uses a real capture-to-compile example:

1. **Capture** — the author's own video transcript about choosing a monitor was clipped into `0_Inbox/clippings/xiaojian-guo-monitor-episode.md`: real input, kept verbatim.
2. **Compile** — `/by-1` turned it into a typed entry: `1_Wiki/frameworks/monitor-selection-guide.md`.

The same transcript supports the concept, entity, comparison, and checklist examples. See [the Wiki index](1_Wiki/index.md) for both languages and their source links.

The whole loop — one person, from a video to a published article, every skill used — is told as a story in **[WORKFLOW.md](WORKFLOW.md)**.

## Quick start

### Option A — explore the example first (recommended)

```bash
git clone https://github.com/keiROLE/Kei-Second-Brain.git
# open this folder in Obsidian ("Open folder as vault")
# browse 0_Inbox/ and 1_Wiki/ — start with the two "real example" files listed above
```

Start with `1_Wiki/index.md` to browse the five entry types and trace them back to their source. The other folders show sample inputs, rules, reports, and outputs.

### Option B — let an AI build your own

**You can hand this README to any AI assistant and ask it to set up the vault for you.** The AI will:

1. Create the five top-level directories (`0_Inbox/`, `1_Wiki/`, `2_Schema/`, `3_KBI-log/`, `4_Outputs/`) and their subdirectories.
2. Ask you to copy `2_Schema/` (rules) and `.agents/skills/` (skills) from this repo.
3. Walk you through your first cycle: write a diary note → run `/by-1` on it → see the compiled entry.

### Option C — build from scratch manually

1. New Obsidian vault.
2. Copy `2_Schema/` and `.agents/skills/` from this repo.
3. Read `2_Schema/TheSchema.md` (the rules) and `2_Schema/pipeline.md` (the operating manual).
4. Start writing raw notes in `0_Inbox/`, then trigger `/by-a` to compile them.

## Repository map

| Path | What |
|------|------|
| `AGENTS.md` | Single authoritative entry: directory conventions, authoritative skill inventory, operating rules, quick commands |
| `2_Schema/TheSchema.md` | Architecture, tags, 8 link types, quality red lines, workflows |
| `2_Schema/frontmatter.md` | Frontmatter field spec |
| `2_Schema/naming.md` | Naming + PARA classification |
| `2_Schema/pipeline.md` | End-to-end operating manual (input → output) |
| `2_Schema/diary-system.md` | Diary system spec (diary template, weekly-review loop) |
| `2_Schema/memory/` | AI working-memory module — per-domain status snapshots (see its README.md) |
| `.agents/skills/` | The 10 skills listed in [AGENTS.md](AGENTS.md#project-skills) |
| `WORKFLOW.md` | The whole system as a story — one person, one loop, every skill used |
| `0_Inbox/clippings/xiaojian-guo-monitor-episode.md` | Real clipped material (the example input) |
| `1_Wiki/frameworks/monitor-selection-guide.md` | The entry it was compiled into (the example output) |
| `4_Outputs/` | Output-layer format examples (articles compiled from entries) |

## Support & maintenance boundaries

- This is a **personal methodology shared in public — not a community project**.
- Issues are welcome: ask questions, report problems.
- **No promise of regular updates**; major versions ship irregularly as the author's own vault evolves.
- Pull requests are merged after discussion; large unrequested changes are not accepted.
- The monitor entries use the included transcript. The workflow story is fictional and illustrates how to run the system.

## License

**CC BY-NC 4.0** (Attribution-NonCommercial 4.0 International).

You are free to share and adapt, under the terms: attribution, and non-commercial use only. Full legal code: <https://creativecommons.org/licenses/by-nc/4.0/legalcode>. See [LICENSE](LICENSE).

---

*Built by Kei — AI-compiled knowledge, for people who want their notes to think back.*

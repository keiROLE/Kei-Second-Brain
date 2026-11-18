---
name: kbr
description: Active recall for the wiki. Draw important, overdue, and new concepts, quiz one at a time, and record recall scores locally. Triggers on "/kbr", "recall a batch", or "review my knowledge".
---

# kbr — Active Recall

Use this skill to recall wiki concepts from memory. The default round contains five concepts. Use the user's language for questions and feedback.

## Start a round

Run commands from the vault root with Python 3.9 or later. Install PyYAML with `python -m pip install PyYAML` if it is missing.

1. Run `python -X utf8 .agents/skills/kbr/scripts/index_kb.py --quiet` at the start of a round. It indexes the wiki without editing it. This picks up added, moved, and edited notes.
2. Run `python -X utf8 .agents/skills/kbr/scripts/pick.py --next --json`. The response gives the concept's `id`, `title`, `path` (relative to the configured wiki directory), `reason`, and the number of items `remaining` in the round. A `null` result means there are no eligible concepts.
3. Ask one question, wait for the answer, then score and record before requesting the next item. Repeating `--next` before recording returns the current item. After recording the item with `remaining: 0`, finish the round.

The picker combines three pools: low recall weighted by importance, longest time since review, and concepts never reviewed. A previously reviewed concept must meet the minimum interval in every pool, including fallback. When a pool is short, eligible new and older concepts fill the remaining places. Pending items from a previous day expire automatically.

## Ask, score, record

1. Read the indexed wiki note. Give its title and a single cue about the core idea. Use the key-insight block, a table dimension, or the introduction for context. Save the answer until the user has tried.
2. Accept a user-supplied recall score (0–100). Otherwise score against the actual note:

   | Score | Standard |
   |---|---|
   | 90–100 | Core ideas complete, with accurate details or examples |
   | 70–89 | Framework correct, with minor omissions |
   | 50–69 | Around half recalled or a substantive misunderstanding |
   | 30–49 | A few fragments without the underlying structure |
   | 0–29 | Little recalled or a clear misconception |

3. Below the configured threshold (default 60), explain the concept in three to six brief points and link the source note. At or above the threshold, give one sentence on any gap.
4. Ask for importance (0–100). The previous value is retained when the user leaves it blank. New concepts default to 50.
5. Run `python -X utf8 .agents/skills/kbr/scripts/record.py --concept <id> --score <score> [--importance <importance>]`. Omit the optional flag to retain the prior importance. On a first review the script adds `recall` to a standard tags list while preserving the rest of the note. `--dry-run` previews the record and tag. Repeating the most recent review with the same date, score, and importance is safe.
6. Give a short summary of scores grouped by recall quality. Run `python -X utf8 .agents/skills/kbr/scripts/stats.py --top 5` to see priorities and coverage.

## Local configuration

`config.json` holds public defaults. Put personal settings in `config.local.json` next to it. The local file, and the default `state/` directory holding the index, queue, scores, and review history, are ignored by Git. A custom state directory should be outside versioned paths.

- `kb_path` is relative to the vault root (default `1_Wiki`). `state_dir` is relative to the skill directory. Absolute overrides are supported. Use a separate state directory for each wiki.
- `exclude_dirs`, `exclude_files` and `exclude_patterns` control what the indexer reads. Patterns are case-insensitive substrings of filenames.
- `batch_size` defaults to 5, `recall_threshold` to 60, and `min_interval_days` to 2.
- `pool_ratios` has three keys: `dredge`, `coverage`, and `new`. Default weights are 60/25/15. Keep all three keys when overriding it.

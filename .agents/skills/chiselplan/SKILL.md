---
name: chiselplan
description: Break a goal into a phased plan under 2_Schema/chiselplan/, or review an active phase. Triggers on "/chiselplan", "re-plan", "phase review", and "project kickoff".
---

> This skill is part of the Kei-Second-Brain ecosystem. The authoritative system entry is `AGENTS.md` (skill inventory + operating rules); `README.md` is the project showcase for GitHub visitors.

# chiselplan — Planning / Phase Review (generic)

This skill is a **generic project planning tool**; it is not bound to any specific project. Use it for the kickoff, restructure and phase review of any goal.

When called, the user may add instructions (if none and intent is unclear, ask which mode first).

## Mode 1: Plan (project kickoff / goal restructure)

Create or update the selected file under `2_Schema/chiselplan/`. Default to `plan.md` when starting a new plan. Use the requested filename when the user supplies one. Structure:

```
# <Project Name> Plan (plan)

> Current phase: Phase N · Name

## Final goal (dynamic, not locked by month)
1. ...
2. ...

## Task phases (in dependency order, no fixed duration per phase)
### Phase 1 · Name
- [ ] Subtask (each delivers a verifiable complete outcome)
### Phase 2 · Name
- [ ] ...
```

Rules:
- The final goal only states the "direction to push now"; do not lock monthly KPIs; mark it "dynamic".
- Task phases follow dependency order (foundation → run-through → deepen → sprint → wrap-up); no dates, no weeks.
- 3-6 subtasks per phase; each is a vertical slice (a verifiable complete outcome).
- A one-line pointer at the top: `> Current phase: Phase N · Name`.

## Mode 2: Phase review (forced mid-way)

- Read the plan file and recent diary notes in `0_Inbox/diary/`; judge whether the current phase is done.
- Done → mark the phase title ✅ + advance the pointer + adjust the final goal.
- Not done → explicitly state which subtasks are incomplete; do not advance.

## Input references

Planning may reference: recent diary notes in `0_Inbox/diary/`, the user's stated goal.

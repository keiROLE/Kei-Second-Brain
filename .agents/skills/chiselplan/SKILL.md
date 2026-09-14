---
name: chiselplan
description: Project planning / restart — break a goal into "final goal + task phases" written into a plan file under 2_Schema/chiselplan/, or force a mid-way phase review. Triggers on "/chiselplan", "re-plan", "phase review", "project kickoff". This skill can create a companion "daily loop" skill (default name plan-1) — see "Can create skills" below.
---

> This skill is part of the Kei-Second-Brain ecosystem. System overview is in `README.md`.

# chiselplan — Planning / Phase Review (generic)

This skill is a **generic project planning tool**; it is not bound to any specific project. Use it for the kickoff, restructure and phase review of any goal.

When called, the user may add instructions (if none and intent is unclear, ask which mode first).

## Mode 1: Plan (project kickoff / goal restructure)

Create/update a plan file: under `2_Schema/chiselplan/` (default `plan.md`; the user may specify a name, e.g. `plan_2.md`). Structure:

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

## Can create skills (default name plan-1)

This skill can create a companion **"daily loop" skill** for a project, default name **plan-1** (append a suffix if the name conflicts).

The created skill's **purpose**:
- Each day, review yesterday's diary (tasks done / unfinished carried over)
- Judge whether the current phase of the plan file is done (if done, run the phase review automatically)
- Roll 3-5 concrete tasks for today from the current phase into today's diary `# PLAN` section
- Mark task ownership (AI can do independently / depends on user input / must be done by the user)

**When to create**: when the project enters execution and needs daily rolling progress. After planning, if the user needs a daily loop, proactively say: "This skill can create a companion daily-loop skill (default name plan-1) that reviews yesterday, judges whether the phase is done, and rolls today's tasks. Want me to create it now?"

## Boundary with plan-1

| | chiselplan | plan-1 (daily loop) |
|---|---|---|
| Frequency | low | high |
| When | kickoff, restructure, phase switch | every day |
| Duty | plan / phase review | review yesterday + roll today's tasks |

chiselplan sets the direction and judges phases; plan-1 pushes things forward daily. They work together; neither replaces the other.

## Input references

Planning may reference: recent diary notes in `0_Inbox/diary/`, the user's stated goal.

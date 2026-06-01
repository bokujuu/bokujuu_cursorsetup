---
name: ralph-loop
description: "Use when planning or running long-running, multi-task work; when the user mentions PRD, task list completion, or autonomous agent loops. Describes the Ralph pattern: run the agent repeatedly until all PRD items are complete, with fresh context per iteration and state in git and progress.txt."
disable-model-invocation: false
metadata:
  version: 1.0.0
  source: "https://nyosegawa.github.io/posts/claude-code-verify-command/"
  note: "Content aligned with the article 'Agentワークフローで人間がボトルネックにならないためのSkill設計' (逆瀬川). Ralph loop = outer loop; use with anti-human-bottleneck (inner)."
---

# Ralph Loop

*This skill is derived from and aligned with the article [Agentワークフローで人間がボトルネックにならないためのSkill設計](https://nyosegawa.github.io/posts/claude-code-verify-command/) (逆瀬川).*

Ralph is an **autonomous AI agent loop** that runs the agent repeatedly until all PRD (Product Requirements Document) items are complete. Each iteration is a **fresh instance with clean context**. Memory persists via **git history**, `progress.txt`, and `prd.json`.

## Role in the workflow

| Layer | Role | Solves |
|-------|------|--------|
| **Ralph loop** (outer) | Run until all tasks are done | Context limits, task management |
| **anti-human-bottleneck** (inner) | Don’t wait for humans inside each run | Decision pauses, approval waits |

Ralph = “keep running until done.” Anti-human-bottleneck = “inside each run, don’t stop to ask.” Use both for near-full autonomy.

## How it works (summary)

1. **PRD** → task list (e.g. `prd.json`) with user stories and `passes` status.
2. **Each iteration**: New agent instance; picks highest-priority story where `passes: false`; implements it; runs checks (typecheck, tests); commits if OK; marks story `passes: true`; appends learnings to `progress.txt`.
3. **Stop when** all stories have `passes: true` (no human review required for completion).

Critical: **Completion is decided by tests/checks, not by the agent or a human.** Run until tests pass.

## Key ideas

- **Small tasks**: Each PRD item should fit in one context window. Split “build the whole dashboard” into many small stories.
- **Feedback loops**: Typecheck, tests, CI must be green. Ralph relies on these to know when a story is done.
- **AGENTS.md**: Update with learnings after iterations so future runs (and humans) see patterns and gotchas.
- **Human involvement**: For “problem finding and solving,” not for routine approval of each step. See the anti-human-bottleneck skill for not asking “should I push?” etc.

## References

- **Article (origin)**: [Agentワークフローで人間がボトルネックにならないためのSkill設計](https://nyosegawa.github.io/posts/claude-code-verify-command/) (逆瀬川) — Ralph loop as outer loop, anti-human-bottleneck as inner; source for this skill.
- **Ralph (snarktank)**: [github.com/snarktank/ralph](https://github.com/snarktank/ralph) — Loop implementation, PRD skill, `ralph.sh`, `prd.json`, `progress.txt`.
- **Ralph pattern (Geoffrey Huntley)**: [ghuntley.com/ralph](https://ghuntley.com/ralph/) / [ghuntley.com/loop](https://ghuntley.com/loop/) — Original “everything is a ralph loop” idea; human for problem-finding, not routine approval.
- **Matthew Berman**: [Why 'Ralph' Agents Are Upending How We Code](https://www.wisdomai.com/insights/matthew_berman/ralph-loop-autonomous-agents-ai-coding-context-window-ffdd1834) — Completion decided by tests, not by agent or human.

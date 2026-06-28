---
name: harness-engineering
description: >-
  Design the outer loop around agents: externalized state, executable
  verification gates, and harness config (AGENTS.md, init/test/review scripts)
  so agents never self-certify completion. Use when building long-running or
  production agent workflows—not for in-window context curation (use
  context-engineering), inner-loop autonomy habits (use anti-human-bottleneck),
  or library-specific implementation (use implement-with-practices).
disable-model-invocation: false
---

# Harness Engineering

A **harness** is everything outside the model that makes agent loops reliable: state files, git, permissions, scripts, and **non-negotiable verification gates**. Engineering leverage in 2025–2026 shifted from prompt tuning alone to this outer structure ([Anthropic harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps); [LangChain deep agents](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering)).

Core rule: **the agent does not declare success**—executable checks do.

## When to use

- Long-running or multi-iteration agent work (beyond one context window).
- Production coding agents, Ralph-style loops, or CI-integrated agent runs.
- Failures from overconfident termination, compounding errors, or missing self-evaluation.
- Setting up `AGENTS.md`, `init.sh`, `test-all.sh`, or review gates for a repo.

Skip when:

- Only need faster non-interactive test runs → `non-interactive-hang`.
- Only need context window hygiene → `context-engineering`.
- Inner-loop "don't ask the human" behavior → `anti-human-bottleneck` (pairs with harness; does not replace gates).

## Harness layers

| Layer | Responsibility | Examples |
|-------|----------------|----------|
| **Config** | Tell any agent how to build, test, boundaries | `AGENTS.md`, tiered tool permissions |
| **State** | Truth outside the model | `prd.json`, `progress.txt`, git |
| **Gates** | Deterministic pass/fail | test runner, linter, typecheck, security scan |
| **Loop** | Fresh context per iteration | Stateless outer loop; see `ralph-loop` |

## Verification gates (mandatory pattern)

1. **`init` (once)** — Install deps, build, confirm baseline green before agent edits.
2. **`test` (every iteration)** — Non-zero exit = not done; re-queue work. Agent cannot override.
3. **`review` (after test)** — Lint, types, optional security scanner on the diff.

Scripts must be **executable and wired into the loop**, not described only in prose. Pair with `non-interactive-hang` for agent-safe entrypoints (no `pause` / modal hangs).

## Stateless outer loop

For work longer than one context window:

- **Fresh context per iteration**; durable state in files + git.
- Inner ReAct/plan-execute stays **under ~half** the advertised context budget when possible.
- Completion when **gates pass and task list is satisfied**, not when the model says "done".

`ralph-loop` is one concrete pattern (PRD JSON + progress file + test-driven stories).

## Self-evaluation and tracing

- Add **evaluator steps** separate from generator steps when UI/behavior quality matters (different role or script).
- Use **traces** (tool I/O, decisions) as a feedback signal to tune harness, tools, and instructions together ([LangChain](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering)).
- On new model releases, **re-benchmark the harness**; strip obsolete guardrails, add new ones.

## Workflow

1. **Inventory** — Existing test/lint/build commands; agent entrypoints; `AGENTS.md`.
2. **Wire gates** — `init` → agent work → `test` → `review`; fail closed.
3. **Externalize state** — Task list + progress notes; git as source of truth.
4. **Configure harness docs** — `AGENTS.md`: build, test, off-limits paths, verification order.
5. **Run loop** — Outer iteration until gates + task list green (`ralph-loop` optional).
6. **Refine** — Read traces; fix tool gaps, flaky gates, or missing context (may need `context-engineering`).

## Pairing with other skills

| Skill | Role |
|-------|------|
| `ralph-loop` | PRD-driven outer loop implementation |
| `anti-human-bottleneck` | Inner loop: act without routine human prompts |
| `non-interactive-hang` | Agent-safe verify scripts, measured timeouts |
| `context-engineering` | When gate failures trace to context rot |
| `repo-agent-bootstrap` | Initial `AGENTS.md` + registry scaffolding |

High-risk irreversible actions may still need **architectural human approval** (outside the model)—complements, not replaces, `anti-human-bottleneck`.

## Report template (user-facing, Japanese)

```markdown
## Harness Engineering

- **対象**: …（repo / loop / 長時間タスク）
- **ゲート**: init / test / review（コマンド）
- **状態**: …（prd.json, progress, git）
- **検証**: …（ゲート結果）
- **次**: …（ralph 化 / trace 改善）
```

## Reference

- [reference.md](reference.md) — gate checklist, AGENTS.md hints, anti-patterns
- [references/sources.md](references/sources.md) — upstream URLs

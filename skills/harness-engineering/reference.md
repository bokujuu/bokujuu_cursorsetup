# Harness Engineering — Reference

## AGENTS.md checklist

Minimum sections for agent-facing harness config:

- How to install / build (`init` command)
- How to test (`test` command) and lint/review (`review` command)
- Directory layout and entry points
- Off-limits paths (secrets, generated artifacts, vendor)
- Verification order: **init → change → test → review → commit**

[AGENTS.md](https://agents.md/) is an open convention adopted across coding agents (Cursor, Copilot agent, Codex CLI, etc.).

## Gate script contract

| Script | When | Pass criteria | Fail behavior |
|--------|------|---------------|---------------|
| `init.sh` / `init` | Start of session / loop | Exit 0, baseline green | Abort agent run; fix env |
| `test-all.sh` / `test` | After each iteration | Exit 0, tests pass | Re-queue task; no "done" |
| `review.sh` / `review` | After test pass | Lint + types + optional SAST clean | Fix before commit |

Agent entrypoints should use non-interactive wrappers (`NO_PAUSE=1`, CI env, Python driver)—see `non-interactive-hang`.

## Plan–execute–verify structure

```
Plan (decompose to verifiable steps, external file)
  → Execute (one step / one story per iteration)
  → Verify (script or separate evaluator — not self-report)
  → Repeat until all steps pass gates
```

Compounding errors in raw ReAct loops are a primary motivator for this structure ([field guide](https://genalphai.com/agentic-loops-and-harness-engineering/)).

## Evaluator separation

When "tests pass" is insufficient (UX bugs, shallow features):

- **Generator** implements from spec.
- **Evaluator** exercises the running app (browser/API probes) or reviews against depth rubric.
- Optional **sprint contract**: agree on done criteria before coding ([Anthropic long-running harness](https://www.anthropic.com/engineering/harness-design-long-running-apps)).

## Trace-driven refinement loop

1. Capture run traces (tools, latencies, errors).
2. Cluster failure modes (missing tool, wrong path, bad instruction).
3. Patch harness (AGENTS.md, tool manifest, gate script)—not only the prompt.
4. Re-run benchmark tasks.

## Anti-patterns

| Anti-pattern | Fix |
|--------------|-----|
| Agent says "all tests pass" without running them | Mandatory `test` gate in loop |
| State only in chat history | `progress.txt` / git / JSON task list |
| Single monolithic prompt for 50-step project | Outer loop + small stories (`ralph-loop`) |
| Human approves every green test | `anti-human-bottleneck` for inner loop; gates for quality |
| Prompt-only "please verify your work" | Executable verification |

## Related skills

- `ralph-loop` — Ralph pattern specifics (`prd.json`, `progress.txt`)
- `context-engineering` — When harness is sound but context degrades
- `templates/loop-orchestration/` — Tiered loop scripts (bash, ps1, mjs)

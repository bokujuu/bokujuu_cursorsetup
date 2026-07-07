---
name: agent-handoff-recovery
description: >-
  Detects agent failure patterns from instruction drift, plan/status mismatch,
  skipped verification, subagent handoff gaps, or ambiguous multi-track scope.
  Course-corrects by reconciling SoT, plan todos, and verify commands before
  continuing. Use when work does not match expectations, todos stay pending,
  background subagents finished without synthesis, a new session lacks context,
  or the user asks why instructions did not land.
disable-model-invocation: false
---

# Agent Handoff Recovery

## Purpose

Stop "keep coding on the wrong track" loops. Reconcile **track, SoT, plan status, and verification** before more edits.

Works with `anti-human-bottleneck` (recover autonomously; ask the user only when blocked), `fable-style-reasoning` (anchor in plan + subagent synthesis in full mode), and `retrospective-codify` (after recovery, codify recurring gaps).

## Self-check triggers (any one → run recovery)

| Signal | Typical cause |
|--------|----------------|
| User says expectations not met / instructions did not land | Scope or SoT drift |
| Plan todos `pending`/`in_progress` but files look done (or reverse) | Session handoff gap |
| Background `Task` / subagent finished; parent only confirmed | Missing synthesis |
| Multiple tracks touched in one diff | Parallel scope bleed |
| "Done" without running project verify/build | False completion |
| New session; user did not attach plan/AGENTS | Context amnesia |
| Vague user ask with no done criteria | Missing contract |

## Recovery loop (mandatory order)

1. **Stop implementation** — no new features until verify passes.
2. **Identify track** — one primary per session.
3. **Load SoT** — user rule → `AGENTS.md` → `.cursor/plans/*.plan.md` → project `.cursor/skills/*/SKILL.md`.
4. **Reconcile state** — `git status`, plan todo YAML, last verify output.
5. **Run verify** — from `.cursor/handoff-recovery.local.md` or `AGENTS.md`.
6. **Report** — status block (Japanese for user-facing text).
7. **Continue or ask** — one `AskQuestion` (2–4 options) only if still ambiguous.

## Status block template

```markdown
## 状況整理

- **トラック**: …
- **SoT**: …（ファイルパス）
- **Plan**: …（todo 名と status）
- **検証**: …（コマンド + OK/NG/未実行）
- **次**: …（1–3 項目）
```

## Subagent / multitask rules

- Do not delegate full plan implementation to background subagents unless the parent synthesizes and verifies in the same session.
- Multitask only when tracks are file-disjoint.
- After `subagentStop`: read changes → verify → update plan todos → one integrated reply.
- When `fable-style-reasoning` full mode is active: parent keeps `.cursor/plans/*.plan.md` anchor and re-sorts subagent output into fact / assumption / unknown before continuing (see that skill).

## Reference

- [reference.md](reference.md) — pattern catalog P1–P8
- [project-extension-template.md](project-extension-template.md) — per-repo `.cursor/handoff-recovery.local.md`

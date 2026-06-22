# Agent Handoff Recovery — Reference

## Failure pattern catalog

| ID | Symptoms | Recover |
|----|----------|---------|
| P1 | Wrong interpretation; no track/done criteria | Draft 5-line contract; safest default |
| P2 | Plan todos vs files/verify mismatch | Verify → update plan YAML |
| P3 | New session reimplements | Read AGENTS.md + plan + skills first |
| P4 | Subagent done; parent only confirmed | Synthesize + verify + plan update |
| P5 | Unrelated paths in one diff | One track; revert bleed |
| P6 | "Done" without build/test | Run SoT verify until green or report [FAIL] |
| P7 | Reinvents external procedure | Read external skill/script; cite source |
| P8 | Ask vs Agent mode mismatch | State limit; switch mode if needed |

## Layered architecture

| Layer | Location | Responsibility |
|-------|----------|----------------|
| Workflow | `~/.codex/skills/agent-handoff-recovery/` | Recovery loop |
| Hook (optional) | `~/.cursor/hooks.json` | `stop` / `subagentStop` nudge |
| Project | `<repo>/.cursor/handoff-recovery.local.md` | Tracks + verify commands |
| Domain | `<repo>/.cursor/skills/*/` | COM, Excel, etc. |

## Learned patterns

| Date | Pattern | Fix |
|------|---------|-----|
| 2026/06/02 | Plan pending but code merged | Verify + reconcile plan todos before done |

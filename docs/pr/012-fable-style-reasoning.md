# PR design note: fable-style-reasoning

Updated: 2026/07/07

## Purpose

Global skill for observation-first agent work in **Cursor / Composer 2.5**. Backbone: Anthropic disclosed Fable 5 epistemology (verbatim in references). Supplement: non-official Phase 0–4 workflow.

## Layer structure

| Layer | Source |
|-------|--------|
| Backbone A | [System Prompts — Fable 5 (2026-06-09)](https://platform.claude.com/docs/en/release-notes/system-prompts) |
| Backbone B | Same page — Opus 4.7–4.8 (`acting_vs_clarifying`, `capability_check`, `tool_discovery`) |
| Supplement | [shotatykr trace](https://x.com/shotatykr/status/2074035238116769851) |
| Reference | CL4R1T4S etc. (patterns only) |

## Design decisions

| Item | Decision |
|------|----------|
| slug | `fable-style-reasoning` (not Anthropic-official) |
| Language | English SKILL.md (behavior-neutral; official quotes stay English) |
| Runtime | Cursor / Composer 2.5 native tool names (`Read`, `GetMcpTools`, `Task`, …) |
| Modes | skip / light (backbone) / full (Phase 0–4) / delegate to recovery |
| Light gate | Observable verify closes task — not file count |
| Anchor SoT | Top of `.cursor/plans/*.plan.md` |
| Verbatim backbone | `references/official-excerpts.md` — Read at light/full entry |
| Output template | Start / phase transition / completion only |
| Eval | `references/eval-scenarios.md` (5 scenarios incl. Composer) |
| Ops notes | `references/skill-memory.md` |

## Related updates

- `MANIFEST.md` / `docs/rule-index.md`
- `.codex/practice-registry.json` (draft)
- `skills/repo-agent-bootstrap` — AGENTS template
- `skills/abstract-source-patterns/references/sources.md`
- `skills/agent-handoff-recovery` — cross-ref unchanged

## Verification

```bash
bash scripts/install.sh
python3 scripts/verify_repo_setup.py
```

Manual: `references/eval-scenarios.md` (5 scenarios).

## Deferred

- Detailed priority matrix vs other skills — add to skill-memory if friction appears

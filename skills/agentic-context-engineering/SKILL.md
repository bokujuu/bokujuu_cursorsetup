---
name: agentic-context-engineering
description: >-
  Maintain evolving agent playbooks (skills, AGENTS.md, session memory) with
  incremental delta updates instead of monolithic rewrites. Use when refining
  instructions after failures, growing skill-memory, or avoiding context collapse
  and brevity bias—not for one-off prompts (use empirical-prompt-tuning) or
  post-task rule classification (use retrospective-codify).
disable-model-invocation: false
---

# Agentic Context Engineering (ACE)

Treat agent instructions and memory as an **evolving playbook**, not a prompt to shrink. Based on [Agentic Context Engineering (Zhang et al., 2025)](https://arxiv.org/html/2510.04618).

## When to use

- Repeated failures suggest missing tactics, not a bad model.
- `skill-memory.md` or AGENTS.md is growing and someone proposes "rewrite it shorter".
- Iterative prompt/skill tuning keeps losing domain detail (brevity bias).
- A full-context rewrite is tempting after a bad run (context collapse risk).

Do **not** use when:

- One-off prompt quality check → `empirical-prompt-tuning`.
- Classifying a single lesson into rule vs skill vs lint → `retrospective-codify`.
- Creating a brand-new task-category skill from scratch → `skill-lifecycle`.

## Core failure modes (avoid)

| Mode | Symptom | Fix |
|------|---------|-----|
| **Brevity bias** | Summaries drop domain specifics ("create tests…" everywhere) | Add atomic bullets with examples; do not shorten wholesale |
| **Context collapse** | Full rewrite shrinks 10k+ tokens to a stub; accuracy drops | **Delta updates only** — add/edit/remove by stable id |

## Three roles (separate concerns)

Run these as distinct steps (different prompts or passes). Do not let one role do another's job.

| Role | Input | Output | Must not |
|------|-------|--------|----------|
| **Generator** | Playbook + task | Trajectory, outcome, candidate bullets | Rewrite the whole playbook |
| **Reflector** | Trajectory + outcome | Scored insights (helpful/harmful, keep/drop) | Edit playbook text |
| **Curator** | Reflector deltas | `add` / `edit` / `remove` by item id | Replace playbook wholesale |

Whole-playbook regeneration is **forbidden**.

## Workflow (mandatory order)

1. **Baseline** — Identify the playbook artifact (`SKILL.md`, `AGENTS.md`, `references/skill-memory.md`, or project `CLAUDE.md` section).
2. **Execute** — Run the task (Generator). Capture what worked and what failed.
3. **Reflect** — List 1–5 atomic insights with evidence from the trajectory. Tag each: helpful / harmful / uncertain.
4. **Curate deltas** — Propose only:
   - `add`: new bullet with stable id (e.g. `ace-20260615-01`)
   - `edit`: same id, revised text
   - `remove`: id + reason (harmful or superseded)
5. **Dedup** — Before merge, `rg` the playbook for overlapping advice; merge or reject duplicates.
6. **Verify** — Re-run the scenario or project's verify command; regression means revert the harmful delta.
7. **Record** — Append provenance to `references/skill-memory.md` (date, delta ids, outcome).

## Playbook item shape

Each item should be self-contained:

```markdown
- **id**: `ace-YYYYMMDD-NN`
- **tactic**: One imperative sentence.
- **example** (optional): Minimal worked case.
- **provenance**: PR / session / failure that motivated it.
```

Prefer many small items over one long paragraph.

## Boundaries with sibling skills

| Skill | ACE vs sibling |
|-------|----------------|
| `skill-lifecycle` | Lifecycle manages *whether* to create a skill; ACE manages *how* playbook content evolves |
| `retrospective-codify` | Retrospective picks artifact type (lint/rule/skill); ACE governs incremental edits inside playbooks |
| `empirical-prompt-tuning` | Empirical tunes prompt clarity with blind executors; ACE preserves accumulated domain knowledge |

## Red flags

| Rationalization | Reality |
|-----------------|---------|
| "Shorter prompt = better" | LLMs often need long, specific playbooks; brevity bias drops signal |
| "Rewrite everything fresh" | Context collapse erases hard-won edge cases |
| "One model pass can reflect and curate" | Role bleed drops items silently; split roles |
| "Delete old bullets to save tokens" | Prune only with Reflector evidence, not convenience |

## Verification

```bash
# Playbook exists and uses delta ids (no empty rewrite)
rg "ace-[0-9]{8}-" skills/<slug>/references/skill-memory.md AGENTS.md 2>/dev/null || true
# Project verify (replace with repo-specific command)
python3 -m py_compile hooks/handoff-stop-check.py
```

## Reference

- [references/sources.md](references/sources.md) — primary sources
- [references/skill-memory.md](references/skill-memory.md) — operational notes

# MUSE-Autoskill — reference mapping

External source for the `skill-lifecycle` global skill. This repo does **not** implement the MUSE runtime or `skill_create` tool.

## Source

- Paper: [MUSE-Autoskill: Self-Evolving Agents via Skill Creation, Memory, Management, and Evaluation](https://arxiv.org/abs/2605.27366) (May 2026)
- Introductory post (JA): [Trtd6Trtd on X](https://x.com/Trtd6Trtd/status/2062127152271872085)

## Idea (one paragraph)

Agents improve by treating skills as **long-lived assets**: search existing skills, create only on demand inside the work loop, store per-skill experience, organize and select skills efficiently, and validate with tests plus runtime feedback before refinement.

## Lifecycle mapping (MUSE → bokujuu_cursorsetup)

| MUSE stage | What MUSE does | This repo |
|------------|------------------|-----------|
| **Creation** | `skill_create` in runtime loop | `templates/project-skills/` or `implement-with-practices` `scaffold_local_skill.py` |
| **Memory** | Skill-level memory across tasks | `references/skill-memory.md` per repo-local skill |
| **Management** | Select and organize skills | `.codex/practice-registry.json`, search `~/.codex/skills/` + `.codex/skills/` |
| **Evaluation** | Unit tests + execution feedback | Verification commands in SKILL + registry |
| **Refinement** | Auto-refine on test failure | Update skill-memory; `retrospective-codify` for structural gaps |

## Global skills involved

| Skill | Role |
|-------|------|
| `skill-lifecycle` | Generic task-category skill evolution |
| `implement-with-practices` | Technology-specific repo-local practices |
| `empirical-prompt-tuning` | Harden important skills/prompts |
| `retrospective-codify` | Codify lessons after task completion |

## What we deliberately omit

- Reinforcement learning / trained skill curator
- Built-in `skill_create` MCP or hook
- Full SkillsBench reproduction

## Related files

- [skills/skill-lifecycle/SKILL.md](../../skills/skill-lifecycle/SKILL.md)
- [templates/project-skills/README.md](../../templates/project-skills/README.md)
- [docs/rule-index.md](../rule-index.md)

# Skill Lifecycle — Reference

## Decision flow

```dot
digraph skill_lifecycle {
    "New or recurring task?" [shape=diamond];
    "Existing skill fits?" [shape=diamond];
    "Library or API specific?" [shape=diamond];
    "Apply existing skill" [shape=box];
    "implement-with-practices" [shape=box];
    "Scaffold from project-skills template" [shape=box];
    "Skip skill creation" [shape=box];

    "New or recurring task?" -> "Existing skill fits?" [label="yes"];
    "New or recurring task?" -> "Skip skill creation" [label="one-off"];
    "Existing skill fits?" -> "Apply existing skill" [label="yes"];
    "Existing skill fits?" -> "Library or API specific?" [label="no"];
    "Library or API specific?" -> "implement-with-practices" [label="yes"];
    "Library or API specific?" -> "Scaffold from project-skills template" [label="no"];
}
```

## Skill boundaries

| Skill | Scope | Trigger |
|-------|--------|---------|
| `skill-lifecycle` | Task-category skills, registry, reuse | Recurring workflow, skill-ify request |
| `implement-with-practices` | Tech stack patterns in this repo | Library/API/framework implementation |
| `retrospective-codify` | Post-task learnings → rule/skill/lint | Task done, "ルール化して" |
| `empirical-prompt-tuning` | Prompt/skill quality via blind executor | New or revised skill needs hardening |

## Search locations

| Location | Contents |
|----------|----------|
| `~/.codex/skills/` | Global skills (install.ps1 from bokujuu_cursorsetup) |
| `.codex/skills/` | Repo-local draft/approved skills |
| `.cursor/skills/` | Cursor project-local skills |
| `.codex/practice-registry.json` | Index of repo-local practices |

## MUSE mapping (summary)

Full table: [docs/references/muse-autoskill.md](../../docs/references/muse-autoskill.md).

| MUSE stage | This repo |
|------------|-----------|
| Creation | Template scaffold or `scaffold_local_skill.py` |
| Memory | `references/skill-memory.md` per skill |
| Management | `practice-registry.json` |
| Evaluation | Verification commands in skill + registry |
| Refinement | skill-memory updates, `retrospective-codify` |

## Related

- [implement-with-practices references/overview.md](../implement-with-practices/references/overview.md)

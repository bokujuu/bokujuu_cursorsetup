---
name: skill-lifecycle
description: >-
  Evolve reusable agent skills for recurring work categories: search existing
  global and repo-local skills first, scaffold a draft only when none fit, run
  verification, register in practice-registry, and refine via skill-memory.
  Use when adding a new task type, automating repeated workflows, or growing
  repo-local skills—not for library-specific implementation patterns (use
  implement-with-practices) or post-task retrospectives (use retrospective-codify).
disable-model-invocation: false
---

# Skill Lifecycle

Manage **task-category skills** as long-lived assets: create on demand, reuse across sessions, validate, and refine. Inspired by [MUSE-Autoskill](https://arxiv.org/abs/2605.27366); operational mapping: [docs/references/muse-autoskill.md](../../docs/references/muse-autoskill.md).

Works with `implement-with-practices` (technology-specific patterns), `empirical-prompt-tuning` (quality loop for important skills), and `retrospective-codify` (after repeated failures).

## When to use

- A **new category of work** will recur (onboarding steps, release checklist, domain workflow).
- User asks to **skill-ify** a procedure or "remember how we do X".
- An existing repo-local skill is **stale** after verify failures or process change.

Do **not** use when:

- The task is **library/API-specific** → `implement-with-practices` + `scaffold_local_skill.py`.
- The task is **one-off** with no reuse → skip skill creation.
- You only need **post-mortem rule extraction** → `retrospective-codify`.

## Lifecycle loop (mandatory order)

1. **Search** — Before inventing steps, search in order:
   - `%USERPROFILE%\.codex\skills\` (global)
   - `<repo>/.codex/skills/`, `<repo>/.cursor/skills/`
   - `<repo>/AGENTS.md`, `<repo>/.codex/practice-registry.json`
   - Keywords: task nouns, tool names, domain terms (2–3 terms via `rg`).
2. **Apply** — If a skill fits, follow it as SoT. Multiple hits: pick the one closest to user intent; do not merge unrelated skills in one pass.
3. **Create (only if gap)** — Copy from [templates/project-skills/](../../templates/project-skills/) into `<repo>/.codex/skills/<slug>/`. Replace `{{SLUG}}`, triggers, and verification commands.
   - **Technology-specific** (framework, SDK, API): use `implement-with-practices` and `scaffold_local_skill.py` instead of duplicating scaffold logic here.
4. **Verify** — Run every command listed in the skill and in registry `verification_commands`. Record pass/fail before claiming done.
5. **Register** — Add or update `<repo>/.codex/practice-registry.json` with `status: draft` (see template). Promote to `approved` only after stable reuse (optional: `promote_local_skill.py` from implement-with-practices).
6. **Refine** — On failure or repeat friction: append to `references/skill-memory.md`; escalate to `retrospective-codify` if the gap is structural.

## Registry rules

- Path: `.codex/practice-registry.json`
- Per entry: `slug`, `summary`, `trigger_keywords`, `verification_commands`, `skill_path`, `status`
- Allowed `status`: `draft`, `approved` only

## Skill memory (lightweight)

After each non-trivial use of a repo-local skill, append one bullet to that skill's `references/skill-memory.md`:

- Date (optional), what worked, what failed, pitfall to avoid next time.

Do not store secrets or environment-specific tokens in skill memory.

## Report template (user-facing, Japanese)

```markdown
## Skill ライフサイクル

- **検索**: …（ヒットした skill / なし）
- **採用**: …（slug または新規 draft）
- **検証**: …（コマンド + OK/NG）
- **registry**: …（更新有無）
- **次**: …（refine / promote / 作業継続）
```

## Reference

- [reference.md](reference.md) — decision flow, skill boundaries
- [templates/project-skills/](../../templates/project-skills/) — repo-local scaffold

# Project-local skills template

Copy into a **target repository** to start `.codex/skills/` and a practice registry. Used by the global skill `skill-lifecycle`.

## Layout after copy

```
<target-repo>/
├── .codex/
│   ├── practice-registry.json
│   └── skills/
│       └── <slug>/
│           ├── SKILL.md
│           └── references/
│               └── skill-memory.md
```

## Setup

1. Create `.codex/` at the repository root if missing.
2. Copy `practice-registry.json` → `<target-repo>/.codex/practice-registry.json`.
3. Copy `skill/` → `<target-repo>/.codex/skills/<slug>/` (rename folder to your slug).
4. Edit `SKILL.md`: replace `{{SLUG}}`, summary, triggers, verification commands.
5. Add a registry entry with `status: draft`.
6. Run verification commands; append outcomes to `references/skill-memory.md`.

## Technology-specific skills

For library/API/framework patterns, prefer `implement-with-practices` and:

```powershell
python $env:USERPROFILE\.codex\skills\implement-with-practices\scripts\scaffold_local_skill.py `
  --target <repo-root> --slug <slug> --summary "..." `
  --trigger-keyword "..." --verification-command "..." --source-url "..."
```

Do not duplicate that scaffold with this generic template.

## Domain skill examples (templates)

| 雛形 | 用途 |
|------|------|
| [qa-multi-perspective/](qa-multi-perspective/) | 多ペルソナ固定のテスト観点（new-feature / migration） |

For richer repo-local skills (progressive disclosure, fixed output format, template catalog), see the global skills in this repository:

- [skills/japanese-doc-review/](../../skills/japanese-doc-review/) — Japanese prose review
- [skills/japanese-technical-writing/](../../skills/japanese-technical-writing/) — Japanese technical writing

Deploy to a target repository's `.codex/skills/`:

```powershell
Copy-Item -Recurse skills/japanese-doc-review <target-repo>/.codex/skills/
Copy-Item -Recurse skills/japanese-technical-writing <target-repo>/.codex/skills/
```

## Related

- Global skill: `skill-lifecycle` (install via `scripts/install.ps1`)
- Global skill: `repo-agent-bootstrap` — AGENTS.md + repo-local skill + registry の一括初期構築・メンテナンス（同等の雛形を skill 内 `assets/templates/` に同梱）
- [docs/references/muse-autoskill.md](../../docs/references/muse-autoskill.md)

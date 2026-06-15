# AGENTS.md

## Cursor Cloud specific instructions

This repository (`bokujuu_cursorsetup`) is a **configuration/distribution repo** for Cursor/Codex
global setup. It is **not** a runnable web/app service: there is no package manager, no dependency
manifest (no `package.json`/`pyproject.toml`/`requirements.txt`), and no CI workflow. The "products"
are a few shell/PowerShell installers, a Cursor hook, helper Python scripts, plus Markdown
rules/skills/docs.

### Runtimes
- Pure standard-library Python (3.9+) and POSIX `bash`. No third-party packages are required, so the
  startup update script is intentionally a near no-op.
- `python3` is available; there is **no `python` alias** on the VM. `hooks/hooks.template.json`
  invokes `python` (it targets Windows/Cursor); run the hook directly with `python3` when testing.

### Key components and how to run them
- **Skills installer (Linux/macOS/WSL):** `bash scripts/install.sh` copies every `skills/<name>/`
  into `~/.codex/skills/`. (`scripts/install.ps1` is the Windows equivalent and only runs under
  PowerShell.)
- **Self-test / validation:** `python3 temp/validate_new_skills.py`. It checks repo files **and**
  that skills are installed under `~/.codex/skills/`, so run `scripts/install.sh` first or some
  `installed <skill>` checks will fail.
- **Handoff hook:** `echo '{"cwd":"/workspace"}' | python3 hooks/handoff-stop-check.py stop`
  (also accepts `subagentStop`). It reads JSON on stdin and prints JSON; it fails open (never errors).
- **Local-skill toolchain:** the scripts in `skills/implement-with-practices/scripts/`
  (`scaffold_local_skill.py`, `validate_local_skill.py`, `promote_local_skill.py`) import
  `practice_helpers` as a sibling module and resolve templates relative to that folder — **run them
  from inside `skills/implement-with-practices/scripts/`** (e.g. `cd` there first), not via an
  absolute path from elsewhere. `scaffold_local_skill.py` requires `--target`, `--slug`, `--summary`,
  and at least one each of `--trigger-keyword`, `--verification-command`, `--source-url`.

### Lint / "build"
- There is no build step. Sanity-check edits with `bash -n scripts/install.sh`,
  `python3 -m py_compile <changed .py>`, and `python3 -c "import json; json.load(open('<file>'))"`
  for JSON templates.
- `py_compile` writes `__pycache__/` dirs; they are gitignored, but clean them up if needed.

### Editing notes
- User Rules in `user-rules/` and skills in `skills/` are the source of truth in this repo; they are
  applied to a developer's machine via the installers and are not auto-synced to Cursor Settings.

# AGENTS.md — bokujuu_cursorsetup

更新: 2026/06/15 13:00

## このリポジトリの目的

Cursor / Codex 向けの**グローバル設定一式**（User Rules 原本・自作 Skills・Hooks 雛形・MCP 雛形・各種テンプレ）を配布・保守する Private リポジトリ。

- 入力: `user-rules/`、`skills/`、`templates/`、`hooks/`、`mcp/`
- 出力: `~/.codex/skills/` へのコピー、Settings への手動貼り付け、任意で Hooks / MCP
- ルール・仕様の SoT: [MANIFEST.md](MANIFEST.md)（同梱一覧）・[docs/rule-index.md](docs/rule-index.md)（タスク別参照）
- 経緯: [README.md](README.md) / 手順: [INSTALL.md](INSTALL.md)

## 作業前に必ず読むもの

| 作業 | 読むドキュメント |
|------|------------------|
| 初回インストール・配布 | [INSTALL.md](INSTALL.md) |
| User Rules の貼り方 | [docs/user-rules-guide.md](docs/user-rules-guide.md) |
| タスク別ルール・skill 参照 | [docs/rule-index.md](docs/rule-index.md) |
| **グローバル skill の追加・更新** | `.cursor/skills/maintain-global-skill/SKILL.md`（標準手順） |
| ループオーケストレーション | [docs/loop-engineering.md](docs/loop-engineering.md) |

## 主要コマンド

```bat
.\scripts\install.ps1
python scripts\verify_repo_setup.py
python scripts\verify_loop_kit.py
```

User Rules をローカル正から再取得する場合（**本 repo を正とするなら使わない**）:

```bat
.\scripts\sync-from-local.ps1
```

## 重要な不変条件

- `skills/` の各フォルダ名と `SKILL.md` の frontmatter `name:` は一致すること
- `install.ps1` の `$Root` は `Split-Path -Parent $PSScriptRoot`（1 段上）— 二重 `Split-Path` は誤り
- 新規 skill は [MANIFEST.md](MANIFEST.md) と（ユーザー向けなら）[docs/rule-index.md](docs/rule-index.md) に追記すること
- User Rules（Settings）は Git 連携されない — `user-rules/` 編集後は手動反映
- 機密（PAT・個人パス）は `mcp.json` 等にコミットしない

## データ・Git の取り扱い

- `temp/` は検証出力・PR 下書き用（コミットは必要時のみ）
- 一時出力は `temp/` へ
- 変更時の更新順: SoT（MANIFEST / rule-index）→ `skills/` 実装 → `install.ps1` 確認 → 検証 → README / INSTALL

## コーディング規約

- PowerShell 5.1+（Windows）、bash は `install.sh` 用
- Python 検証スクリプトは `# -*- coding: utf-8 -*-`、`open(..., encoding='utf-8')`
- ドキュメントの日付は `Get-Date -Format 'yyyy/MM/dd HH:mm'` で実時刻を取得して記載

## リポジトリローカルスキル

| スキル | 用途 |
|--------|------|
| `.cursor/skills/maintain-global-skill/` | `skills/` へのグローバル skill 追加・更新・検証・PR までの標準手順 |

登録簿: `.codex/practice-registry.json`

## 未決事項（変更が来る可能性が高い箇所）

- `sync-from-local.ps1` の `$Root` が二重 `Split-Path` のまま（本 repo 正運用では未使用想定）

---

## Cursor Cloud specific instructions

This repository (`bokujuu_cursorsetup`) is a **configuration/distribution repo** for Cursor/Codex
global setup. It is **not** a runnable web/app service: there is no package manager, no dependency
manifest (no `package.json`/`pyproject.toml`/`requirements.txt`), and no CI workflow. The "products"
are a few shell/PowerShell installers, a Cursor hook, helper Python scripts, plus Markdown
rules/skills/docs.

### Runtimes

- Pure standard-library Python (3.9+) and POSIX `bash`. No third-party packages are required.
- `python3` is available on Cloud VMs; there is **no `python` alias**. Use `python3` when testing on
  Linux. (`hooks/hooks.template.json` invokes `python` for Windows/Cursor.)

### Key components and how to run them

- **Skills installer (Linux/macOS/WSL):** `bash scripts/install.sh` copies every `skills/<name>/`
  into `~/.codex/skills/`. (`scripts/install.ps1` is the Windows equivalent.)
- **Self-test / validation:** `python3 scripts/verify_repo_setup.py` (preferred) or
  `python3 scripts/verify_loop_kit.py`. Run `scripts/install.sh` first if checks need skills under
  `~/.codex/skills/`.
- **Handoff hook:** `echo '{"cwd":"/workspace"}' | python3 hooks/handoff-stop-check.py stop`
  (also accepts `subagentStop`). Fails open (never errors).
- **Local-skill toolchain:** run scripts in `skills/implement-with-practices/scripts/` from that
  directory (they import `practice_helpers` as a sibling module).

### Lint / "build"

- No build step. Sanity-check with `bash -n scripts/install.sh`,
  `python3 -m py_compile <changed .py>`, and JSON load for templates.
- `py_compile` writes `__pycache__/` dirs; they are gitignored.

### Editing notes

- User Rules in `user-rules/` and skills in `skills/` are the source of truth; applied via installers,
  not auto-synced to Cursor Settings.

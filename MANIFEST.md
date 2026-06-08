# 同梱マニフェスト

最終同期の想定元（ローカル）。`scripts/sync-from-local.ps1` で再取得できます（Windows・rulemaintenance 利用時）。

## user-rules/

| ファイル | 同期元（sync 利用時） |
|----------|------------------------|
| `user-rule-*.md` (8件) | `C:\CursorPJs\rulemaintenance\user-rule-*.md`（COM/VBA は同梱しない） |

**正の編集場所**: 本リポジトリを正とする場合は `user-rules/` を直接編集。

## skills/（グローバル・自作のみ）

| スキル | 備考 |
|--------|------|
| `anti-human-bottleneck` | sync 時は `%USERPROFILE%\.codex\skills\` から |
| `cursor-session-doc` | Cursor `agent-transcripts/*.jsonl` 用（本 repo 内で管理） |
| `empirical-prompt-tuning` | 同上 |
| `implement-with-practices` | 同上 |
| `ralph-loop` | 同上 |
| `retrospective-codify` | 同上 |
| `web-research-resolve` | 旧 `.cursor/commands/websearch-resolve` を skill 化 |
| `agent-handoff-recovery` | 指示ずれ・Plan/verify 折り返し（本 repo 内で管理） |
| `skill-lifecycle` | タスクカテゴリ Skill の検索・draft 化・registry・改良 |
| `system-structure-viz` | 構造・依存の Tier 別可視化（docs / canvas / 静的サイト） |
| `japanese-doc-review` | 日本語文書レビュー・校正指摘（[himadajin/skills](https://github.com/himadajin/skills) より取込） |
| `japanese-technical-writing` | 日本語技術文書の作成・改稿（同上） |

## hooks/（任意・Windows）

| ファイル | 内容 |
|----------|------|
| `handoff-stop-check.py` | Cursor `stop` / `subagentStop` 用 |
| `hooks.template.json` | `install.ps1` が `%USERPROFILE%\.cursor\hooks.json` に展開 |
| `README.md` | 手動マージ手順 |

## user-rules/（追加分）

| ファイル | 内容 |
|----------|------|
| `user-rule-agent-handoff-recovery.md` | 層 B: ずれ検知時に skill を読む（任意） |

## templates/project-rules/excel/

| ファイル | 内容 |
|----------|------|
| `README.md` | リポへの `.cursor/rules/` コピー手順 |
| `excel-com-automation.mdc` | win32com 共通（要 globs 調整） |
| `vba-coding-policy.mdc` | VBA 共通 |
| `pcaf-excel-agent.mdc.example` | SoT・検証・トークン効率の例 |

**廃止（user-rules から削除）**: `user-rule-com-automation.md`, `user-rule-vba-coding-policy.md`

## templates/project-skills/

| ファイル | 内容 |
|----------|------|
| `README.md` | 対象リポの `.codex/skills/` 展開手順 |
| `practice-registry.json` | registry 雛形 |
| `skill/SKILL.md` | 汎用 repo-local skill 雛形 |
| `skill/references/skill-memory.md` | skill 単位の経験メモ |

## templates/structure-viz/

| ファイル | 内容 |
|----------|------|
| `README.md` | Tier 1 / 3 のコピー手順 |
| `architecture.md` | Tier 1: Mermaid 置き場 |
| `site/index.html` | Tier 3: 単一 HTML + Mermaid CDN |

## docs/

| ファイル | 内容 |
|----------|------|
| `rule-index.md` | タスク別ルール参照 |
| `user-rules-guide.md` | Settings への貼り方（2 層運用） |
| `migration-from-legacy.md` | 旧 `.cursor/` からの移行 |
| `hooks-handoff-recovery.md` | handoff recovery 設計メモ |
| `references/muse-autoskill.md` | MUSE-Autoskill と本 repo の対応表 |
| `pr/` | PR 設計メモ |

## mcp/

| ファイル | 内容 |
|----------|------|
| `mcp.template.json` | 最小構成の雛形 |
| `mcp.optional.json` | playwright / serena（任意） |
| `README.md` | 適用手順・セキュリティ注意 |

## 意図的に含めないもの

| 対象 | 理由 |
|------|------|
| `%USERPROFILE%\.cursor\skills-cursor\` | Cursor 製品同梱。Cursor が自動同期 |
| `%USERPROFILE%\.codex\skills\.system\` | Codex 同梱 |
| 各プロジェクトの `.cursor/skills/` | リポジトリローカル |
| Obsidian Vault の commands | ワークスペース専用 |
| 旧 `.cursor/commands` / `mcp_enhanced.json` / `step_snapshot.py` | 廃止（移行表: `docs/migration-from-legacy.md`） |
| `codex-primary-runtime`（空ディレクトリ） | 中身なしのため同梱しない |

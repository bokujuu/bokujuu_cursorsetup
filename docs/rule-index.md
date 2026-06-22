# ルールインデックス（タスク別参照）

`user-rules/` 内の `user-rule-*.md` を、タスク種別に応じて参照する際の目安です。

適用の考え方（常時貼り付け vs タスク時参照）は [user-rules-guide.md](user-rules-guide.md) を参照してください。

## 行数の目安（2026/06/01 時点）

| ファイル | 行数 | 層 |
|----------|------|-----|
| `user-rule-cursor-integrated.md` | 約210 | コア |
| `user-rule-git-policy.md` | 約128 | 専門 |
| `user-rule-python-coding-policy.md` | 約130 | 専門 |
| ~~`user-rule-vba-coding-policy.md`~~ | — | **廃止** → `templates/project-rules/excel/` |
| ~~`user-rule-com-automation.md`~~ | — | **廃止** → 同上 |
| `user-rule-codex-mcp-strategy.md` | 約48 | 専門 |
| `user-rule-rule-creation-policy.md` | 約62 | 専門 |
| `user-rule-jst-date.md` | 約70 | 専門 |
| `user-rule-bookmarklet-best-practices.md` | 約31 | 専門 |
| `user-rule-ahkv2-coding-policy.md` | 約81 | 専門 |

**層 B の全ファイルを Settings に貼ると約700行**（COM/VBA 除く）になり、それでも上限に近づきやすいです。

## タスク別の参照順（上限: 通常 3 ファイル・合計 400–600 行）

該当セクションのみ渡す前提。2 ファイルで足りるタスクはそのままでよい。

| タスク | 参照順 |
|--------|--------|
| **Python** | cursor-integrated → python-coding-policy → git-policy |
| **COM/Excel（win32com）** | 対象リポの `.cursor/rules/excel-com-automation.mdc`（雛形: `templates/project-rules/excel/`）。層 B: python-coding-policy |
| **VBA** | 対象リポの `.cursor/rules/vba-coding-policy.mdc`（同上） |
| **Git** | git-policy → cursor-integrated（要約のみ） |
| **フロント/ブックマークレット** | cursor-integrated → bookmarklet-best-practices → git-policy（必要時） |
| **ルール作成** | rule-creation-policy → cursor-integrated（スタイル） |
| **Codex レビュー** | codex-mcp-strategy → cursor-integrated（MCP要約） |
| **ループ・無人収束（Ralph）** | skill `ralph-loop` → `templates/loop-orchestration/` → [loop-engineering.md](loop-engineering.md)。内側は `anti-human-bottleneck` |
| **エージェント基盤** | skill `repo-agent-bootstrap` → `templates/project-skills/` |
| **指示ずれ・セッション折り返し** | skill `agent-handoff-recovery`（推奨）または user-rule-agent-handoff-recovery |
| **Skill 化・進化（繰り返し手順）** | skill `skill-lifecycle` → 雛形 `templates/project-skills/`。技術特化は `implement-with-practices` |
| **構造・依存の可視化** | skill `system-structure-viz` → 雛形 `templates/structure-viz/` |
| **日本語技術文書（作成・改稿）** | skill `japanese-technical-writing` |
| **日本語文書レビュー（校正・指摘）** | skill `japanese-doc-review` |

`cursor-integrated` は**該当セクションのみ**渡す。COM/VBA はグローバル User Rules に載せない。

日本語文書 skill の運用: 執筆は `japanese-technical-writing`、指摘レビューは `japanese-doc-review`。「レビューして」単独は STRUCTURE のみ。全観点は `全部` / `総合` / `全観点` を指定する。

## グローバル skill（install 後）

| skill | 用途 |
|-------|------|
| `agent-handoff-recovery` | Plan/SoT/verify のずれを検知して状況整理 |
| `cursor-session-doc` | 過去 Cursor セッションの jsonl 要約 |
| `retrospective-codify` | タスク完了後の学びのルール化 |
| `skill-lifecycle` | タスクカテゴリ Skill の検索・作成・registry・改良 |
| `system-structure-viz` | アーキテクチャ・依存の可視化（Tier 1/2/3） |
| `implement-with-practices` | ライブラリ/API 特化の repo-local practice（skill-lifecycle と併用） |
| `ralph-loop` | 外側ループ（Ralph）— `templates/loop-orchestration/` と併用 |
| `repo-agent-bootstrap` | AGENTS.md / registry / verify の初期構築 |
| `japanese-doc-review` | 日本語 prose のレビュー・校正指摘（固定出力形式・観点依存） |
| `japanese-technical-writing` | 日本語技術文書の作成・改稿（テンプレート方針・5種テンプレ） |

外部参照: [references/muse-autoskill.md](references/muse-autoskill.md)

## 旧構成からの移行

廃止した `.cursor/commands` や旧 MCP ドキュメントとの対応表: [migration-from-legacy.md](migration-from-legacy.md)

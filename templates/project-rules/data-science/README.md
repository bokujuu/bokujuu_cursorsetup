# Data Science — プロジェクトローカルエージェント基盤

データ分析・DS 系リポジトリ向けの **AGENTS ルーター**と**データ安全 verify** の雛形。  
グローバル skill ではなく、対象 repo にコピーして使う（Excel テンプレと同じ考え方）。

## 何を抽象化したか

[atsushi-green/ds-ai-coding-skills](https://github.com/atsushi-green/ds-ai-coding-skills) から次だけ取り込む:

| パターン | 本テンプレでの実体 |
|----------|-------------------|
| 薄い入口 + スキルルーター | `AGENTS.md.template` |
| エージェント向けドキュメントの SoT | `docs/agent/README.md.template` |
| raw / 機密のコミット防止 | `scripts/check_no_raw_data_commit.py` |
| 秘密パターン検出 | `scripts/check_no_sensitive_patterns.py` |
| エージェント文書の整合 | `scripts/validate_agent_docs.py` |

## 除去した固有要素

- uv / polars / mypy / ruff の具体コマンド列（プロジェクトで差し替え）
- Copilot `.github/skills` と Claude `.claude/skills` の二重管理の全文
- DS 固有スキル 10 種の実装本文（必要なら `implement-with-practices` で別途 scaffold）

## 手順

1. 対象リポのルートに `docs/agent/` を作成
2. 本フォルダからファイルをコピーし `{{...}}` を置換
3. `AGENTS.md` をルートに配置（`AGENTS.md.template` から生成）
4. `scripts/` に verify 3 本をコピーし、パス・許可リストをプロジェクトに合わせて編集
5. `repo-agent-bootstrap` で `.codex/practice-registry.json` を整備
6. 分析用 repo-local skill は `templates/project-skills/qa-multi-perspective/` や `implement-with-practices` で追加

## 同梱ファイル

| ファイル | 用途 |
|----------|------|
| `AGENTS.md.template` | タスク別スキル・docs へのルーター |
| `docs/agent/README.md.template` | データカタログ・指標定義等の SoT 案内 |
| `data-safety-rules.md` | raw 不変・outputs 分離の不変条件 |
| `scripts/check_no_raw_data_commit.py` | `data/raw` 等のコミット検出 |
| `scripts/check_no_sensitive_patterns.py` | API キー等のパターン検出 |
| `scripts/validate_agent_docs.py` | AGENTS と docs/agent の最低限整合 |

## 参照

- 設計メモ: [docs/pr/004-qa-ds-template-adoption.md](../../docs/pr/004-qa-ds-template-adoption.md)
- パターン抽出: グローバル skill `abstract-source-patterns`
- 出典: [references/sources.md](references/sources.md)（作成後）

## 更新履歴

- 2026/06/29: 初版（ds-ai-coding-skills からルーター・データ安全のみ抽象化）

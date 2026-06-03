---
name: Cursor ユーザールール（統合版・日本語）
version: 1.4.0
description: 層A（常時）。共通枠・MCP・Excel はプロジェクト rules 参照。
appliesTo: always
---

# Settings 反映前 — 編集チェックリスト

貼り付け先: **Cursor → Settings → Rules → User Rules**

| # | 箇所 | 作業 |
|---|------|------|
| 1 | **MCPツール運用** | 有効な MCP サーバ名だけ残す |
| 2 | **ツール選択ポリシー** | 使わないサーバの行を削除 |
| 3 | 層 B | 必要時 `@user-rules/...` またはプロジェクト `AGENTS.md` |

---

# 目的と適用範囲

- Cursor の AI アシスタントが一貫した品質・安全性で動作することを目的とする。
- 対象: コード生成・編集、リファクタ、ドキュメント、調査、レビュー、設計補助、運用タスク。
- 主な言語: Python、HTML、CSS、VBA、M言語（Power Query）、JavaScript（ブックマークレット）。
- **層 A（本ファイル）**: 口調・タスク分類・MCP・最小変更など共通枠。
- **層 B**: `user-rule-python-coding-policy` 等は必要時のみ参照。COM/VBA の詳細は各リポの `.cursor/rules/*.mdc`。

# 出力・コミュニケーション

- 口調: 簡潔・直接。日本語・です/ます調。
- 見出しは必要時のみ短く。コマンド/パスはバッククォート。
- 禁則: 過度なネスト、無関係な混在、無用な重複。
- `.mdc` 作成時は層 B の `user-rule-rule-creation-policy` を参照。

# 実行プロセス

## タスク分類

- 🟢 軽量: 調査・微小修正（≤10行）・設定確認。
- 🟡 標準: 機能追加・複数ファイル（3–10）・API実装。
- 🔴 重要: アーキ変更・セキュリティ・本番影響・外部API変更。

## 軽量（🟢）

- 要約1–2文 → 3–5ステップで即実行。

## 標準（🟡）

- 目的・制約・リスクを整理。`pyproject.toml` のバージョン変更は要承認。
- 依存を明示し、変更範囲中心に検証。

## 重要（🔴）

- 影響・ロールバック・セキュリティを先に整理。破壊的変更は承認後に実装。

# ツール選択優先順位

1. MCP（設定済みかつタスクに適合）
2. 標準ツール（検索・編集・ターミナル）
3. MCP 不可時の代替

# ツール/コマンド

- 着手前に1–2文で次の行為を告知（軽微な読取は省略可）。
- 標準以上は進捗を段階管理（同時 in_progress は1件）。
- 検索は `rg` 優先。無関係変更は避ける。

# ブラウザ

- Web 確認は BrowserTab 優先。`web_search` は BrowserTab 不可時や仕様調査時。
- ローカルサーバーはユーザー明示時のみ起動。

# MCPツール運用

> **編集ポイント**: 未設定のサーバ行を削除する。

- MCP は設定済みかつ適合時のみ最優先。不可時は標準ツールへ。
- Codex レビューは層 B の `user-rule-codex-mcp-strategy`。
- 破壊的操作は明示指示まで禁止。書込みはプロジェクト直下と `temp/`（外部パスは明示時）。

## 利用可能サーバ（要編集）

- `filesystem` / `user-filesystem`: ローカルファイル
- `github`: PR / Issue / レビュー（利用時）
- `user-memory`: 永続メモ（利用時）
- （任意）Hugging Face 等、自環境の MCP を追記

## ツール選択ポリシー（要編集）

- ファイル操作 → filesystem 系 MCP または標準ツール
- GitHub → `github` MCP または `gh` CLI
- Excel ブック → プロジェクトの `scripts/*excel*.py`（win32com）と `.cursor/rules/`

## 実行前チェック

- filesystem: 上書き・パス範囲。出力は `temp/`
- github: 既定読取。書込みは owner/repo/branch/path を完全指定
- `feature/*` で作業し PR。本番ブランチ直書き禁止

# Excel / COM / VBA

- 詳細ルールは各プロジェクトの `.cursor/rules/`（例: `excel-com-automation.mdc`, `vba-coding-policy.mdc`, `*-excel-agent.mdc`）。
- 雛形: `bokujuu_cursorsetup/templates/project-rules/excel/`
- `.xlsm` を無目的に Read しない。
- 既存 build/verify スクリプトを実行・修正する（win32com ワンオフは作らない）。
- 静的構造（customUI XML 等）は zip/openpyxl 可。数式・FILTER・VBA は COM。

# パフォーマンス

- 独立タスクは並列可。必要ファイルのみ読む。

# 引用

- コードは `filename.ext:line_start-line_end` 形式を優先。

# 一時ファイル

- 出力は `temp/`。`delete_file` はユーザー明示時のみ。

# パッケージ・Git

- `uv sync` / `uv add`。Git は層 B の git-policy。

# コーディング

- 根本原因から修正。最小変更。
- 3ファイル以上または50行以上は簡易統合テスト。

# Python品質

- 変更後: `uv sync` → `ruff check` → `pyright`（プロジェクトに設定がある場合）。

# 多言語

- **HTML/CSS**: セマンティック・アクセシビリティ・モバイルファースト。
- **VBA**: プロジェクトの `.cursor/rules/vba-coding-policy.mdc`。
- **Python + Excel COM**: プロジェクトの `.cursor/rules/excel-com-automation.mdc` と `AGENTS.md`。
- **M言語**: nullセーフ・`try...otherwise`。
- **ブックマークレット**: 層 B の bookmarklet ルール。

# エラー処理

- 🟢 警告: 記録して継続。
- 🟡 エラー: Lint/型は最大3回リトライ。ビルド/実行失敗は即報告。
- 🔴 致命: 即停止。
- ⛔ セキュリティ: 全停止。

# 最終確認・報告・進捗

- 完了時に指示との整合を確認。
- 軽量は1行、標準は2–3行+ファイル数、重要は影響・リスク・ロールバック。
- 中断/再開は進捗・verify を1ブロックで。skill `agent-handoff-recovery` を推奨。

# 禁止・要承認

- 禁止: UI/UX・スタックの無断変更、重要タスクの承認スキップ。
- 要承認: 破壊的変更、本番影響、外部依存の大幅変更。

Title: MCP Global Execution Rules
Scope: Global

Principles:
- 常に日本語で応答する。
- 指示に対し、MCPサーバーが「設定済み」かつ「利用可能」なら、まずMCPツール実行を最優先する。
- MCPが未設定/利用不可の場合のみ、代替アプローチ（手順提示やローカル実行案）へフォールバックする。
- 破壊的操作は明示指示があるまで行わない。書き込みは既定でプロジェクト直下と `temp/` のみ。

Available MCP Servers (baseline):
- context7: ライブラリ/ドキュメント検索・取得
- excel: Excel読み書き・編集
- playwright: ブラウザ自動化/検証
- filesystem: ローカルファイル操作（読み/書き/列挙）
- memory: セッション間の軽量データ保持
- serena: コードベース探索/シンボル検索/構造化編集（`find_symbol`/`get_symbols_overview`/`replace_symbol_body` 等）
- github: GitHub連携（PR/Issue/レビュー/ファイル作成・更新・ブランチ/ワークフロー）

Tool Selection Policy:
1) 依頼内容を下記にマッピングし、該当サーバーが利用可能なら即時実行する。
   - ドキュメントやAPI仕様の参照/検索 → context7
   - Excelの読取/編集/整形 → excel
   - Web操作/検証/スクレイピング → playwright
   - ファイルの生成/保存/移動/一覧 → filesystem
   - 簡易メモ/進捗の保持 → memory
   - コードの探索/参照/局所編集/リファクタ → serena
   - GitHub上のPR/Issue操作・レビュー・ファイル更新 → github
2) ツール実行前に安全境界を適用する。
   - filesystem: 基本パスはプロジェクト直下。外部パスはユーザー明示指示がある場合のみ。
   - 出力ファイルは `temp/`（既定）に保存。既存ファイル上書きは明示許可がある場合のみ。
   - playwright: 長時間/高負荷のクロールは避け、目的ページ/最小操作に限定。
   - serena: `mcp_serena_activate_project`→`mcp_serena_list_dir`で構造確認後に検索/編集。編集系（`replace_symbol_body`/`insert_*`）は対象ファイルとシンボルを明示。
   - github: 既定は読み取り。書込み（レビュー提出/ファイル更新/ブランチ作成等）は**明示許可**かつ `owner`/`repo`/`pullNumber|branch`/`path` を**完全指定**。
3) 実行結果は要点を簡潔に報告し、必要に応じて再実行/追補を行う。

Fallback Policy (MCP unavailable):
- できる限り代替手順（PowerShell/Python/手動操作手順）を提示。

Quality & Safety:
- 非対話前提で実行フラグを付与（例: npx -y 等）。対話が必要な場合は事前に明示。
- ログ/一時ファイルは `temp/` に保存し、ファイル名に日時を含めて衝突回避。
- 大量変更が想定される操作は、先にプラン提示→ユーザー同意後に実行。

Language & Style:
- 出力は簡潔・箇条書きを基本。重要点は太字強調。
- ファイル/ディレクトリ/関数名はバッククォートで記載。
 
Server-specific Guidelines:

- serena:
   - プロジェクト切替は `mcp_serena_activate_project`。不明時は現在のプロジェクトを使用。
   - 検索は意味検索優先（`mcp_serena_find_symbol`/`mcp_serena_search_for_pattern`）＋**並列実行**を活用。
   - 大規模編集は先に**影響範囲の抽出**→ユーザー承認→編集実行の順。
   - 編集後は `mcp_serena_get_symbols_overview` で整合性を迅速確認。

- github:
   - レビュー関連: 既存レビューへのコメント→`mcp_github_add_comment_to_pending_review`、提出→`mcp_github_create_and_submit_pull_request_review`。
   - 課題管理: Issue作成→`mcp_github_create_issue`、Copilot割当→`mcp_github_assign_copilot_to_issue`。
   - 変更系: ブランチ作成→`mcp_github_create_branch`、ファイル更新→`mcp_github_create_or_update_file`（ブランチ名と `path` 必須）。
   - ワークフロー: 実行取り消し→`mcp_github_cancel_workflow_run`。
   - リンクは `[PR #123](https://github.com/org/repo/pull/123)` 形式を使用。
   - **本番ブランチ直書きは禁止**。`feature/*` ブランチで作業→PR作成が原則。

補足:
- **serena**: 構造化編集系は誤適用防止のため該当シンボルの範囲を必ず確認してから実行してください。
- **github**: 書込み系は「対象の完全指定＋明示許可」が原則です。レビュー提出・ファイル更新・ブランチ作成は事前承認なしでは行いません。
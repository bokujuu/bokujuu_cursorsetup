# ルールインデックス（タスク別参照）

リポジトリ直下の `user-rule-*.md` を、タスク種別に応じて参照する際の目安。閾値は**上限**（通常 3–5 ファイル・大規模 5–8、合計 400–600 行を超えない）。2 ファイルで収まるタスクはそのままでよい。該当セクション抽出前提。

- **Python**: cursor-integrated → python-coding-policy → git-policy
- **COM/Excel**: cursor-integrated → com-automation → python-coding-policy（エンコーディング）
- **VBA**: cursor-integrated → vba-coding-policy
- **Git**: git-policy → cursor-integrated（要約のみ）
- **フロント/ブックマークレット**: cursor-integrated → bookmarklet-best-practices → git-policy（必要時）
- **ルール作成**: rule-creation-policy → cursor-integrated（スタイル）
- **Codex レビュー**: codex-mcp-strategy → cursor-integrated（MCP要約）

長大ファイル（com-automation / cursor-integrated）は該当セクションのみ渡す。旧ルールは [docs/old-rules/](old-rules/) を参照。

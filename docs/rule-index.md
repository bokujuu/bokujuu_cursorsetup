# ルールインデックス（タスク別参照）

`user-rules/` 内の `user-rule-*.md` を、タスク種別に応じて参照する際の目安です。

適用の考え方（常時貼り付け vs タスク時参照）は [user-rules-guide.md](user-rules-guide.md) を参照してください。

## 行数の目安（2026/06/01 時点）

| ファイル | 行数 | 層 |
|----------|------|-----|
| `user-rule-cursor-integrated.md` | 約210 | コア |
| `user-rule-git-policy.md` | 約128 | 専門 |
| `user-rule-python-coding-policy.md` | 約130 | 専門 |
| `user-rule-vba-coding-policy.md` | 約246 | 専門 |
| `user-rule-com-automation.md` | 約302 | 専門 |
| `user-rule-codex-mcp-strategy.md` | 約48 | 専門 |
| `user-rule-rule-creation-policy.md` | 約62 | 専門 |
| `user-rule-jst-date.md` | 約70 | 専門 |
| `user-rule-bookmarklet-best-practices.md` | 約31 | 専門 |
| `user-rule-ahkv2-coding-policy.md` | 約81 | 専門 |

**全ファイルを Settings に貼ると約1,300行**になり、エージェントのコンテキスト上限（目安 400–600 行）を超えやすいです。

## タスク別の参照順（上限: 通常 3 ファイル・合計 400–600 行）

該当セクションのみ渡す前提。2 ファイルで足りるタスクはそのままでよい。

| タスク | 参照順 |
|--------|--------|
| **Python** | cursor-integrated → python-coding-policy → git-policy |
| **COM/Excel** | cursor-integrated → com-automation → python-coding-policy（エンコーディング） |
| **VBA** | cursor-integrated → vba-coding-policy |
| **Git** | git-policy → cursor-integrated（要約のみ） |
| **フロント/ブックマークレット** | cursor-integrated → bookmarklet-best-practices → git-policy（必要時） |
| **ルール作成** | rule-creation-policy → cursor-integrated（スタイル） |
| **Codex レビュー** | codex-mcp-strategy → cursor-integrated（MCP要約） |

長大ファイル（`com-automation` / `cursor-integrated`）は**該当セクションのみ**を渡す。

## 旧構成からの移行

廃止した `.cursor/commands` や旧 MCP ドキュメントとの対応表: [migration-from-legacy.md](migration-from-legacy.md)

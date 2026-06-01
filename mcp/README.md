# MCP 設定

## ファイル

| ファイル | 用途 |
|----------|------|
| `mcp.template.json` | コミット用の雛形（秘密情報なし） |
| `mcp.optional.json` | 任意サーバー（playwright / serena 等） |
| `mcp.json` / `mcp.local.json` | **ローカル専用**（`.gitignore` 済み・コミット禁止） |

## 適用手順（Windows）

1. `%USERPROFILE%\.cursor\mcp.json` をバックアップ（既存がある場合）
2. `mcp.template.json` の内容をマージ（またはコピー）
3. `YOUR_GITHUB_PAT_HERE` を自分の PAT に置換（`Bearer ` プレフィックスを維持）
4. 必要なら `mcp.optional.json` のサーバーを `mcpServers` に追加
5. Cursor を再起動

```powershell
Copy-Item mcp\mcp.template.json $env:USERPROFILE\.cursor\mcp.json
# エディタで PAT と filesystem パスを編集
```

## filesystem のルート

テンプレの `"."` は **Cursor 起動時の cwd** に依存します。安定させるには、許可したいプロジェクトルートの**絶対パス**に差し替えてください。

```json
"args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\CursorPJs\\your-project"]
```

複数ルートが必要な場合は [Model Context Protocol filesystem server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) の仕様に従ってください。

## 同梱サーバー（template）

| 名前 | 用途 | API キー |
|------|------|----------|
| context7 | ライブラリドキュメント | 不要 |
| excel | Excel 読み書き | 不要（uvx） |
| filesystem | ローカルファイル | 不要 |
| memory | セッション間メモ | 不要 |
| github | GitHub 操作 | PAT 必須 |

## 任意サーバー（optional）

`mcp.optional.json` を参照:

- **playwright**: ブラウザ自動化
- **serena**: コードベース分析（uvx / GitHub から取得）

## トラブルシュート

| 現象 | 対処 |
|------|------|
| MCP が一覧に出ない | Cursor 再起動、`mcp.json` の JSON 構文確認 |
| GitHub 401 | `Authorization` が `Bearer <token>` 形式か確認 |
| filesystem が意図しないパスを見る | `"."` を絶対パスに変更 |
| npx / uvx が見つからない | Node.js / `pip install uv` をインストール |

旧 `.cursor/MCP_README.md` の内容は本ファイルに集約しました。

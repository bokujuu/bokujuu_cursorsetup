# MCP 設定

## ファイル

| ファイル | 用途 |
|----------|------|
| `mcp.template.json` | コミット用の雛形（秘密情報なし） |
| `mcp.optional.json` | 任意サーバー（excel / github / playwright / serena 等） |
| `mcp.json` / `mcp.local.json` | **ローカル専用**（`.gitignore` 済み・コミット禁止） |

## Cursor への入れ方

MCP は `.cursorrules` や User Rules では設定できません。Cursor は次のどちらか（または両方）を読みます。

| 場所 | スコープ | 本 repo での位置づけ |
|------|----------|----------------------|
| `%USERPROFILE%\.cursor\mcp.json` | 全プロジェクト（グローバル） | **推奨**。`mcp.template.json` をここへコピー／マージ |
| `<project>/.cursor/mcp.json` | そのプロジェクトのみ | 個別リポ用。本配布 repo のグローバル雛形とは別 |

両方にある同名サーバーは **プロジェクト側が優先**されます。

## 適用手順（Windows）

1. `%USERPROFILE%\.cursor\mcp.json` をバックアップ（既存がある場合）
2. `mcp.template.json` の内容をマージ（またはコピー）
3. 必要なら `mcp.optional.json` のサーバーを `mcpServers` に追加（github は `YOUR_GITHUB_PAT_HERE` を置換）
4. Cursor を再起動（または Reload Window）

```powershell
# 未設定なら雛形をそのまま配置（既存がある場合は上書きしない）
if (-not (Test-Path $env:USERPROFILE\.cursor\mcp.json)) {
  Copy-Item mcp\mcp.template.json $env:USERPROFILE\.cursor\mcp.json
}
# 既にある場合は差分マージ。filesystem の "." は絶対パスへ差し替え推奨
```

`install.ps1 -InstallMcp` でも、グローバル `mcp.json` が **無いときだけ** 雛形を配置します。

## Codex への入れ方

Codex は Cursor の `mcp.json` を読みません。Codex のグローバル MCP は `%USERPROFILE%\.codex\config.toml` の `mcp_servers` で管理します。Cursor 側を変更せずに、Sol / Terra / Luna、filesystem、memory を設定するには次を実行します。

```powershell
.\scripts\install.ps1 -InstallCodex -SkipHooks
```

この処理は次だけを変更します。

- `%USERPROFILE%\.codex\config.toml`: `mcp/codex-mcp.template.toml` の管理ブロックを追加・更新
- `%USERPROFILE%\.codex\AGENTS.md`: `user-rules/user-rule-cursor-communication.md` を完全コピー（既存ファイルは日時付きバックアップ）

Cursor の `%USERPROFILE%\.cursor\mcp.json`、Cursor の hooks、Cursor User Rules は変更しません。Sol / Terra / Luna はレビュー用の別 Codex セッションとして呼び出すため、MCPツール承認を `default_tools_approval_mode = "approve"` にしています。filesystem / memory は追加の承認設定を持たず、クライアントの既定承認に従います。

設定後は Codex を再起動してから、次で確認します。

```powershell
codex mcp list
```

## filesystem のルート

テンプレの `"."` は **Cursor 起動時の cwd** に依存します。安定させるには、許可したいプロジェクトルートの**絶対パス**に差し替えてください。

```json
"args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\CursorPJs\\your-project"]
```

複数ルートが必要な場合は [Model Context Protocol filesystem server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) の仕様に従ってください。

## 同梱サーバー（template）

| 名前 | 用途 | 備考 |
|------|------|------|
| filesystem | ローカルファイル | ルートは絶対パス推奨 |
| memory | セッション間メモ | |
| codex-sol | Codex MCP（GPT-5.6 Sol 既定） | 旗艦・難しいエージェント作業 |
| codex-terra | Codex MCP（GPT-5.6 Terra 既定） | バランス・高ボリューム |
| codex-luna | Codex MCP（GPT-5.6 Luna 既定） | 軽量・日常作業 |

各 Codex エントリは既存の `codex mcp-server` 起動をベースに、`-c model="gpt-5.6-..."` で既定モデルだけ分けています。呼び出し時の `model` 引数で上書きも可能です。Codex 用の TOML 正本は `mcp/codex-mcp.template.toml` です。

**削除したもの**: `context7`（ライブラリ docs 用。不要のため template から外した）

## 任意サーバー（optional）

`mcp.optional.json` を参照:

- **excel**: Excel 読み書き（uvx）
- **github**: GitHub 操作（PAT 必須）
- **playwright**: ブラウザ自動化
- **serena**: コードベース分析（uvx / GitHub から取得）

## トラブルシュート

| 現象 | 対処 |
|------|------|
| MCP が一覧に出ない | Cursor 再起動、`mcp.json` の JSON 構文確認 |
| GitHub 401 | `Authorization` が `Bearer <token>` 形式か確認 |
| filesystem が意図しないパスを見る | `"."` を絶対パスに変更 |
| Codex MCP が起動しない | `codex` が PATH にあるか、`codex doctor` を確認 |
| npx / uvx が見つからない | Node.js / `pip install uv` をインストール |

旧 `.cursor/MCP_README.md` の内容は本ファイルに集約しました。

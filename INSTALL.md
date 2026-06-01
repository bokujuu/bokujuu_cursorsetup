# インストール手順

## 前提

- Windows（手順は PowerShell 想定）
- Git
- Cursor または Codex CLI

## 1. クローン

```powershell
git clone https://github.com/bokujuu/bokujuu_cursorsetup.git
cd bokujuu_cursorsetup
```

## 2. Skills をホームへ配置

```powershell
.\scripts\install.ps1
```

`skills/` 配下が `%USERPROFILE%\.codex\skills\<skill名>\` にコピーされます（既存は上書き）。

Cursor は `.codex\skills` をグローバル skill として読み込みます。

## 3. User Rules を Cursor に反映

1. `user-rules\` 内の `user-rule-*.md` を開く
2. Cursor → **Settings → Rules → User Rules**
3. 運用方針に合わせて貼り付け:
   - **推奨**: `user-rule-cursor-integrated.md` を軸に、必要な専門ルールを追記または分割参照
   - またはタスク別に [docs/rule-index.md](docs/rule-index.md) を見て該当ファイルをコピー

GitHub を更新しても **Settings は自動では変わりません**。

## 4. MCP（任意）

1. `mcp\mcp.template.json` を Cursor の MCP 設定にマージ
2. `YOUR_GITHUB_PAT_HERE` 等を **自分のキーに置換**（コミットしない）
3. ローカル専用なら `mcp\mcp.json` として保存（`.gitignore` 済み）

## 5. 動作確認

- Cursor を再起動
- Agent で skill 名（例: `anti-human-bottleneck`）が認識されるか確認
- 新規チャットで User Rules が効いているか確認

## トラブルシュート

| 現象 | 対処 |
|------|------|
| skill が出てこない | `install.ps1` 再実行、Cursor 再起動 |
| ルールが古い | Settings の User Rules を `user-rules/` で更新 |
| MCP 認証エラー | `mcp.json` のトークン・URL を確認 |

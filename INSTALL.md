# インストール手順

## 前提

- Git
- Cursor または Codex CLI
- **Windows**: PowerShell 5.1+
- **Linux / macOS / WSL**: bash（任意、`install.sh`）

## 1. クローン

```powershell
git clone https://github.com/bokujuu/bokujuu_cursorsetup.git
cd bokujuu_cursorsetup
```

## 2. Skills をホームへ配置

**Windows**

```powershell
.\scripts\install.ps1
```

**Linux / macOS / WSL**

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

`skills/` 配下が `~/.codex/skills/<skill名>/` にコピーされます（既存は上書き）。

Cursor / Codex は `.codex/skills` をグローバル skill として読み込みます。

## 3. User Rules を Cursor に反映

**推奨運用（2 層）** — 詳細は [docs/user-rules-guide.md](docs/user-rules-guide.md):

1. **常時**: `user-rules/user-rule-cursor-integrated.md` のみを Settings → **Rules → User Rules** に貼る
2. **タスク時**: [docs/rule-index.md](docs/rule-index.md) に従い、必要な専門ルールをチャットで参照させる（全10ファイルの一括貼り付けは非推奨）

GitHub を更新しても **Settings は自動では変わりません**。

## 4. MCP（任意）

1. [mcp/README.md](mcp/README.md) を読む
2. `mcp/mcp.template.json` を `%USERPROFILE%\.cursor\mcp.json`（または Cursor 設定の MCP 欄）にマージ
3. `YOUR_GITHUB_PAT_HERE` と **filesystem のルートパス**を自分の環境に置換（コミットしない）
4. 必要なら `mcp/mcp.optional.json` から playwright / serena を追加
5. ローカル専用の `mcp/mcp.json` として保存してもよい（`.gitignore` 済み）

## 5. 動作確認

- Cursor を再起動
- Agent で skill 名（例: `web-research-resolve`）が認識されるか確認
- 新規チャットで User Rules（層 A）が効いているか確認

## 旧構成から移行した場合

`.cursor/commands` や `mcp_enhanced.json` を使っていた場合: [docs/migration-from-legacy.md](docs/migration-from-legacy.md)

## トラブルシュート

| 現象 | 対処 |
|------|------|
| skill が出てこない | `install.ps1` / `install.sh` 再実行、Cursor 再起動 |
| ルールが古い / 長すぎる | [user-rules-guide.md](docs/user-rules-guide.md) の 2 層運用を確認 |
| MCP 認証エラー | `mcp.json` のトークン・URL を確認（`Bearer` 形式） |
| filesystem が変なパスを見る | `mcp.template.json` の `"."` をプロジェクト絶対パスへ変更 |

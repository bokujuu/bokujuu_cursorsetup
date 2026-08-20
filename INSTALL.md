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

`skills/` 配下が `~/.codex/skills/<skill名>/` にコピーされます（同名の既存skillは上書き）。

インストール時には、単純な上書きに加えて管理対象の同期も行われます。

- `~/.codex/skills/.bokujuu-cursorsetup-managed.txt` が、このリポジトリで管理するskill名の一覧です。
- marker に記録されたskillがrepoから消えている場合、そのskillのインストール先ディレクトリを削除します。
- marker がまだ無い既存環境では、installer内のlegacy移行リスト名を初回だけ削除し、完了後にmarkerを作成します。
- marker にないユーザー独自ディレクトリは削除しません（初回移行時のlegacy移行リスト名を除く）。

Cursor / Codex は `.codex/skills` をグローバル skill として読み込みます。

### 2.1 Cursor Hooks（任意）

`install.ps1` は `hooks/*.py`（`handoff-stop-check.py` と `knowledge-capture-nudge.py`）を `%USERPROFILE%\.cursor\hooks\` にコピーし、**既存の `hooks.json` が無い場合のみ** 新規作成します。既にある場合は [hooks/README.md](hooks/README.md) の手動マージを行ってください（`sessionStart` を含む）。

Hook を入れない場合: `.\scripts\install.ps1 -SkipHooks`

## 3. User Rules を Cursor に反映

**推奨運用** — 詳細は [docs/user-rules-guide.md](docs/user-rules-guide.md):

1. **`user-rules/user-rule-cursor-communication.md` のみ**を Settings → **Rules → User Rules** に貼る
2. コーディング規約・MCP 等の技術手順は各リポの `AGENTS.md`、`.cursor/rules/`、skills を参照

GitHub を更新しても **Settings は自動では変わりません**。

## 4. MCP（任意）

MCP は User Rules / `.cursorrules` では設定できません。Cursor と Codex では設定ファイルと登録方法が異なります（詳細は [mcp/README.md](mcp/README.md)）。

### 4.1 Cursor

グローバルは `%USERPROFILE%\.cursor\mcp.json`、プロジェクト単位は `<repo>/.cursor/mcp.json` です。

1. [mcp/README.md](mcp/README.md) を読む
2. 未設定なら `.\scripts\install.ps1 -InstallMcp`（既存 `mcp.json` は上書きしない）、または `mcp/mcp.template.json` を手動マージ
3. **filesystem のルートパス**を自分の環境に置換（コミットしない）
4. 必要なら `mcp/mcp.optional.json` から excel / github / playwright / serena を追加（github は PAT）
5. ローカル専用の `mcp/mcp.json` として保存してもよい（`.gitignore` 済み）

### 4.2 Codex CLI（ユーザー全体）

Codex のグローバル設定は `~/.codex/config.toml`（Windows は `%USERPROFILE%\.codex\config.toml`）です。今回の完全な Codex 設定（Sol / Terra / Luna、filesystem、memory、`AGENTS.md` 同期）には次を使います。Cursor 側は変更しません。

```powershell
.\scripts\install.ps1 -InstallCodex -SkipHooks
```

`codex-mcp.template.toml` の管理対象は Sol / Terra / Luna / filesystem / memory です。既存の `%USERPROFILE%\.codex\AGENTS.md` はバックアップ後、Cursor User Rules 原本と同一内容に更新されます。

既存の先行運用との互換性のため、`codex mcp add` を使う登録経路も残しています。これは MCP 登録だけを行い、`AGENTS.md` は同期しません。既存の同名サーバーは上書きしません。

```powershell
.\scripts\install.ps1 -InstallCodexMcp
```

filesystem MCP も登録する場合:

```powershell
.\scripts\install.ps1 -InstallCodexMcp -CodexFilesystemRoot $env:USERPROFILE
```

**Linux / macOS / WSL**

```bash
bash scripts/install.sh --install-codex-mcp
bash scripts/install.sh --install-codex-mcp --codex-filesystem-root "$HOME"
```

filesystem のルートを指定しない場合は、ファイルアクセスを追加しない安全側の動作になります。登録後は `codex mcp list` で確認し、Codex Desktop / CLI / IDE を再起動してください。

`-InstallCodex` と `-InstallCodexMcp` を併用した場合、管理ブロック側の同名サーバーを優先し、`codex mcp add` は重複登録を行いません。

雛形の既定: filesystem / memory / **codex-sol・codex-terra・codex-luna**（GPT-5.6）。`context7` は含めません。

## 5. 動作確認

1. **機械検証**（install 済みであること）:

   ```powershell
   python scripts\verify_repo_setup.py
   python scripts\verify_loop_kit.py
   ```

   Linux / macOS / WSL: `python3 scripts/verify_repo_setup.py`（`install.sh` 実行後）

2. **手動確認**

   - Cursor を再起動
   - Agent で skill 名（例: `web-research-resolve`）が認識されるか確認
   - 新規チャットで User Rules が効いているか確認
   - （任意）Settings → **Hooks** に handoff 用エントリが表示されるか確認
   - （任意）`agent-handoff-recovery` skill が「期待と違う」等で読み込まれるか確認
   - （任意）`japanese-technical-writing` で短い技術説明ドラフトを作成できるか確認
   - （任意）`natural-japanese` で「もっと自然な日本語に」「AIっぽさを取って」が動作するか確認（`uv` は任意。無い場合は手動チェックリスト）
   - （任意）`cognitive-rhythm-writing` で「緩急を付けて書いて」「平坦な文章を診断して」が動作するか確認
   - （任意）`slide-narration-video` で「全画面スライド解説動画を作って」「Marp＋ナレーション」「対話形式の解説」が動作するか確認（依存 skill も install 済みであること）
   - （任意）`voicevox-theater-video` で「VOICEVOX劇場」「立ち絵つき対話解説」が動作するか確認（親 `slide-narration-video` も install 済みであること）
   - （任意）`japanese-doc-review` で「全観点でレビューして」が動作するか確認
   - （任意）`repo-agent-bootstrap` が「AGENTS.mdをセットアップして」で読み込まれるか確認
   - （任意）`excel-deliverable-quality` が「帳票/取込用CSVを作って」「数式が壊れていないか確認して」「見た目/色/レイアウトを整えて」で読み込まれるか確認
   - （任意）`power-query-refactor` が「M を整理」「コメント追加」「Table.Buffer」「再計算抑制」で読み込まれるか確認
   - （任意）`md-html-visual-doc` で「MD だと読みにくい比較・ギャラリーを HTML で見やすく」が動作し、相対リンクと再生成情報を含む成果になるか確認
   - （任意）`requirement-aligned-fixtures` が「ダミーデータを作って」「fixture を設計して」で読み込まれるか確認

## 旧構成から移行した場合

`.cursor/commands` や `mcp_enhanced.json` を使っていた場合: [docs/migration-from-legacy.md](docs/migration-from-legacy.md)

## トラブルシュート

| 現象 | 対処 |
|------|------|
| skill が出てこない | `install.ps1` / `install.sh` 再実行、Cursor 再起動 |
| ルールが古い / 長すぎる | [user-rules-guide.md](docs/user-rules-guide.md) の 1 ファイル運用を確認 |
| MCP 認証エラー | `mcp.json` のトークン・URL を確認（`Bearer` 形式） |
| filesystem が変なパスを見る | `mcp.template.json` の `"."` をプロジェクト絶対パスへ変更 |
| Codex MCP（sol/terra/luna）が無い | 完全設定は `install.ps1 -InstallCodex -SkipHooks`、既存互換経路は `install.ps1 -InstallCodexMcp` または `install.sh --install-codex-mcp`。`codex mcp list` と Codex 再起動も確認 |

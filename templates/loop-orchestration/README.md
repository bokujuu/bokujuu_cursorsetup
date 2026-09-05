# loop-orchestration テンプレート

現行方針: 通常作業はエージェントの内側ループを使います。本キットは旧Cursor環境の手動展開用で、グローバルにインストールしません。モデルと継続の判断は [model-routing.md](../../docs/model-routing.md)。
Cursor で **ループエンジニアリング**（外側オーケストレータ + fresh context + 検証ゲート）を再現するための一式です。`repo-agent-bootstrap` で整えた AGENTS.md / registry とセットで使います。

## 4 層スタック（推奨順）

| Tier | 方式 | 用途 |
|------|------|------|
| **1** | **A** — `ralph.ps1` + `cursor-agent -p` | 本番ループ（最小依存・Windows 実証済み） |
| **2** | **F** — `@cursor/sdk` TypeScript `ralph.mjs` | SDK でストリーム・run 管理が必要なとき（Windows で安定） |
| **2** | **B** — Python `AsyncClient.launch_bridge()` | 既存 Python パイプライン向け（**同期 `Client` は禁止**） |
| **3** | **C** — 手動 Bridge + env | デバッグ・sidecar |
| **4** | **D** — WSL + `ralph.sh` | bash 資産があるときのみ（CLI/API キー整備が前提） |
| **5** | **E** — upstream 修正待ち | Python 同期 Bridge のみ |

詳細: [docs/loop-engineering.md](../../docs/loop-engineering.md)

## コピー手順

1. 本フォルダを対象リポの `loop/`（任意の名前）にコピー
2. `PROMPT.md.template` → `PROMPT.md`、`ROADMAP.md.template` → `ROADMAP.md` にリネームして編集
3. `progress.txt` を用意（`progress.txt.template` をコピー可）
4. 検証コマンドを `PROMPT.md` と `ROADMAP.md` に具体化
5. **5 秒スモーク**（`run-once.ps1` または `sdk-smoke.ps1`）→ 本番 `ralph.ps1`

## モデル方針

- 既定は **`composer-2.5`**（多数反復向け。`-fast` 系は既定にしない）
- Grok 併用時は上書き: `run-once.ps1 -Model grok-4.5-xhigh` / `MODEL=…` / `CURSOR_MODEL=…`
- CLI account default が fast でもスクリプト側で品質系 slug を明示する
- 詳細: [docs/model-routing.md](../../docs/model-routing.md)

## Windows 必須注意

- **PowerShell パイプ禁止**: `Get-Content PROMPT.md | cursor-agent -p` はプロンプトが渡らない
- **正**: `run-once.ps1`（変数に読み込み引数渡し）
- **Python SDK 同期 `Client.launch_bridge()` は Windows で失敗**（WinError 10038）。TypeScript `@cursor/sdk` または Python `AsyncClient` を使う

## ファイル一覧

| ファイル | 役割 |
|----------|------|
| `run-once.ps1` | CLI 1 反復（Tier 1） |
| `ralph.ps1` | 外側ループ（Tier 1） |
| `ralph.mjs` | SDK ループ（Tier 2 F） |
| `ralph.sh` | bash ループ（Tier 4 D / Linux） |
| `start-bridge.ps1` | 手動 Bridge（Tier 3 C） |
| `PROMPT.md.template` | エージェント向けプロンプト雛形 |
| `ROADMAP.md.template` | タスク一覧（passes フラグ） |
| `progress.txt.template` | 反復ログ |
| `prd.json.template` | snarktank 互換（任意） |
| `facets/` | Faceted prompting 雛形（persona / policy / knowledge / instruction / output-contract） |

## Faceted prompting（任意）

レビューと実装でコンテキストを分けたいときは [facets/README.md](facets/README.md) を `loop/facets/` にコピーし、`PROMPT-faceted.md.template` をベースにする。設計: [docs/pr/004-qa-faceted-adoption.md](../../docs/pr/004-qa-faceted-adoption.md)。

## 関連 skill

- `repo-agent-bootstrap` — AGENTS.md / registry / verify

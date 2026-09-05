# ループエンジニアリング（Cursor）

現行方針: 通常作業はエージェントの内側ループを使います。本キットは旧Cursor環境の手動展開用で、グローバルにインストールしません。モデルと継続の判断は [model-routing.md](model-routing.md)。
外側オーケストレータがエージェントを **反復呼び出し**し、各反復は **fresh context**。状態はチャットではなく **git / ファイル** に残す（Ralph パターン）。


テンプレ実体: [templates/loop-orchestration/](../templates/loop-orchestration/)

## 5 要素

| # | 要素 | 役割 |
|---|------|------|
| 1 | オーケストレータ | `ralph.ps1` / `ralph.mjs` / Automations / `/loop` |
| 2 | `PROMPT.md` | 反復ごとに渡す指示 |
| 3 | ファイルメモリ | `ROADMAP.md`, `progress.txt`, `loop-journal.txt` |
| 4 | ステアリング | `AGENTS.md`, skills, verify コマンド |
| 5 | 完了シグナル | 検証 exit 0 + `<promise>COMPLETE</promise>` |

## Faceted prompting（任意）

外側ループは同じまま、**反復ごとのプロンプト**を 5 種 facet に分割できる（着想: [TAKT](https://github.com/nrslib/takt)）。

| Facet | 役割 |
|-------|------|
| persona | 実装者 / レビュアー |
| policy | 編集可否・スコープ |
| knowledge | リポ事実・SoT（手順は含めない） |
| instruction | この反復のステップ |
| output-contract | `COMPLETE` / `REVIEW_PASS` 等 |

雛形: [templates/loop-orchestration/facets/](../templates/loop-orchestration/facets/)。設計: [docs/pr/004-qa-faceted-adoption.md](pr/004-qa-faceted-adoption.md)。

単一 `PROMPT.md` で足りる場合は facet を使わなくてよい。implement と review のコンテキスト分離が必要なときに有効。

## Cursor 4 層スタック

| 層 | 手段 | fresh context | 向き |
|----|------|---------------|------|
| ① | `/loop` | なし（同一セッション） | 学習・定期確認 |
| ② | Automations | 実行ごとに新規 | クラウド repo・スケジュール |
| ③ | `cursor-agent -p` + shell | あり | **本キット標準（Tier 1）** |
| ④ | SDK | あり | ストリーム・run 管理（**Tier 2**） |

`/multitask` は **並列** でありループの代替ではない。

## 推奨スタック（SDK 安定優先）

**方針**: SDK を使うときは「動くか試す」より **実証済み経路だけをキット化**する。

| Tier | ID | 方式 | 安定性（Windows） | 用途 |
|------|-----|------|-------------------|------|
| **1** | **A** | `cursor-agent -p` + `ralph.ps1` | 実証済み | デフォルト本番ループ |
| **2** | **F** | `@cursor/sdk` TypeScript `ralph.mjs` | **実証済み**（workaround F） | SDK 第一候補（Windows） |
| **2** | **B** | Python `AsyncClient.launch_bridge()` | 実証済み | Python 既存資産向け |
| **3** | **C** | 手動 Bridge + env | 実証済み | デバッグ・sidecar |
| **4** | **D** | WSL + `ralph.sh` | 要整備（CLI 版・API キー） | bash 資産があるときのみ |
| **5** | **E** | upstream `cursor-sdk` 修正 | 未 | Python **同期** `Client` 専用 |

### 使わない（Windows）

| 方式 | 理由 |
|------|------|
| Python 同期 `Client.launch_bridge()` / `Bridge.launch()` | stderr パイプ + `select` → **WinError 10038** |
| PowerShell パイプ `Get-Content PROMPT.md \| cursor-agent -p` | プロンプト未伝達 |
| WSL を「Windows 問題のデフォルト回避」 | ネイティブで A / F が既に動く。二重管理コスト |

## SDK Bridge — 技術メモ

```
スクリプト → cursor-sdk-bridge (Node) → ローカルエージェント
```

失敗箇所は **Bridge 本体ではなく Python 同期の discovery 読み取り**。

| 実装 | discovery | Windows |
|------|-----------|---------|
| Python sync `_bridge.py` | `selectors.select` on pipe | NG |
| Python async `_async_bridge.py` | `asyncio` stderr read | OK |
| TypeScript `@cursor/sdk` | Node `child_process` streams | OK |
| CLI `cursor-agent -p` | Bridge 非経由 | OK |

参考: [Python select — Windows](https://docs.python.org/3/library/select.html#select.select), [anthropics/skills#1061](https://github.com/anthropics/skills/issues/1061)

## モデル方針

- ラッパー既定は **`composer-2.5`**（多数反復のコスト効率。coding specialist）
- 対話メインや難所は **Grok**（例: `grok-4.5-xhigh`）を `-Model` / `MODEL` / `CURSOR_MODEL` で上書き
- `-fast` はモデル slug の一部であり CLI フラグではない。ループ既定に fast 系を使わない
- account default が fast でもスクリプトで品質系 slug を明示する
- 使い分けの SoT: [model-routing.md](model-routing.md)

## 展開フロー

1. `install.ps1` → グローバル skills
2. 対象 repo で `repo-agent-bootstrap` → `AGENTS.md` / registry / verify
3. `templates/loop-orchestration/` を `loop/` にコピー → `PROMPT.md` / `ROADMAP.md` 編集
4. （任意）`loop/facets/` をコピー — **Faceted prompting**（implement / review でプロンプト分離）。[facets/README.md](../templates/loop-orchestration/facets/README.md)
5. 5 秒スモーク → `ralph.ps1` または `ralph.mjs`
6. `practice-registry.json` に verify を登録

## 検証

```powershell
# キット同梱チェック（リポ root）
python scripts/verify_loop_kit.py

# SDK スモーク（CURSOR_API_KEY 要）
.\scripts\sdk-smoke.ps1
```

## 参考

- [Loop Engineering — Addy Osmani](https://addyo.substack.com/p/loop-engineering)
- [Cursor CLI Headless](https://cursor.com/docs/cli/headless)
- [Cursor TypeScript SDK](https://cursor.com/docs/sdk/typescript)
- [snarktank/ralph](https://github.com/snarktank/ralph)

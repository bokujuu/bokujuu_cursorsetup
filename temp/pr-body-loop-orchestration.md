# PR 010: 汎用ループ・オーケストレーションキット

**ブランチ**: `feature/loop-orchestration`（`feature/repo-agent-bootstrap` 上に積む）  
**関連**: `repo-agent-bootstrap`, `ralph-loop`, `anti-human-bottleneck`

## Summary

- Cursor の **ループエンジニアリング**を再現可能な **テンプレート一式**として同梱
- **SDK 安定優先**: 実証済み経路のみ文書化・同梱（**TypeScript `@cursor/sdk` を Windows SDK 第一候補**）
- **既定モデル**: `composer-2.5`（`-fast` 系は使わない）
- `repo-agent-bootstrap` とセットの汎用セットアップ

## SDK 推奨スタック（安定優先）

| Tier | ID | 方式 | Windows | キットでの位置づけ |
|------|-----|------|---------|-------------------|
| **1** | **A** | `cursor-agent -p` + `ralph.ps1` | 実証済み | **デフォルト本番** |
| **2** | **F** | `@cursor/sdk` + `ralph.mjs` | **実証済み** | **SDK 第一候補** |
| **2** | **B** | Python `AsyncClient.launch_bridge()` | 実証済み | Python 資産向け |
| **3** | **C** | 手動 Bridge + env | 実証済み | デバッグのみ |
| **4** | **D** | WSL + `ralph.sh` | 要整備 | bash 資産があるときのみ |
| **5** | **E** | upstream 修正 | 未 | Python 同期専用 |

### 禁止（Windows）

- Python 同期 `Client.launch_bridge()` → WinError 10038
- `Get-Content PROMPT.md | cursor-agent -p` → プロンプト未伝達
- WSL をデフォルト回避策にしない（ネイティブ A / F で足りる）

## 背景（Vault PoC）

| 実験 | 結果 |
|------|------|
| `/loop` + 5秒スモーク | OK |
| `cursor-agent -p` + 引数渡し | OK |
| `ralph.ps1 -MaxIterations 3` | OK |
| Python sync `Bridge.launch` | **NG** (10038) |
| Python `AsyncClient` | OK |
| 手動 Bridge + env | OK |
| **`@cursor/sdk` TS `Agent.create` + `send`** | **OK** |

## 追加ファイル

```
templates/loop-orchestration/
├── README.md, PROMPT.md.template, ROADMAP.md.template, progress.txt.template, prd.json.template
├── run-once.ps1, ralph.ps1          # Tier 1 (A)
├── ralph.mjs                        # Tier 2 (F)
├── ralph.sh                         # Tier 4 (D)
└── start-bridge.ps1                 # Tier 3 (C)

scripts/verify_loop_kit.py
scripts/sdk-smoke.ps1

docs/loop-engineering.md
skills/ralph-loop/references/operational-guide.md
docs/pr/010-loop-orchestration-kit.md
```

## Test plan

- [ ] `python scripts/verify_loop_kit.py`
- [ ] `run-once.ps1` + `--model composer-2.5`
- [ ] `ralph.ps1 -MaxIterations 2`
- [ ] `MAX_ITERATIONS=1 node templates/loop-orchestration/ralph.mjs`
- [ ] `sdk-smoke.ps1`（CLI + TS、任意で Python async）

## フォローアップ

- cursor-sdk Python sync の upstream issue
- GitHub Actions で `verify_loop_kit.py`

## 参考

- [loop-engineering.md](../loop-engineering.md)
- Obsidian Vault: `2026-06-15-ループエンジニアリング学習メモ.md`

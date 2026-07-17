# Ralph loop — 運用ガイド

`ralph-loop` skill の **実装側** 手順。概念は [SKILL.md](../SKILL.md)、アーキテクチャは [docs/loop-engineering.md](../../../docs/loop-engineering.md)。

## 前提

- グローバル skills: `ralph-loop`, `repo-agent-bootstrap`（`install.ps1` 済み）。承認境界は User Rules / `anti-human-bottleneck`（任意）
- 対象 repo: `CURSOR_API_KEY`, `cursor-agent` on PATH
- SDK 利用時: **Tier 2 F（TypeScript）または Tier 2 B（Python async）のみ**

## 1. エージェント基盤（repo-agent-bootstrap）

1. `AGENTS.md` / `.codex/practice-registry.json` / verify スクリプトを整備
2. 検証コマンドを `ROADMAP.md` と `PROMPT.md` に書く（例: `python scripts/verify_*.py`）

## 2. テンプレ展開

```powershell
Copy-Item -Recurse path\to\bokujuu_cursorsetup\templates\loop-orchestration .\loop
cd loop
Copy-Item PROMPT.md.template PROMPT.md
Copy-Item ROADMAP.md.template ROADMAP.md
Copy-Item progress.txt.template progress.txt
# PROMPT.md / ROADMAP.md の {{VERIFY_COMMAND}} 等を編集
```

## 3. スモーク（本番前必須）

```powershell
# Tier 1 — 5 秒相当の 1 反復
.\run-once.ps1

# Tier 2 F — SDK（Node + @cursor/sdk）
npm install @cursor/sdk   # 対象 repo または kit 同梱 dir
node ralph.mjs            # MAX_ITERATIONS=1 で短く試すのも可

# リポ同梱 verify
python ..\scripts\verify_loop_kit.py
```

`scripts/sdk-smoke.ps1`（cursorsetup リポ root）で CLI + TS + Python async を一括確認可。

## 4. 本番ループ

```powershell
# Tier 1（推奨デフォルト）
.\ralph.ps1 -MaxIterations 10 -StopOnComplete

# Tier 2 F（SDK・反復ごとに fresh agent が要る場合は run-once 相当をループ内で設計）
$env:MAX_ITERATIONS = "10"
$env:STOP_ON_COMPLETE = "1"
node ralph.mjs
```

## 5. 完了の定義

- 検証コマンドが **exit 0**
- `ROADMAP.md` の該当タスクが `passes: true`
- エージェント出力に `<promise>COMPLETE</promise>`（全タスク完了時）

人間の承認ではなく **テスト/verify** で完了を決める（Ralph の原則）。

## 6. トラブルシュート

| 症状 | 対処 |
|------|------|
| `No prompt provided for print mode` | パイプ禁止 → `run-once.ps1` |
| `WinError 10038` on Bridge | Python 同期 Client を使っている → **F または B** |
| WSL で auth エラー | `CURSOR_API_KEY` を WSL に設定。CLI を最新化 |
| `*-fast` で動く | ラッパーに品質系 `--model`（既定 `composer-2.5`）があるか確認 |
| Grok で1反復だけ回したい | `run-once.ps1 -Model grok-4.5-xhigh` / `MODEL=` / `CURSOR_MODEL=`（[model-routing.md](../../../docs/model-routing.md)） |

## 7. registry 登録例

`practice-registry.json` の `verification_commands` に対象 repo の verify を追加し、`ralph-loop` skill_path と併記する。

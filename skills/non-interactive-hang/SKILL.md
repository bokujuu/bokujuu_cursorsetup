---
name: non-interactive-hang
description: >-
  エージェントが検証を素早く回すための非対話ループ。人間用 pause は維持しつつ NO_PAUSE +
  実測キャリブレーション型 timeout（p95×1.5+5）と秒単位の watchdog 自己検証。
  .bat 誤実行・Shell 無期限待ち・Excel COM の遅い verify 設計で使う。
---

# non-interactive-hang — 素早いエージェント検証ループ

方針 SoT: [docs/fast-agent-test-loop.md](../../docs/fast-agent-test-loop.md)

## いつ使うか

- エージェントが `.bat` や対話付きスクリプトで verify するとき
- Shell が `Press any key…` で無期限ブロックした疑い
- 固定 600s timeout で「遅いが成功」な verify を何度も回したいとき
- Excel COM 自動化の macro timeout / Silent 設計を見直すとき

## 核心（3 行）

1. **人間とエージェントの入口を分ける** — pause は人間用だけ。エージェントは `scripts/ci/run_*.py` または `NO_PAUSE=1` + watchdog。
2. **成功の上限は実測** — `timeout_sec = ceil(p95 × 1.5) + 5`。計測コマンド = 検証コマンド。
3. **watchdog 自体を検証** — 導入・変更時に `test_watchdog.py`（Excel 不要）を通す。通常の verify ごとには繰り返さない。

## 手順（プロジェクトに展開済みの場合）

1. **高速自己検証**（導入・watchdog変更・実行環境変更時）

   ```powershell
   python scripts/ci/test_watchdog.py
   ```

   期待: `[SUMMARY] OK=3 FAIL=0`（〜20s）

2. **キャリブレーション**（verify 変更・マシン変更後）

   ```powershell
   python scripts/ci/calibrate_timeout.py --key <key> --samples 3
   ```

3. **watchdog 付き bat 検証**（どうしても bat を叩くときのみ）

   ```powershell
   python scripts/ci/run_with_watchdog.py --key <key> -- cmd /c your-build.bat
   ```

4. **解釈**
   - exit **0** … 正常
   - exit **124** … pause 検知 or wall-clock 超過 → cleanup 後、ci 入口へ切り替え

## レイヤー（優先順）

| 層 | 内容 |
|----|------|
| A 予防 | 非対話 ci、`NO_PAUSE`、Excel `*Silent` + macro timeout |
| B 検知 | bat 時のみ pause 文言 + 実測 wall-clock |
| C 回復 | kill、プロジェクト cleanup、124 |

COM に stdout 監視は**広げない**（MsgBox はコンソールに出ない）。

## 未展開リポへの導入

1. [templates/project-ci/non-interactive-hang/](../../templates/project-ci/non-interactive-hang/) を `scripts/ci/` にコピー
2. `calibrate_presets.json` と `timeouts.json` をプロジェクトの bat に合わせて編集
3. `AGENTS.md` にエージェント一行（`.bat` を使わない / watchdog キー名）を追記

## 落とし穴

- **`run_build.py` の時間で `.bat` timeout を決めない**
- **`pause` 単語**はログ FP。検知はプロンプト全文のみ
- **実 `pause` はパイプに出ない**ことがある → wall-clock が主、文言は補助
- **キャリブレーションは成功完走のみ**。失敗時は先にビルドを直す

## 合格基準

- `test_watchdog.py` → OK=3
- （任意）キャリブレ後 `run_with_watchdog.py --key <key>` で本番 verify 成功

## メモ

[references/skill-memory.md](references/skill-memory.md)

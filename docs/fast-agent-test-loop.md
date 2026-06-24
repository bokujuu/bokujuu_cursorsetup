# 素早くテストを回す — エージェント向け検証ループ

更新: 2026/06/22  
着想元: Excel COM 帳票リポでの `.bat` pause ハング対策（実装例: `excel-approval-platform-customer-registration`）

---

## 何が問題か

エージェントが Shell で検証するとき、**成功経路は遅いだけ**だが、**失敗経路は無限待ち**になりやすい。

| 種別 | 典型 | エージェントへの影響 |
|------|------|---------------------|
| `.bat` 失敗時の `pause` | Press any key… | プロセス未終了 → Shell がブロック |
| Excel COM の `MsgBox` | モーダル | `Application.Run` が戻らない |
| 固定 600s timeout | 正常完了は 60s なのに 10 分待つ | **遅いテスト＝回数が減る** |

「テストを速く回す」はマシンを速くすることだけではない。**ハングを秒単位で切り、成功経路の上限を実測で決める**ことで、同じセッションで verify を何度も回せる。

---

## 三原則（優先順位）

1. **予防（Layer A）** — エージェントは非対話入口だけ使う。人間用 `pause` は残す。
2. **実測キャリブレーション** — 固定長 timeout より `p95 × 1.5 + 5` で成功経路の上限を決める。
3. **秒で終わる自己検証** — 重い E2E の前に、watchdog 単体を Excel なしで 3 本回す。

補助として **pause 文言検知**（bat 専用）と **exit 124**（ハング系の共通終了コード）を使う。COM には stdout 監視を広げない（MsgBox はコンソールに出ない）。

---

## 二系統（人間とエージェントを分ける）

| 利用者 | 入口 | 失敗時 |
|--------|------|--------|
| 人間 | `.\build.bat`（`pause` あり） | 画面を読んで修正 |
| エージェント | `python scripts/ci/run_build.py` または watchdog 付き bat | `NO_PAUSE=1`、timeout、124 で即切り |

**壊してはいけないこと**: 人間の運用を「エージェント用に pause 削除」で直さない。ガード変数（`NO_PAUSE` / `CI` / `CURSOR_AGENT`）で分岐する。

---

## 実測キャリブレーション

### 公式

```text
timeout_sec = ceil(p95_seconds × 1.5) + 5
```

- `p95` … 同一マシンで **3 回以上**の成功完走 wall-clock の 95 パーセンタイル
- `× 1.5` … 冷起動・RPC 再試行のゆらぎ
- `+ 5` … 起動・kill の固定オーバーヘッド

### 鉄則: 計測対象 = 検証対象

| 誤り | なぜダメか |
|------|-----------|
| `run_build.py` の時間で `.bat` の timeout を決める | 入口が違えば秒数も違う |
| 1 回だけ計測して 1.5 倍 | 外れ値に弱い |
| 失敗時の `pause` を実測 timeout だけで待つ | 成功 60s なら失敗で 90s 待つことになり無駄 |

失敗時の無限 `pause` は **文言検知（数秒 grace）** で切る。成功の上限は **キャリブレーション値**。

### 記録

`scripts/ci/timeouts.json` に key ごとに `command` / `env` / `samples_sec` / `timeout_sec` を残す。verify シナリオ増・マシン変更時に再計測。

---

## レイヤー整理

### Layer A — 予防（必須・コスト最小）

- エージェント SoT: `scripts/ci/run_*.py`（対話なし）
- bat: `if not defined NO_PAUSE pause` 等
- Excel: `*Silent` エントリポイント、`WF_TEST=1`、macro 60s timeout（既存 COM 検証と同型）

### Layer B — 検知（bat 誤実行の保険）

`run_with_watchdog.py`:

- stdout/stderr tail で `press any key to continue` / `続行するには何かキーを` のみ（単語 `pause` は FP）
- bat/cmd 実行時のみ自動 ON
- マッチ後 5s grace → `taskkill /F /T` → exit **124**

注意: Windows の実 `pause` は **CON 直書き**でパイプに出ないことがある。本番防御は **実測 wall-clock**、文言検知は補助（テスト用 fixture は echo でプロンプトを再現）。

### Layer C — 回復

- exit 124 → ログに `[HANG]`、必要ならプロジェクト固有の cleanup（Excel force-quit 等）
- エージェントは 124 を「対話待ち」と解釈し、ci 入口へ切り替えて retry

---

## 速い検証ループ（推奨順）

```text
1. python scripts/ci/test_watchdog.py     # 〜20s、Excel 不要 → OK=3
2. python scripts/ci/calibrate_timeout.py --key <key> --samples 3   # 必要時
3. python scripts/ci/run_with_watchdog.py --key <key> -- cmd /c build.bat
4. （プロジェクトの）本番 COM / E2E verify
```

**1 を飛ばして 4 から始めない。** watchdog が壊れていると 4 が何時間もブロックする。

テンプレ: [templates/project-ci/non-interactive-hang/](../templates/project-ci/non-interactive-hang/)

---

## Excel COM への当てはめ（同型）

| 対象 | 検知 | 備考 |
|------|------|------|
| bat `pause` | stdout パターン + wall-clock | bat 時のみ |
| `Application.Run` | 既存 macro timeout（例 60s） | stdout 監視はしない |
| Outlook / 本番 MsgBox | 自動化対象外 | `[SKIP] manual` |

verify 全体の上限は `.bat` キャリブレーションに含め、個別 macro は短い timeout を維持する。

---

## グローバル skill / プロジェクト展開

| 層 | パス |
|----|------|
| 考え方（本 doc） | `docs/fast-agent-test-loop.md` |
| エージェント手順 | skill `non-interactive-hang`（`skills/non-interactive-hang/`） |
| リポ実装雛形 | `templates/project-ci/non-interactive-hang/` |
| Excel 固有 | `templates/project-rules/excel/excel-com-automation.mdc` |

---

## 評価基準（導入できているか）

- [ ] エージェント向け非対話入口が `AGENTS.md` に一行で書いてある
- [ ] `test_watchdog.py` が 20s 以内に PASS（重い verify の前に毎回）
- [ ] `timeouts.json` が実測由来（placeholder 600s だけではない）
- [ ] 人間用 bat の `pause` が残っている

---

## 関連

- skill: [skills/non-interactive-hang/SKILL.md](../skills/non-interactive-hang/SKILL.md)
- PR 設計: [docs/pr/011-fast-agent-test-loop.md](pr/011-fast-agent-test-loop.md)

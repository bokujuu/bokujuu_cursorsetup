# non-interactive-hang — プロジェクト CI 雛形

`scripts/ci/` へコピーして使う。リポルートを `WATCHDOG_CWD`（未設定時は本ファイルから 2 段上）とする。

## コピー手順

```powershell
Copy-Item -Recurse templates\project-ci\non-interactive-hang\* scripts\ci\
```

1. `calibrate_presets.json.example` → `calibrate_presets.json`（キーと command を編集）
2. `timeouts.json.example` → `timeouts.json`（キャリブレーション後に上書き）
3. 人間用 `.bat` に `if not defined NO_PAUSE pause` を追加（未実装なら）
4. `AGENTS.md` に「エージェントは `python scripts/ci/run_build.py`」等を一行追記

## 検証順（速い順）

```powershell
python scripts/ci/test_watchdog.py
python scripts/ci/calibrate_timeout.py --key build_bat --samples 3
python scripts/ci/run_with_watchdog.py --key build_bat -- cmd /c your-build.bat
```

## 環境変数（任意）

| 変数 | 意味 |
|------|------|
| `WATCHDOG_CWD` | 子プロセスの cwd（既定: リポルート想定） |
| `WATCHDOG_TIMEOUT_SEC` | 全体 timeout 上書き |
| `WATCHDOG_HANG_CLEANUP` | hang 時に実行するスクリプト（例: Excel force-quit `.bat`） |
| `NO_PAUSE` | bat 側が pause をスキップするガード |

考え方: [docs/fast-agent-test-loop.md](../../docs/fast-agent-test-loop.md)

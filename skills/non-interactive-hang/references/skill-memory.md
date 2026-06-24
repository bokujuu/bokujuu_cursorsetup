# skill-memory — non-interactive-hang

- 2026-06-22: 着想は Excel 帳票で `.bat` pause がエージェントを無期限ブロックした事例。削除ではなく **人間 pause 維持 + NO_PAUSE + watchdog**。
- 2026-06-22: **素早く回す**＝固定 600s より **実測 p95×1.5+5**。計測は検証と同じコマンドで行う。
- 2026-06-22: Windows 実 `pause` は CON 直書きでパイプ検知不可。**test_watchdog.py** で秒検証し、本番は wall-clock が主防御。

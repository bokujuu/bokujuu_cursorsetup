# skill-memory — voicevox-theater-video

- 2026/08/01: 親 `slide-narration-video` から劇場合成を分離。口パクは時間交互ではなく WAV RMS＋遅れ（現行 0.1s）。字幕は行ごと縁→字だと下行が上行白を食うため全行3パス必須。登場は AviUtl「弾む」速さ≈6.7・高さ8＋遅いX。劇場 fps 既定は 30。スライド文字のグレーハローは Marp ClearType／LANCZOS 縮小が主因 → Pillow 直描き推奨。
- 2026/08/01: 字幕は `narration` 原文（`3.2` / `$\\hbar$` / `SU(2)`）。TTS カナを字幕に出さない。`$...$` は mathtext ビットマップ＋共通縁取り。退場は Y 回転（scale_x=cos）→導入と同パラメータで歩き＋フェードアウト。出典図転載と先頭スライドの参考URLは親 skill（figures-and-math）へ。
- 2026/08/01 (Sol xhigh #2): `第3章` の `3` 縮小は `[0-9]` を latin 扱いした誤分類。縮小は latin 識別子一塊のみ。
- 2026/08/01 (Sol xhigh #3): 主因は GenShin の実インク（`３` でも h≈38 vs 第≈47）。全角化は高さ補正にならない。半角のまま `第`/`章` 基準で等方 boost。小文字 Latin は `あ` 基準＋cap≈1.45。`$` 未処理に光学補正をかけない。規約は `subtitle-typography.md`。

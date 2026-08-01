# skill-memory — voicevox-theater-video

- 2026/08/01: 親 `slide-narration-video` から劇場合成を分離。口パクは時間交互ではなく WAV RMS＋遅れ（現行 0.1s）。字幕は行ごと縁→字だと下行が上行白を食うため全行3パス必須。登場は AviUtl「弾む」速さ≈6.7・高さ8＋遅いX。劇場 fps 既定は 30。スライド文字のグレーハローは Marp ClearType／LANCZOS 縮小が主因 → Pillow 直描き推奨。
- 2026/08/01: 字幕は `narration` 原文（`3.2` / `$\\hbar$` / `SU(2)`）。TTS カナを字幕に出さない。`$...$` は mathtext ビットマップ＋共通縁取り。退場は Y 回転（scale_x=cos）→導入と同パラメータで歩き＋フェードアウト。出典図転載と先頭スライドの参考URLは親 skill（figures-and-math）へ。
- 2026/08/01 (Sol xhigh): 縁の矩形化＝余白なし alpha への MaxFilter＋NEAREST 拡大が主因。`$J$` 巨大化＝mathtext 高 dpi を字幕 48px に合わせず並べたこと。対策は単純記号の同一フォント flatten＋円形ダイレーション縁取り、ラテン 0.72 倍、複雑式のみ高さ合わせ＋`outer_w+8` 余白。

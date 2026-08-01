# skill-memory — voicevox-theater-video

- 2026/08/01 20:39: 親 `slide-narration-video` から劇場合成を分離。口パクは WAV RMS＋**0.1s** 遅れ（0.2s は誤り）。字幕は全行3パス必須。登場／退場は AviUtl「弾む」速さ≈6.7・高さ8。ClearType フリンジ → Pillow 直描き推奨。
- 2026/08/01 20:39: 字幕は `narration` 原文。TTS カナ非表示。退場は Y 回転→弾む歩きアウト＋フェード。出典図は親 skill。プロファイル既定: teacher=ひまり／左、listener=つむぎ／右（明示上書きまで）。
- 2026/08/01 20:39 (Sol): `第3章` の数字縮小は誤分類＋フォント実インク。半角＋光学 boost。規約は `subtitle-typography.md`。
- 2026/08/01 20:39 (PR#41): description トリガから固有話者名を外し、役割ベースに。temp/ 試作パスは配布 SoT にしない。
- 2026/08/02 07:53 (Sol xhigh + 実測): 本編15／モーション30。OpenCV dilate＋NumPy ROI blend。NVENC は実 probe＋fallback。納品は CFR30（VFR は作業用のみ）。Ch3 s01–s08+outro: 映像≈235s／合成壁≈97s（RT≈2.4x）。ボトルネックは outro 毎フレーム合成。

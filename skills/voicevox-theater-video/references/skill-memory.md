# skill-memory — voicevox-theater-video

- 2026/08/01 20:39: 親 `slide-narration-video` から劇場合成を分離。口パクは WAV RMS＋**0.1s** 遅れ（0.2s は誤り）。字幕は全行3パス必須。登場／退場は AviUtl「弾む」速さ≈6.7・高さ8。劇場 fps 30。ClearType フリンジ → Pillow 直描き推奨。
- 2026/08/01 20:39: 字幕は `narration` 原文。TTS カナ非表示。退場は Y 回転→弾む歩きアウト＋フェード。出典図は親 skill。プロファイル既定: teacher=ひまり／左、listener=つむぎ／右（明示上書きまで）。
- 2026/08/01 20:39 (Sol): `第3章` の数字縮小は誤分類＋フォント実インク。半角＋光学 boost。規約は `subtitle-typography.md`。
- 2026/08/01 20:39 (PR#41): description トリガから固有話者名を外し、役割ベースに。temp/ 試作パスは配布 SoT にしない。
- 2026/08/02 08:50: 速度既定は全面 30fps CFR + Pillow `alpha_composite` + libx264 + concat copy。字幕マスクのみ任意 OpenCV `MORPH_ELLIPSE`（無ければ Pillow perimeter dilate）。測定ログ（Sakurai Ch3 intro+s01–s08+outro ≈235s）3回中央値85.6s vs legacy99.2s。body15 / NumPy ROI / 短尺NVENC / VFR→CFR 再エンコードは速度既定から除外。規約本文のターゲット表記は案件名を避け抽象化する（PR#42 review）。
- 2026/08/05 00:36 (Issue #44/#45): 経験的に収束した値をプロファイル既定化（ひまり left+face_flip、つむぎ right、FACE_GAP 42%、口 0.1s、同位相バウンス、呼称）。provenance: Sakurai Ch3 制作。`theater-presets.md` / `dialogue-density.md` 追加。メタ指示の本文混入禁止、密度 medium 既定・high で理解確認、前提語の先出しを明文化。
- 2026/08/05 00:55: 口調・一人称・呼称の SoT はボイボ寮（https://voicevox.hiroshiba.jp/dormitory/）。ひまり＋つむぎ既定は寮と一致済みのため再照会不要、と明記。
- 2026/08/05 10:32 (PR#46 review): 規約本文から案件名を外しプロファイル既定として抽象化。前提説明はテーマ理解用の汎用文に縮約。`high` は理解確認必須・再解説は必要時。とらっかぁ系はひまり＋つむぎ private use の既定候補として維持。親 `dialogue-writing.md` は口調 SoT、子 `dialogue-density.md` は密度・前提・メタ分離 SoT と境界を一文固定。
- 2026/08/05 10:36 (Sol): とらっかぁ系を「ひまり＋つむぎ private use 向け既定。公開配布・別キャラの前提にしない」と規約本文へ明記。
- 2026/08/10 08:38: とらっかぁ素材の取得元を `tachie-sources.md` に固定。teacher は冥鳴ひまり download/16、listener は春日部つむぎ「さっぱり」download/9 を優先。ZIP は非同梱、PSD 正本、SHA-256 と取得ページを案件側で記録。

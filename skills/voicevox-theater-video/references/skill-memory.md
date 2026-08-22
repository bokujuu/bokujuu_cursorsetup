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
- 2026/08/11 10:09 (Solレビュー反映): 字幕の固定 `0.72` 倍 shrink と span ごとの別 font size は、`SU(2)` 等を小さく・別フォント風に見せる。1080p基準48pxの単一解決フォントを共有し、必要時だけ同一 font の mask を補正する。0.90〜1.10倍は補正後の実インク高比であり scale 上限ではない。`baseline_offset` を保持して共通 baseline に置き、raw TeX 分類前の補正は禁止、MATH_MASK 化後の正規化は必須。縁取り前 alpha（閾値16）と `第`/`章`/`あ` の中央値を測定基準にし、mathtext の暗黙 fallback を検出・記録する。Matplotlib 既定 math font の tight-bbox 生出力は混在させない。
- 2026/08/11 10:49 (試作動画で再検証): 同一 GenShinGothic P Heavy 48px の supersample mask と共通 baseline を実装。`第3章`、`3.1`、`図28`、`SU(2)`、`v1.2`、`J`、`x×p`、`API`、`Wigner–Eckart` は測定上の補正後インク高比 1.00（CJK基準47px）まで揃った。分数・根号は式の意味上の分子／分母縮小を残しつつ、MATH_MASK 全体の高さ・baseline・縁取りを通常文字と同じ経路へ通す。実動画では字幕ボックスがスライドのフッタと重なり得るため、画面レビュー時に下端余白と立ち絵との干渉も同時確認する。
- 2026/08/11 10:56 (Sol/Luna動画レビュー反映): raw TeXを通常文字経路で測る検査は無効。必ず `$...$` 付きの実入力を MATH_MASK へ通し、最終 fill alpha・通過経路・`baseline_delta_px`・解決 font/fallback をログ化する。`SU(2)` 単体の bbox 高だけで baseline 合格を出さず、実合成行の共通 baseline で確認する。劇場字幕は立ち絵の背面を許容するが、顔・口・重要な手元・スライドフッタとの干渉を安全帯 QA で確認し、最終動画は ffprobe で明示 CFR30 と音声略語のスポット試聴まで行う。
- 2026/08/11 15:15 (Mendel/Darwin/Newton/Lorentz再レビュー反映): 同一TTFでもCJKのem高、Latin cap/x-height、数字、括弧の自然な字形高は一致しない。識別子全体のbboxをCJK高へ合わせる光学補正は `SU(2)`／`v1.2`／`J` に別倍率を掛け、基本ゴシックの見た目を壊すため既定から外す。通常Latinは基準48pxのnative metrics／共通baselineを使う。`\\frac{J_1}{\\hbar}` のような短い分数は `J1/ℏ` の安全なslash flattenを優先し、flatten不能なMATH_MASKだけをascent/depth由来baseline＋分子／分母／stem／分数線の回帰へ送る。family解決だけでは個別glyph fallback不在を証明できず、`fallback_status=unverified`を合格扱いにしない。混在行は同じ縁取り幅、最終outline基準の行間、実測baselineを使う。
- 2026/08/11 16:04 (最終QA反映): 視覚QAが合格でも、PLAIN_MASKの `font_file`／`font_size_px` とMATH_MASKの `verification_basis` が欠けていれば検証証跡として不十分。要求TTFへの解決、semantic glyph coverage、custom mathtext slot一致を記録できる場合だけ `fallback_status=verified` とし、未検証を合格扱いにしない。
- 2026/08/22 14:02: つむぎの「あーし」は一人称であり相槌ではない。文頭の「あーし、」＋相手の行為は呼び掛け／フィラーに聞こえる。`call_names` 一致のために毎発話へ挿入しない。呼び掛けは `ひまっち`／`つむぎ先輩`。原稿規範は親 `dialogue-writing.md`、例は `theater-presets.md`。
- 2026/08/22 14:02: 和文48pxは PR#50 以降の SoT どおり。Latin／数字の相対縮小（`font_size * 0.72`）も同 PR で禁止済み。案件 `render-theater.py` を旧試作からコピーすると shrink/boost が残るため、skill より画面が古くなる。コピー後に `0.72` を照合する。


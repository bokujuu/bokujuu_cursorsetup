# 劇場レンダ規約

Updated: 2026/08/22 14:02

## パイプライン

```text
立ち絵 PSD → 固定キャンバス PNG（表情×口）
スライド PNG
発話 WAV（VOICEVOX）
        ↓
合成（Pillow alpha_composite + 字幕マスクは OpenCV 楕円 dilate 推奨）
        ↓
ffmpeg rawvideo pipe → libx264 + AAC → 明示 CFR30 delivery
        ↓
concat -c copy（ネイティブ CFR 30）
```

フレーム PNG をディスクに残して結合する方式は重いので避ける（pipe または一時ディレクトリ即削除）。

## fps

劇場プロファイルの既定は **全面 30fps（CFR）**。

intro／outro／本編を分けて 15fps にする案は、同一ターゲット実測で納品総時間を改善しなかった（VFR→CFR 再エンコードが短縮を食う）。

## エンコーダ

既定は `libx264 -preset medium -crf 23`。

短尺クリップを多数 NVENC する方式は起動オーバーヘッドで不利になり得る（実測で採用見送り）。

## 合成の高速化（採用済み）

- **採用**: 字幕マスク膨張を OpenCV `MORPH_ELLIPSE` dilate に置換（Pillow 周回スタンプより速い）
- **`cv2` は任意**: 利用可能な場合のみ `MORPH_ELLIPSE`。未導入・import 失敗時は既存の Pillow perimeter dilate。速度目的で依存追加しない
- **不採用（速度目的）**: NumPy ROI blend（intro が遅くなった）、本編15fps＋CFR正規化、短尺NVENC混在

同一ターゲット（映像≈235s、intro+本編+outro）:

- legacy（Pillow perimeter dilate）≈99.2s
- legacy + OpenCV dilate 中央値≈85.6s（3回: 85.6 / 87.3 / 84.5）

他環境での同等短縮は保証しない。速度改善を主張する変更は、同一ターゲットで legacy 経路との実測処理時間を比較してから採用する。案件名付きの測定ログは `skill-memory.md` または案件 repo 側に置く。

## 口パク

1. WAV の RMS で発話区間を検出（短いギャップは結合）
2. 区間開始 + **100ms** から開閉交互（既定 150ms）
3. 無音・区間外は閉じ
4. fps 既定は **30**。遅れ SoT は **0.1s**

## 字幕縁取り（D 系統）

- 幅: 楕円 dilate（参考 outer≈10 / inner≈3.5 @ 最終 px 相当）。`cv2` 可なら `MORPH_ELLIPSE`、無ければ Pillow perimeter dilate
- 正方形 MaxFilter 単体は使わない（余白 `outer_w+8` 付きの円形／楕円）
- Blur: 弱め（広いガウシアンハローは避ける）
- 合成順（**全行まとめて**）:
  1. キャラ色縁
  2. 黒縁
  3. 白文字（Blur ほぼ無し）
- スーパーサンプル後、マスクを BOX 縮小してから着色するとフリンジが減る

## 字幕テキスト（表示 ≠ TTS）

詳細: [subtitle-typography.md](subtitle-typography.md)

- 画面字幕は `utterances[].narration`（人間可読 SoT）。`tts_text`／発音辞書のカナは**出さない**
- **表示区間**: 当該発話 cue の実測開始〜終了のみ。`pause_between_turns_ms` は字幕尺に含めない（次ターンへ食い込ませない）
- 節番号はアラビア数字（`3.1`）。人名・群名はラテン（`SU(2)`、`Wigner–Eckart`）
- **和文数値**は半角のまま、同じ字幕フォントの基準サイズで描画する。単語全体の bbox をCJK高へ合わせる補正はせず、明示した単一 glyph だけ必要時に同じ font mask を測定補正する。全角化は高さ合わせに使わない
- latin 識別子（`SU(2)`、`v1.2`）を固定倍率で縮小・拡大しない。内部数字を別補正せず、一塊として基本ゴシックの native size で表示する
- 数式は `$...$`。単純式は半角 unicode flatten＋同一フォントの mask。短い分数は `J1/ℏ` のような安全な slash 表記へ flatten し、複雑式は字幕フォントの custom mathtext、または MATH_MASK を component／実インク高・baseline・縁取りまで正規化する
- Matplotlib 高 dpi の tight-bbox 生出力、既定 DejaVu／Computer Modern の無調整混在を禁止する
- MATH_MASK の目標高は `font_size * 0.92` の固定値ではなく、同じ字幕フォントで測った基準グリフと数式componentの実インク高から決める。alpha bbox を crop しても `baseline_offset` を捨てず、mathtext の ascent/depth 等から実測した共通 baseline（通常±1px、MATH_MASK±2px）へ合わせてから縁取りへ渡す。raw TeX 分類前の補正は禁止、MATH_MASK 化後の component／baseline 正規化は必須
- インク高の測定は縁取り前・最終解像度の fill alpha（`alpha >= 16`）で行い、基準は `第`・`章`・`あ` の中央値。MATH_MASK は全体 bbox だけでなく分子／分母・stem・分数線を測る。custom mathtext の未収録 glyph は暗黙 fallback を検出・記録し、`fallback_status=unverified` も未確認として扱う。`verified` は要求TTF、semantic glyph coverage、custom mathtext slotの一致と `verification_basis` が揃った場合だけ許可し、別 font のまま最終画面へ出さない
- 1080p の和文基準サイズは **48px**（[subtitle-typography.md](subtitle-typography.md)）。和文が立ち絵に対して小さく見えることと、Latin／数字だけが相対縮小されることは別問題。後者は `font_size * 0.72` の span 別ロードと識別子 bbox の CJK 合わせが原因で、現行 SoT では禁止（GitHub PR #50）
- 案件側 `render-theater.py` を旧試作からコピーすると、skill が直っても画面は旧挙動のまま。コピー後に `0.72` shrink／span 別 `font_size` が残っていないか照合する

## 字幕安全帯

- 最終 outline bbox の下端から画面下端まで **56px以上**を確保する。1行・2行とも、fill bboxではなく縁取りを含む最終 bbox で測る
- スライドの静的フッタ・出典行は字幕帯へ置かない。必要なら字幕帯より上へ移すか、劇場版では非表示にする
- 立ち絵を字幕の背面に置くレイアウトは許容するが、顔・口・重要な手元・表情差分の視認を字幕で隠さない。最終合成フレームで alpha bbox の重なりを確認する

## 最終出力 QA

- `ffprobe` で 1920×1080、`yuv420p`、映像 `r_frame_rate=30/1`・`avg_frame_rate=30/1` を確認する
- 映像パケットの継続時間が原則 `1/30` 秒で、concat の時間ベース由来の `60/1` などの誤メタデータを残さない。必要なら concat copy ではなく `fps=30` の明示再エンコードを行う
- 音声は実聴せずに合格扱いにせず、`LaTeX`、`raw TeX`、`MATH_MASK`、`baseline_offset` 等の発音辞書語をスポット試聴する

## スライド文字

- Chromium/Marp の ClearType 色フリンジが出やすい → Pillow＋源真ゴシック直描きを優先
- 過度な 2×LANCZOS はハローの原因。ネイティブ描画か、縮小するなら BOX＋α注意
- 出典図・先頭出典行は親 skill の figures-and-math / slide-design に従う

## 負荷メモ

- 発話クリップは口開閉の **2 枚**だけ合成し、時間方向は pipe で切替
- 導入・退場だけは毎フレーム姿勢が変わるためコスト高。尺は各 2〜3 秒程度に抑える
- `$...$` が多い発話は字幕合成が重い。必要最小の数式島に留める
- outro／intro の毎フレーム合成は依然として主因。追加の速度施策は ROI 再利用など別課題

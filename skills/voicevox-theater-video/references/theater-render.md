# 劇場レンダ規約

Updated: 2026/08/02 08:43

## パイプライン

```text
立ち絵 PSD → 固定キャンバス PNG（表情×口）
スライド PNG
発話 WAV（VOICEVOX）
        ↓
合成（Pillow alpha_composite + 字幕マスクは OpenCV 楕円 dilate 推奨）
        ↓
ffmpeg rawvideo pipe → libx264 + AAC
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

他環境での同等短縮は保証しない。速度改善を主張する変更は、同一ターゲットで legacy 比の壁時計を測ってから採用する。案件名付きの測定ログは `skill-memory.md` または案件 repo 側に置く。

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
- **和文数値**は半角のまま、実測インク高さで光学拡大（基準=`第`/`章`）。全角化は高さ合わせに使わない
- **0.72 倍**は latin 識別子一塊だけ（`SU(2)`）。内部数字を再拡大しない
- 数式は `$...$`。単純式は半角 unicode flatten＋変数 boost。複雑式のみ MATH_MASK＋余白付き円形縁取り
- matplotlib 高 dpi 生出力をそのまま並べない

## スライド文字

- Chromium/Marp の ClearType 色フリンジが出やすい → Pillow＋源真ゴシック直描きを優先
- 過度な 2×LANCZOS はハローの原因。ネイティブ描画か、縮小するなら BOX＋α注意
- 出典図・先頭出典行は親 skill の figures-and-math / slide-design に従う

## 負荷メモ

- 発話クリップは口開閉の **2 枚**だけ合成し、時間方向は pipe で切替
- 導入・退場だけは毎フレーム姿勢が変わるためコスト高。尺は各 2〜3 秒程度に抑える
- `$...$` が多い発話は字幕合成が重い。必要最小の数式島に留める
- outro／intro の毎フレーム合成は依然として主因。追加の速度施策は ROI 再利用など別課題

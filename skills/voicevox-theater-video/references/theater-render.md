# 劇場レンダ規約

Updated: 2026/08/02 08:20

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

フレーム PNG をディスクに残して結合する方式は重いので避ける。

## fps

劇場プロファイルの既定は **全面 30fps（CFR）**。  
intro／outro／本編を分けて 15fps にする案は、同一ターゲット実測で納品総時間を改善しなかった（VFR→CFR 再エンコードが短縮を食う）。

## エンコーダ

既定は `libx264 -preset medium -crf 23`。  
短尺クリップを多数 NVENC する方式は起動オーバーヘッドで不利になり得る（実測で採用見送り）。

## 合成の高速化（採用済み）

- **採用**: 字幕マスク膨張を OpenCV `MORPH_ELLIPSE` dilate に置換（Pillow 周回スタンプより速い）
- **不採用（速度目的）**: NumPy ROI blend（intro が遅くなった）、本編15fps＋CFR正規化、短尺NVENC混在

同一ターゲット（Ch3 intro+s01–s08+outro, 映像≈235s）:
- legacy（Pillow dilate）≈99.2s
- legacy + OpenCV dilate 中央値≈85.6s（3回: 85.6 / 87.3 / 84.5）→ **約14s短縮**

OpenCV が無い環境は Pillow dilate にフォールバックしてよい。

## 口パク

1. WAV の RMS で発話区間を検出
2. 区間開始 + **100ms** から開閉交互（既定 150ms）
3. 無音・区間外は閉じ
4. fps 既定 **30**。遅れ SoT は **0.1s**

## 字幕縁取り

- 楕円 dilate（OpenCV 推奨）。正方形 MaxFilter 単体は使わない
- 合成順（全行まとめて）: 色縁 → 黒縁 → 白文字

## 字幕テキスト（表示 ≠ TTS）

詳細: [subtitle-typography.md](subtitle-typography.md)

## 負荷メモ

- outro／intro の毎フレーム合成は依然として主因。追加の速度施策は ROI 再利用など別課題
- 速度改善を主張する変更は、同一ターゲットで legacy 比の壁時計を測ってから採用する

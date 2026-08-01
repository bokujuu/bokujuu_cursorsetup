# 劇場レンダ規約

Updated: 2026/08/02 07:53

## パイプライン

```text
立ち絵 PSD → 固定キャンバス PNG（表情×口）
スライド PNG
発話 WAV（VOICEVOX）
        ↓
合成（Pillow + 推奨: NumPy ROI blend / OpenCV dilate）
        ↓
ffmpeg rawvideo pipe → H.264（NVENC 可なら）+ AAC
        ↓
concat（中間は VFR 可）→ **納品は CFR 30 に正規化**
```

フレーム PNG をディスクに残して結合する方式は重いので避ける（pipe または一時ディレクトリ即削除）。

## fps（用途別）

| 区間 | 既定 fps | 理由 |
|------|----------|------|
| intro / outro（弾む・Y回転） | **30** | モーションの見え方 |
| 本編発話・ターン pause | **15** | 口パク程度の低運動。合成フレーム数を半減 |
| **納品ファイル** | **CFR 30** | 15fps 区間はフレーム複製。VFR のまま納品しない |

中間セグメントの VFR concat（`-c copy`）は作業用。最終だけ `fps=30` で正規化する。

## エンコーダ

1. 起動時に **微小クリップで NVENC 実エンコード probe**（一覧に名前があるだけでは不十分）
2. 成功 → `h264_nvenc`（例: `-preset p4 -rc vbr -cq 23 -b:v 0`）
3. 失敗 → `libx264 -preset medium -crf 23`
4. 使用した encoder をログ／ベンチに残す

## 合成の高速化（推奨）

- 字幕マスク膨張: OpenCV `MORPH_ELLIPSE` dilate
- 立ち絵 overlay: NumPy による ROI だけの Porter-Duff over
- 発話クリップは口開閉2枚を先に焼き、pipe で差し替え
- intro/outro は毎フレーム合成のため高コスト。静的レイヤ再利用が次の最適化候補

## 口パク

1. WAV の RMS で発話区間を検出（短いギャップは結合）
2. 区間開始 + **100ms** から開閉交互（既定 150ms）
3. 無音・区間外は閉じ
4. 本編 fps は上記表（15）。遅れ SoT は **0.1s**

## 字幕縁取り（D 系統）

- 幅: 円形／楕円 dilate（参考 outer≈7–10 / inner≈2.5–3.5）
- Blur: 弱め
- 合成順（**全行まとめて**）: 色縁 → 黒縁 → 白文字
- スーパーサンプル後、マスクを BOX 縮小してから着色

## 字幕テキスト（表示 ≠ TTS）

詳細: [subtitle-typography.md](subtitle-typography.md)

- 画面字幕は `utterances[].narration`。TTS カナは出さない
- 表示区間は発話 cue の実測区間のみ（`pause_between_turns_ms` を含めない）
- 光学サイズ規約は subtitle-typography に従う

## 負荷メモ

- intro/outro は毎フレーム RGBA 合成のため壁時計の主因になりやすい（実測で outro が全体の約 20% 超もあり得る）
- 工程別 wall（intro / utterance / outro / encode / CFR 正規化）をベンチに残す
- **同一ターゲット実測（Ch3 s01–s08+outro, 映像≈235s）**: legacy（全面30・Pillow・libx264）≈99s に対し、新手法の合成＋セグメントencodeのみ≈95s（約4%短縮）。納品用 CFR30 正規化を含めると ≈110s で **総時間は遅くなり得る**。短い pause を NVENC で多数回すと起動オーバーヘッドも効く。速度目的なら CFR を任意化し、intro/outro の再合成削減を先に検討する

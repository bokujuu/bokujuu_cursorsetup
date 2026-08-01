---
name: voicevox-theater-video
description: >-
  VOICEVOX 劇場レイアウトの全画面スライド対話動画。立ち絵バストアップ、ワイプ字幕、
  口パク（実音波形同期）、登場／退場（弾む歩き＋Y回転）、表情切替を Pillow＋ffmpeg で合成する。
  slide-narration-video の dialogue 拡張。Use when VOICEVOX劇場、立ち絵つき解説対話、
  ひまり／つむぎ劇場、theater profile、弾む登場・退場演出のとき。単純な Marp＋TTS のみ、
  Remotion 主軸、モノローグ専用は slide-narration-video に委譲。
---

# VOICEVOX 劇場動画（slide-narration 拡張）

Updated: 2026/08/01 19:03

`slide-narration-video` の **dialogue 劇場プロファイル**を、立ち絵・字幕・口パク・登場／退場演出まで含めて設計・実装する拡張 skill。
原稿・SoT・語り口は親 skill に従い、本 skill は **画面合成とレンダ規約**を担う。

## 親 skill（必須）

着手前に読む:

1. [`../slide-narration-video/SKILL.md`](../slide-narration-video/SKILL.md) — 制作フロー・`narration_mode`・キュー SoT・**出典図の転載**
2. [`../slide-narration-video/references/dialogue-writing.md`](../slide-narration-video/references/dialogue-writing.md) — 対話原稿
3. [`../slide-narration-video/references/tts-pronunciation.md`](../slide-narration-video/references/tts-pronunciation.md) — 字幕＝`narration`、読み＝辞書→`tts_text`
4. [`../japanese-technical-writing/SKILL.md`](../japanese-technical-writing/SKILL.md) — スライドの論理
5. （monologue 接続のみ）[`../cognitive-rhythm-writing/SKILL.md`](../cognitive-rhythm-writing/SKILL.md)

本 skill を選ぶ条件: **立ち絵劇場レイアウト**が成果物の一部である。スライド＋音声だけの案件は親 skill のみでよい。

## 適用範囲

使う:

- 解説役（左）＋聞き手（右）の立ち絵 overlay
- 枠なしワイプ字幕（話者テーマ色縁取り）。字幕は **原文表記**（数字・ラテン・`$...$` 数式）
- VOICEVOX 発話 WAV に同期した口パク
- 動画先頭の無音登場（弾む歩きスライドイン＋フェード）
- 動画末尾の無音退場（Y 軸回転で外側向き → 弾む歩きスライドアウト＋フェード）
- 表情タグ（default / question / think / understand / surprise）

使わない:

- Remotion／Motion Canvas が主タイムラインの案件（親 skill）
- 立ち絵なしの ffmpeg 静止画結合のみ
- 会話劇そのものが目的で解説・理解確認がないコンテンツ

## 既定スタック（劇場）

| 層 | 既定 | 備考 |
|----|------|------|
| スライド | 白テーマ PNG（Marp または Pillow 直描き） | ClearType フリンジ回避のため Pillow＋源真ゴシックを推奨。出典図は親 skill に従い抽出配置 |
| 立ち絵 | とらっかぁ系 PSD → 全身スプライト（胴体クロップしない） | 画面下へはみ出させて連続感を出す |
| 合成 | Pillow（RGBA）→ ffmpeg rawvideo pipe | フレーム PNG を残さない |
| TTS | VOICEVOX（役割は `meta.speakers`） | 発話ごと WAV。読みは辞書、字幕は `narration` |
| 字幕数式 | `$...$` を mathtext 等でビットマップ挿入 | カタカナ読みを字幕に出さない |
| fps | 30 | 登場／退場の見え方用 |
| フォント（字幕） | 源真ゴシック P Heavy | 失敗時: MS UI Gothic → メイリオ → default |
| フォント（スライド） | 源真ゴシック P Medium/Bold | 同上 |

詳細: [references/theater-layout.md](references/theater-layout.md) / [references/theater-render.md](references/theater-render.md) / [references/subtitle-typography.md](references/subtitle-typography.md) / [references/intro-entrance.md](references/intro-entrance.md) / [references/outro-exit.md](references/outro-exit.md)

## 制作フロー（劇場追加分）

親 skill の Task Progress に、劇場案件では次を足す。

```text
Theater extras:
- [ ] T0. profile: voicevox-theater（layout / speakers / theme_rgb）
- [ ] T1. 立ち絵エクスポート（固定キャンバス・表情・口開閉）
- [ ] T2. スライド書き出し（フリンジ対策・出典図・先頭出典行）
- [ ] T3. 導入: 無音弾む歩きスライドイン
- [ ] T4. 本編: 発話クリップ（口パク＝実音区間＋0.1s 遅れ）
- [ ] T5. 字幕: narration 原文＋$LaTeX$／全行 色縁→黒縁→白文字
- [ ] T6. 退場: Y回転→弾む歩きアウト＋フェード（導入と同パラメータ）
- [ ] T7. concat → mp4 検証（導入／退場無音・口閉じ・縁・字幕記号）
```

## 不変条件（短縮）

1. **対面**: 左=解説役（中央向き）、右=聞き手（中央向き）。全身反転レイヤが無ければ画像反転可
2. **口パク**: 無音では閉じる。実音開始から **0.1s 後**に開き始め（音声が先）
3. **字幕レイヤ**: `narration`（SoT）を描画。TTS 用カナは出さない。和文数値はフルサイズ。`$...$` は数式。latin 識別子のみ任意縮小。全行まとめて ①キャラ色縁 ②黒縁 ③白文字（[subtitle-typography.md](references/subtitle-typography.md)）
4. **立ち絵**: 胴体を切り捨てない。入らない部分は画面外へ
5. **一時ファイル**: フレーム PNG を成果物として残さない
6. **導入**: 音なしで登場完了してから最初の発話
7. **退場**: 本編後に音なしで外側向き回転→歩き去り→フェード

## 参照プロトタイプ

実装の参照実装（ローカル試作）:

`temp/sakurai-ch3-theater/scripts/render-theater.py`  
（字幕 LaTeX・outro 込み。global skill は規約の SoT、コードは案件へコピーしてよい）

## 検証

- 導入クリップが無音で、両キャラが外側から弾みながら定位置へ入る
- 退場クリップが無音で、Y 回転のあと外側へ歩きフェードする
- 最初の発話前に口が無音で動いていない
- 字幕に「三点二」「エイチバー」など TTS 用表記が出ておらず、`3.2` / `$\\hbar$` 等が原文どおり
- 2行字幕で下行縁が上行の白字に乗らない
- `python -m py_compile` 対象スクリプト / `ffmpeg` で最終 mp4 再生可能

## メモ

運用知見は [references/skill-memory.md](references/skill-memory.md) へ追記する。

# 例: 短いキューシート

Updated: 2026/08/01 20:40

## monologue（既定互換）

2 枚だけの最小例。本番では `aligns_with` と実測 `at_ms` を埋める。

```yaml
meta:
  fps: 30
  narration_mode: monologue
  voice:
    engine: voicevox
    speaker: 冥鳴ひまり
  default_pause_after_ms: 500

slides:
  - id: s01
    image: slides/01.png
    narration: |
      まず境界を確認します。
      ここで扱うパイプラインは、原稿から音声と画面を同じ時刻表で結ぶ仕組みであって、
      編集ソフト上で手作業で尺を合わせる作業そのものではありません。
    pause_after_ms: 500
    cues:
      - id: s01-boundary
        at_ms: 600
        duration_ms: 2800
        type: highlight
        target: { x: 0.10, y: 0.30, w: 0.55, h: 0.25 }
        aligns_with: "ここで扱うパイプラインは"

  - id: s02
    image: slides/02.png
    narration: |
      次に部品です。
      Remotion が時刻表と書き出しを持ち、Motion Canvas は必要なときだけ注釈の動きを受け持ちます。
      声は VOICEVOX の冥鳴ひまりを既定とします。
    pause_after_ms: 500
    cues:
      - id: s02-remotion
        at_ms: 900
        duration_ms: 2000
        type: arrow
        target: { x: 0.28, y: 0.45 }
        aligns_with: "Remotion が時刻表"
      - id: s02-motion
        at_ms: 3200
        duration_ms: 2000
        type: arrow
        target: { x: 0.62, y: 0.45 }
        aligns_with: "Motion Canvas は"
```

## 原稿側で意識する接続

s01 末尾は「何ではないか」で境界を閉じ、s02 冒頭は「次に部品です」で構成要素へ進む。
japanese-technical-writing の提示順（境界→構成要素）に沿っている。

文の拍は cognitive-rhythm-writing に任せる。上の例は短さ優先の見本であり、本番原稿は同 skill の点検を通す。

## dialogue（会話劇寄り）

聞き手はメタ宣言せず、具体的な噛みつきで返す。字幕は現在台詞のみ。

```yaml
meta:
  fps: 15
  narration_mode: dialogue
  speakers:
    teacher:
      engine: voicevox
      speaker: 冥鳴ひまり
    listener:
      engine: voicevox
      speaker: 春日部つむぎ
  default_pause_between_turns_ms: 220
  default_pause_after_ms: 600

slides:
  - id: s01
    image: slides/01.png
    utterances:
      - id: s01-u01
        speaker: teacher
        narration: |
          講義だけだと、どこかで置いてかれた瞬間に、その先が全部こぼれ落ちる。
      - id: s01-u02
        speaker: listener
        narration: |
          え、情報が多いから？
      - id: s01-u03
        speaker: teacher
        narration: |
          量より、拾う役が画面にいないこと。
    pause_between_turns_ms: 220
    pause_after_ms: 700
```

劇場レイアウト（任意）では解説役を左下・聞き手を右下、字幕は中央下の現在台詞のみ。詳細: [dialogue-writing.md](dialogue-writing.md)

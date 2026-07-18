# 例: 短いキューシート

2 枚だけの最小例。本番では `aligns_with` と実測 `at_ms` を埋める。

```yaml
meta:
  fps: 30
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

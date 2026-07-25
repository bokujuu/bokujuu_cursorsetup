# タイムラインと発話同期

## 問題の本質

解説動画で視聴者が置いていかれる典型は、情報量ではなく次の二つである。

1. **遷移が認知より速い** — 前枚の主張が頭に残る前に次枚が来る
2. **指差と発話がずれる** — 「ここ」と言っているのに画面の別の場所が動いている

キューシートは、この二つを防ぐための単一の真実源（SoT）である。

## スライド間の「間」

- 既定: 各スライドのナレーション終了後、次スライド表示の前後に **`pause_after_ms: 500`**
- 目的: 人が一呼吸置ける長さ。演出のための長尺サイレンスではない
- 調整: 概念の切れ目が深いときは 700〜1000 ms まで延ばしてよい。連続する短い確認枚では 300 ms まで短縮してよいが、**0 にはしない**
- 実装: Remotion では前クリップ末尾または次クリップ先頭に静止＋無音フレームを入れる。音声ファイル末尾に無音を足す方法でもよいが、キューシート上で明示する

「間」は原稿の接続文の代わりにならない。接続が弱いときは原稿を直す。

## 同期モデル

時間の原点は **当該スライドのナレーション音声の開始（t = 0）** とする。
動画全体の絶対時刻は Remotion が累積する。エージェントはキューでは相対時刻だけを扱う。

```
[slide N 表示]
  →（任意の入フェード）
  → narration audio 開始 = t=0
  → cues が at_ms で発火
  → narration 終了
  → pause_after_ms
[slide N+1]
```

### cue の種類

| type | 用途 | 実装の置き場 |
|------|------|----------------|
| `highlight` | 矩形・下線で領域を示す | Remotion で十分なことが多い |
| `arrow` | 注目点への矢印 | 単純なら Remotion、軌道が複雑なら Motion Canvas |
| `zoom` | 一時的な拡大 | Remotion |
| `motion` | Motion Canvas クリップ再生 | `clip` パスを指定 |
| `dim` | 注目以外を暗くする | Remotion |

同時に出せる cue は、原則 **視線を奪い合わない数（目安 1、多くて 2）**。

### 発話との対応づけ

各 cue は、原稿上のフレーズに紐づける。

- 良い: 「この矢印が示すのが入力側です」の「この矢印」に合わせて `arrow` を出す
- 悪い: 文の途中と無関係に装飾だけ先に動かす

`at_ms` の初期値は、TTS 後の実測 WAV 長から割り当てる。原稿だけの推定で最終書き出ししない。
VOICEVOX は文ごとに WAV を分けておくと、cue の再計測が容易になる。

## スキーマ（YAML）

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
      まず境界を確認します。ここで扱うのは A であって、B ではありません。
    pause_after_ms: 500
    cues:
      - id: c01
        at_ms: 800
        duration_ms: 2400
        type: highlight
        target:
          # スライド画像上の正規化座標 (0–1) またはピクセル。プロジェクトで一方に統一する
          x: 0.12
          y: 0.35
          w: 0.40
          h: 0.22
        aligns_with: "ここで扱うのは A"
```

必須: `id`, `image`, `narration`, `pause_after_ms`  
cue 使用時の必須: `at_ms`, `type`, `duration_ms`  
`aligns_with` は検証用。書き出しには使わなくてよいが、ずれ調査で残す。

読み辞書はキューと別に置いてよい（推奨: `script/pronunciation.yml`）。  
`meta.pronunciation` や `slides[].pronunciation_overrides` を足してもよいが、変換後文字列を SoT 必須フィールドにしない。TTS 入力は派生物（[tts-pronunciation.md](tts-pronunciation.md)）。

## Remotion / Motion Canvas への落とし方

1. キューシートを読み、スライド順に Sequence を積む
2. 各 Sequence の尺 = `audio_duration_ms + pause_after_ms`（＋入出フェード）
3. `cues` を `at_ms` で AbsoluteFill オーバーレイ、または Motion Canvas 書き出しクリップの開始にマップする
4. Motion Canvas 側の尺が `duration_ms` と一致しない場合は、クリップを直す（Remotion 側で引き伸ばして誤魔化したままにしない）

## 検証手順

1. キューシートだけで通読し、接続文と `pause_after_ms` の有無を確認する
2. TTS 後、各スライドの WAV 長を計測し、`at_ms + duration_ms ≤ audio_duration_ms` を満たすか確認する
3. プレビューで「指差と発話」を 1 本ずつ目視する
4. 遷移直後に早送り感があれば、間を足すより先に原稿の橋を疑う

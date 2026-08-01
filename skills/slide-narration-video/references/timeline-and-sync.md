# タイムラインと発話同期

Updated: 2026/08/01 01:27

## 問題の本質

解説動画で視聴者が置いていかれる典型は、情報量ではなく次である。

1. **遷移が認知より速い** — 前枚の主張が頭に残る前に次枚が来る
2. **指差と発話がずれる** — 「ここ」と言っているのに画面の別の場所が動いている
3. **理解確認がない** — 一方的な講義でつまずきが回収されない（`dialogue` で緩和）

キューシートは、この二つ（および対話時の三つめ）を防ぐための単一の真実源（SoT）である。

## 語り口モード

`meta.narration_mode`:

| 値 | SoT | 備考 |
|----|-----|------|
| `monologue`（未指定時の既定） | `slides[].narration` | 現行互換 |
| `dialogue` | `slides[].utterances[]` | 同一スライドでトップレベル `narration` を併記しない |

二重 SoT を許可しない。表示用に通し文が必要なら、書き出し時に `utterances` から導出する。

## スライド間の「間」

- 既定: 各スライドのナレーション終了後、次スライド開始前に **`pause_after_ms: 500`**
- 目的: 人が一呼吸置ける長さ。演出のための長尺サイレンスではない
- 調整: 概念の切れ目が深いときは 700〜1000 ms まで延ばしてよい。連続する短い確認枚では 300 ms まで短縮してよいが、**0 にはしない**
- 実装: Remotion では Sequence 尺を音声実測合計（＋ターン間 pause）＋`pause_after_ms` とし、ナレーション後に静止＋無音フレームを入れる。音声ファイル末尾に無音を足す方法でもよいが、キューシート上で明示する
- 境界の正: **ナレーション完了後〜次スライド開始前**。「スライド遷移の直後」だけを正としない（実装が遷移の前後どちらに置くかでぶれないようにする）

「間」は原稿の接続文の代わりにならない。接続が弱いときは原稿を直す。

## ターン間の「間」（dialogue）

- 既定候補: **`pause_between_turns_ms: 250`**（`meta.default_pause_between_turns_ms` またはスライド単位）
- 目的: 話者交替の区切りと、視聴者の一拍。ゼロにしない
- 調整: 深い確認の前は 300〜400 ms、短い相づちの後は 150〜200 ms まで短縮してよい

## 同期モデル

時間の原点は **当該スライドの最初の発話音声の開始（t = 0）** とする。
動画全体の絶対時刻は Remotion が累積する。エージェントはキューでは相対時刻だけを扱う。

```
[slide N 表示]
  →（任意の入フェード）
  → first utterance audio 開始 = t=0
  →（dialogue）utterance → pause_between_turns → utterance …
  → cues が at_ms で発火（単一発話区間内）
  → 最終発話終了
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
- dialogue: cue は **単一発話の実測区間内**に収める。ターンをまたがない。任意で `utterance_id` を付与して検証しやすくする

`at_ms` の初期値は、TTS 後の実測 WAV 長から割り当てる。原稿だけの推定で最終書き出ししない。
VOICEVOX は文ごと（dialogue では発話ごと）に WAV を分けておくと、cue の再計測が容易になる。

## スキーマ（YAML）— monologue

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
      まず境界を確認します。ここで扱うのは A であって、B ではありません。
    pause_after_ms: 500
    cues:
      - id: c01
        at_ms: 800
        duration_ms: 2400
        type: highlight
        target:
          x: 0.12
          y: 0.35
          w: 0.40
          h: 0.22
        aligns_with: "ここで扱うのは A"
```

必須: `id`, `image`, `narration`, `pause_after_ms`  
cue 使用時の必須: `at_ms`, `type`, `duration_ms`  
`aligns_with` は検証用。書き出しには使わなくてよいが、ずれ調査で残す。

## スキーマ（YAML）— dialogue

```yaml
meta:
  fps: 30
  narration_mode: dialogue
  speakers:
    teacher:
      engine: voicevox
      speaker: 冥鳴ひまり
    listener:
      engine: voicevox
      speaker: <プロジェクトで選んだ聞き手>
  default_pause_between_turns_ms: 250
  default_pause_after_ms: 500

slides:
  - id: s01
    image: slides/01.png
    utterances:
      - id: s01-u01
        speaker: teacher
        narration: |
          まず、ここでは入力から出力までを一つの時刻表で管理します。
      - id: s01-u02
        speaker: listener
        narration: |
          えっと、音声と画面を別々に作って、あとで合わせるのとは違うんですか。
      - id: s01-u03
        speaker: teacher
        narration: |
          近いですが、後から手で合わせるのではありません。最初から同じキューシートで決めます。
    pause_between_turns_ms: 250
    pause_after_ms: 500
    cues:
      - id: s01-timeline
        at_ms: 900
        duration_ms: 1800
        type: highlight
        target: { x: 0.14, y: 0.38, w: 0.52, h: 0.18 }
        aligns_with: "一つの時刻表で管理します"
        utterance_id: s01-u01
```

必須: `id`, `image`, `utterances`（各要素に `id`, `speaker`, `narration`）, `pause_after_ms`  
`speaker` は役割 ID（`teacher` / `listener` 等）。実話者は `meta.speakers` で解決する。  
原稿規範: [dialogue-writing.md](dialogue-writing.md)

読み辞書はキューと別に置いてよい（推奨: `script/pronunciation.yml`）。  
`meta.pronunciation` や `slides[].pronunciation_overrides` を足してもよいが、変換後文字列を SoT 必須フィールドにしない。TTS 入力は派生物（[tts-pronunciation.md](tts-pronunciation.md)）。

## Remotion / Motion Canvas / ffmpeg への落とし方

1. キューシートを読み、スライド順に Sequence（またはセグメント）を積む
2. 各スライドの尺 = 発話 WAV 実測合計 ＋ ターン間 pause 合計 ＋ `pause_after_ms`（＋入出フェード）
3. dialogue は発話順に音声を繋ぎ、役割ごとに話者を切り替える
4. `cues` を `at_ms` で AbsoluteFill オーバーレイ、または Motion Canvas 書き出しクリップの開始にマップする
5. Motion Canvas 側の尺が `duration_ms` と一致しない場合は、クリップを直す（Remotion 側で引き伸ばして誤魔化したままにしない）

## 検証手順

1. キューシートだけで通読し、接続文と `pause_after_ms`（および dialogue ならターン間 pause・理解確認）の有無を確認する
2. TTS 後、各発話の WAV 長を計測し、累積時刻で `at_ms + duration_ms` が対応発話区間内に収まるか確認する
3. プレビューで「指差と発話」を 1 本ずつ目視する
4. 遷移直後に早送り感があれば、間を足すより先に原稿の橋を疑う
5. dialogue では、優等生聞き手になっていないか原稿点検する（[dialogue-writing.md](dialogue-writing.md)）

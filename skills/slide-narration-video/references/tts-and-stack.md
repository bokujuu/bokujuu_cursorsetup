# TTS と描画スタック

Updated: 2026/08/01 01:27

## 描画スタック（確定方針）

| 採用 | 役割 |
|------|------|
| Remotion | タイムライン、スライド表示、音声、単純オーバーレイ、最終書き出し（モーションあり） |
| Motion Canvas | 発話に同期する複雑な注釈・図解アニメ |
| **ffmpeg 静止画結合** | **動きのない**全画面スライド＋WAV の高速書き出し（優先候補） |

| 不採用（原則） | 理由 |
|----------------|------|
| Adobe Premiere 等 | 所持・自動化前提にしない |
| PixiJS / Three.js | インタラクティブが主目的でない限り不要 |

例外: ユーザーがインタラクティブデモを明示したときだけ Pixi/Three を検討する。解説動画の本線には戻さない。

## Remotion と Motion Canvas の境界

- どちらでも書ける単純なハイライトは Remotion に寄せ、ツール切替コストを下げます
- 経路アニメ、多段の組み立て、図の要素が時間とともに増えるものは Motion Canvas
- Motion Canvas の成果は動画クリップまたは Remotion が埋め込める形式で書き出し、キューの `at_ms` で開始する

同じ注釈を両ツールで二重実装しない。

## 静止スライドショー（動きなし）の高速書き出し

全画面スライドが **静止 PNG** で、注釈アニメが無い／ほぼ無い場合、Remotion の毎フレームキャプチャは過剰になりやすい。次を優先する。

### 推奨: ffmpeg 静止画結合

各スライドについて「PNG を音声尺＋`pause_after_ms` だけ表示」し、WAV を載せてセグメント化し、concat する。

dialogue では、発話 WAV をターン間無音付きで先に1本のスライド音声へ結合してから載せるか、セグメント内で順に mux する。いずれでも **実測長の累積**が SoT になる。

- `-loop 1 -i slide.png` + `-i slide.wav`
- `-c:v libx264`（映像エンコーダを明示）
- `-r <meta.fps>`（キューの `meta.fps`。静止画候補は **15**）
- `-tune stillimage` / `-pix_fmt yuv420p`
- 音声後の間は `-af apad=pad_dur=<pause_sec>` と `-t <audio+pause>` で揃える
- 最後に concat demuxer で結合（`-movflags +faststart`）
- **書き出し後に ffprobe／1 フレーム抽出**で健全性を確認する（`pix_fmt=unknown` や `Invalid NAL unit size` なら破損）

Remotion 未使用なら README / `process-log.md` にその旨を残す。

### fps

静止画中心なら **15 fps** を既定候補とする（30 の半分のフレームで見た目差は小さい）。キューの `meta.fps` と一致させる。注釈アニメや細かいモーションがあるときは 30 のまま Remotion／Motion Canvas 側を使う。

### Remotion を使う場合の注意

- 同時に複数 `remotion render` しない（mux 破損しやすい）
- `--concurrency` はまず `1`。安定を確認してから上げる
- exit 0 でもビットストリームが壊れることがある。再生前に上記の健全性チェックを行う

## TTS 既定: VOICEVOX

- エンジン: VOICEVOX
- monologue 既定話者: **冥鳴ひまり**
- dialogue: `meta.speakers` で役割（`teacher` / `listener` 等）→ 話者を解決する。特定キャラを skill 共通既定に固定しない
- 向き: バッチ生成、安定したキャラ声、CPU 中心で負荷が軽い
- 運用（monologue）: キューシートの `narration` を文またはスライド単位で WAV 化し、実測長を同期に使う
- 運用（dialogue）: **発話ごと**に WAV を生成し、実測長と `pause_between_turns_ms` を累積してタイムラインを確定する。スライド単位の一括 WAV に戻さない
- 推奨パス例: `audio/<slide_id>/<utterance_id>.wav`（または同等の発話単位）
- **読み正規化**: 英字・固有語は TTS 直前にプロジェクト辞書でカタカナ化する。SoT 本文を場当たりカタカナ化しない。詳細は [tts-pronunciation.md](tts-pronunciation.md)
- VOICEVOX ユーザー辞書 API への永続依存はしない（再現性のため。使うならプロジェクト辞書から都度投入）

話者を変えるのはユーザーが明示したとき、または dialogue の `meta.speakers` で案件が決めたときに限る。

## サブプラン: Irodori-TTS（彩りTTS）

位置づけは **代替オプション** であり、既定移行先ではない。

検討してよい場合:

- 声のクローンや VoiceDesign が必要
- 既存キャラではトーンが足りない
- GPU に余裕があり、バッチ品質を優先する

避けたほうがよい場合:

- まず手早く本数を増やしたい
- GPU / VRAM が他タスクと競合しやすい
- 漢字読みの手直しコストを今は払えない

技術メモ（実装時の目安）:

- GPU 前提。VOICEVOX 比でグラフィック負荷は桁違い（VRAM 数 GB 級が典型）
- 公式 CLI / Gradio、または薄い API ラッパで「テキスト → WAV」だけ差し替え可能
- 漢字読みが弱い場合がある。必要なら読み仮名前処理を挟む
- 声の再現は参照音声または VoiceDesign + seed 固定で行う

切り替え時もキューシート・Remotion 側は維持し、**TTS アダプタだけを替える**。

## 音声ファイル規約（推奨）

```
audio/
  s01.wav
  s02.wav
  ...
```

- ファイル名は `slide_id` と一致させる
- スライド間の間は、音声末尾への無音付与か Remotion 側の空白か、どちらかに統一しキューに明記する

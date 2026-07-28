# Skill memory

運用で得た落とし穴・成功パターンを追記する。秘密情報や環境固有のトークンは書かない。

- 画面は要約しすぎない。主要バレット＋インデント下位項目・具体例で厚くし、ナレーションを追える密度を好む（悪いのは階層なし並列や無関係詰め込み）。
- 概念・比較・フローの枚では図・表を積極採用する。箇条の厚さと両立させる（図のために薄くしない）。
- Mermaid は Marp 生フェンスに頼らない。`@mermaid-js/mermaid-cli`（`mmdc`）で SVG/PNG 先レンダ → `![](...)` 埋め込みが最も確実。
- Mermaid ノード内の改行は `\n` ではなく `<br/>`（`\n` はリテラル文字として残ることがある）。
- ローカル SVG/PNG を埋め込む PNG 書き出しでは Marp CLI に `--allow-local-files` が必須（省略すると図が欠ける）。
- 動きのないスライドショーは Remotion より ffmpeg 静止画結合が速い。fps は 15 を候補に。書き出し後は ffprobe／1 フレーム抽出で NAL 破損を確認する。
- Remotion は同時複数 render や高い concurrency で mux 破損しうる。exit 0 でも再生不能になりうる。
- 数式は Marp `math: mathjax` を採用（PNG 書き出しで数式が焼けることを実測）。KaTeX は CDN フォント依存でオフライン崩れやすい。先レンダ SVG は MathJax が通る限り不要。
- 書き出し後は必ず PNG を目視する。`flowchart TD` や生 `$E=mc^2$` が見えたら失敗としてやり直す。
- 下端の `.note` や長いコードは端欠けしやすい。PNG 目視ゲート（工程 2.5）を省略しない。`overflow: hidden` は修正ではない。
- 画像を枠に収めるとき両軸固定で押しつぶさない。`max-width: 100%; height: auto;` または `object-fit: contain`。
- 未知の英語固有名詞を自動ローマ字読みしない。Gigatoken 等は `pronunciation.yml` に明示（TTS 直前変換）。`narration` SoT と画面英語は維持する。

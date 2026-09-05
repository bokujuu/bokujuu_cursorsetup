---
name: slide-narration-video
description: >-
  全画面スライド＋合成音声の解説動画を設計・制作する。単一ナレーション（monologue）と
  解説役＋聞き手の理解確認型対話（dialogue）のキューシート、Marp、VOICEVOX（既定）／Irodori-TTS（任意）、
  Remotion と Motion Canvas、ffmpeg 静止画結合、発話同期・間、配置 QA、TTS 読み正規化を扱う。
  Use when making explain/talk-through videos from slides, Marp＋TTS 動画、対話形式の解説、
  Remotion／Motion Canvas／ffmpeg 解説動画、キューシート・注釈タイミングの設計時。
---

# 全画面スライド解説動画

Updated: 2026/08/09 23:44

理解を深めるための解説動画を、**全画面スライド＋ナレーション＋必要時の注釈**で作る。
左右分割テンプレや編集ソフト前提のワークフローは採らない。

解説で視聴者が置いていかれやすいときは、一方的な講義（`monologue`）ではなく
**解説役＋聞き手の対話（`dialogue`）**で理解確認・質問・誤解訂正を画面内に置く（[references/dialogue-writing.md](references/dialogue-writing.md)）。
未指定の既定は `monologue`（現行互換）。

## 文章の補助資料（必要な場合のみ）

文章の構成や緩急に具体的な問題があるときだけ参照する。動画制作の前提として一括で読み込まない。

1. [`../japanese-technical-writing/SKILL.md`](../japanese-technical-writing/SKILL.md)  
   スライド／原稿の情報提示順（境界→構成要素→因果→例外）、用語導入、テンプレート方針。
2. [`../cognitive-rhythm-writing/SKILL.md`](../cognitive-rhythm-writing/SKILL.md)  
   ナレーション原稿の緩急・拍・未回収の緊張。読み上げ文は「説明の読み上げ」ではなく、考え進む声で書く。

`dialogue` の各台詞は `references/dialogue-writing.md` を主規範とする。`japanese-technical-writing` はスライドの論理・用語導入・情報提示順に、`cognitive-rhythm-writing` は `monologue` の原稿と `dialogue` の場面接続・話題転換にだけ適用する。JT の常体指定・テンプレート文体や cognitive-rhythm の文の拍を、dialogue の各台詞へ直接移さない。

依存の使い分け:

| 成果物 | 主に従う skill |
|--------|----------------|
| スライドの論理構成・1枚の主張 | japanese-technical-writing |
| monologue 原稿の文の拍・接続 | cognitive-rhythm-writing |
| dialogue の各台詞（会話劇） | 本 skill の dialogue-writing |
| dialogue の場面接続のみ | cognitive-rhythm-writing（各台詞へ機械適用しない） |
| 立ち絵劇場の合成・口パク・登場演出 | 劇場プロファイル側の拡張 skill |
| 尺・同期・レンダリング分担（非劇場） | 本 skill |

## 適用範囲

使う:

- Marp（または同等の Markdown スライド）を全画面で映し、TTS で説明する動画
- 単一ナレーション、または解説役＋聞き手の理解確認型対話のキュー設計
- Remotion でタイムライン／音声合成／書き出しを組むとき
- Motion Canvas で矢印・ハイライト・図解アニメを発話に同期させるとき
- スライド原稿・キューシート・注釈タイミングの新規作成／改稿

使わない:

- インタラクティブデモが主目的（PixiJS / Three.js は原則使わない）
- Adobe Premiere 等の GUI 編集ソフト前提の工程
- ライブ配信・リアルタイム会話エージェント（本 skill はバッチ生成向け）
- 会話劇そのものが目的で、解説・理解確認がないコンテンツ

## 既定スタック

| 層 | 既定 | 備考 |
|----|------|------|
| スライド | Marp → PNG/PDF ページ | 画面全体に表示。要点パネルを左右に常設しない |
| 書き出し（動きなし） | **ffmpeg 静止画結合**（優先） | PNG＋WAV＋pause。fps **15** を候補 |
| タイムライン・音声 mux（モーションあり） | Remotion | Composition の骨格 |
| 精密な注釈アニメ | Motion Canvas | 必要なクリップだけ。常時必須ではない |
| TTS | VOICEVOX（冥鳴ひまり） | monologue 既定。dialogue は `meta.speakers` で役割解決。キャラ変更はユーザー指定時のみ |
| TTS 代替 | Irodori-TTS（彩りTTS） | サブプラン。品質・声の自由度が必要なときだけ |

詳細: [references/tts-and-stack.md](references/tts-and-stack.md)

## 制作フロー

音声と画像が確定してから最終同期を決める。原稿・画像の設計は並行してよい。以下は制作時の目安。

```text
Task Progress:
- [ ] 1. 内部モデルの骨格（JT writing）
- [ ] 1.5 語り口の選択（monologue / dialogue）← 概念の理解確認が中心なら dialogue を推奨
- [ ] 2. スライド設計（全画面・柔軟。dialogue なら一時対話カードの安全域）
- [ ] 2.2 出典図の要否（ソースに図があり文字再現が非効率なら抽出配置。先頭枚に参考URL）
- [ ] 2.5 スライド配置 QA（はみ出し・画像比・対話カード）← 最終合成までに修正する
- [ ] 3. ナレーション原稿（cognitive rhythm／dialogue なら dialogue-writing）
- [ ] 4. キューシート（間・注釈・同期。dialogue は utterances[]）
- [ ] 4.5 TTS 読み正規化（辞書・未解決語）
- [ ] 5. TTS 生成（dialogue は発話ごと＋ターン間 pause）
- [ ] 6. 書き出し（動きなし→ffmpeg 静止画結合／モーションあり→Remotion ± Motion Canvas）
- [ ] 7. 検証（間・同期・配置・読み・対話品質・mp4 健全性）
```

制作中は `process-log.md`（または同等）に工程・判断・NG→修正を残す。

### 1. 内部モデルの骨格

japanese-technical-writing の提示順で、動画全体の主張を一文にし、スライド枚数の上限を決める。
1 概念を不必要に細切れにしない。接続が弱い分割は、枚数を減らすか橋渡し原稿を足す。

### 1.5 語り口の選択（monologue / dialogue）

| モード | 向く案件 | SoT |
|--------|----------|-----|
| `monologue`（既定） | 短い告知・手順・単独語り | `slides[].narration` |
| `dialogue` | 理解確認・誤解訂正・つまずきの先回りが中心 | `slides[].utterances[]`（同一スライドで `narration` を併記しない） |

対話は話者を増やすことが目的ではない。詳細: [references/dialogue-writing.md](references/dialogue-writing.md)

### 2. スライド設計（全画面）

既定の型（柔軟に崩してよい）:

1. 見出し（1 行）— この枚の主張（視線の主張は 1 本。無関係な主張を 1 枚に 2 つ置かない）
2. 核 — 図、または**ナレーションを追える程度に厚い**箇条（主要バレット＋インデント下位項目・具体例）
3. 補足 — 定義・例外など、必要なら行を足してよい
4. 喋り全文・注釈タイミングはスライド外（キューシート側）

**画面情報は要約しすぎない。** 全画面は維持し、左右常設パネルは作らない。  
悪いのは「階層のない 7 点並列」や「無関係な詰め込み」であって、「具体例付きの充実した箇条」ではない。

型に沿いすぎて見にくいときは、エージェント判断で崩す。優先順位は次のとおり。

1. 視線の道が一本あること（主張が画面上で見失われない）
2. 全画面であること（常設の左右パネルを作らない）
3. ナレーションと画面要素が対応して追えること（要約しすぎない）
4. 型の充足

詳細と許容逸脱: [references/slide-design.md](references/slide-design.md)

**概念・比較・因果・公式**の枚では、箇条だけに頼らず図・表・数式を積極採用する（情報密度の厚さは維持）。

| 用途 | 手段 | 確実な載せ方 |
|------|------|--------------|
| 単純な関係図 | Markdown | そのまま |
| 比較・役割一覧 | Markdown 表 | そのまま |
| フロー・パイプライン | Mermaid `.mmd` | **先に SVG/PNG → 画像埋め込み**（生フェンス禁止。PNG 書き出しは `--allow-local-files`） |
| 数式 | LaTeX `$...$` / `$$...$$` | **`math: mathjax`**（PNG 書き出しで焼ける。KaTeX CDN は避ける） |

画像はアスペクト比を維持する（両軸固定で押しつぶさない）。  
レンダ失敗（Mermaid 生テキスト・`$E=mc^2$` のまま）は PNG 目視で落とす。  
詳細: [references/figures-and-math.md](references/figures-and-math.md) / [references/slide-layout-qa.md](references/slide-layout-qa.md)

### 2.5 スライド配置 QA（必須ゲート）

Marp → PNG のあと、**全ページを画像として目視**する。配置の問題を最終合成までに修正する。独立した原稿作成は進めてよい。

確認項目:

- 文字・表・コードが端で欠けていない
- 埋め込み図が歪んでいない（`max-width` + `height: auto` 等）
- 生 Mermaid／生 `$...$` が出ていない
- dialogue で対話カードを使う場合、カードと本文が重なっていない（最小高・下端安全域）

NG 時の修正順（情報削除を最初にしない）: note 退避 → 重複除去 → 表／コード焦点化 → **意味単位の枚分割** → 配置組替 → 下限付き局所 compact。  
`overflow: hidden` で隠すのは修正ではない。

詳細: [references/slide-layout-qa.md](references/slide-layout-qa.md)

### 3. ナレーション原稿

`monologue` の緩急を特に調整するときは cognitive-rhythm-writing を参照できる。`dialogue` の各台詞は dialogue-writing を主規範とし、cognitive-rhythm-writing はスライド間の接続・場面転換だけに使う。加えて動画固有の制約:

- **スライド間の接続文を書く**。次枚の見出しを突然出さない。
- **遷移の直前で回収または橋を置く**。「では〜を見る」型の進行実況だけで繋がない（cognitive-rhythm の駄文判定と同じ）。
- 1 枚あたり、視聴者が視線を置ける長さを確保する。早口で埋めない。
- `dialogue` のときは [references/dialogue-writing.md](references/dialogue-writing.md) に従う。会話劇口調を優先し、各台詞へ cognitive-rhythm を機械適用しない。メタな不安宣言や説明カード字幕は使わない。

### 4. キューシート

原稿・音声・画面を結ぶ単一の SoT を置く（YAML 推奨）。`meta.narration_mode` は `monologue`（既定）または `dialogue`。

共通フィールド:

- `slide_id` / 画像パス
- `pause_after_ms`（既定 **500**。当該スライドのナレーション終了後〜次スライド開始前の認知的な間。尺は音声実測合計＋ターン間 pause＋`pause_after_ms`）
- `cues[]`: 必須は `at_ms` / `type` / `duration_ms`。空間系 cue（`highlight` 等）は `target`、`motion` は `clip` パスなど type 依存フィールドを使う

monologue:

- `narration`（読み上げ全文。製品名は英語のままでよい）

dialogue:

- `utterances[]`（`id` / `speaker`（役割 ID） / `narration`）。同一スライドでトップレベル `narration` を併記しない
- `meta.speakers` で役割 → エンジン／話者を解決する
- `pause_between_turns_ms`（既定候補 **250**。話者交替の短い間）
- cue は単一発話の実測区間内に収める（ターンをまたがない）

同期の設計原則とスキーマ: [references/timeline-and-sync.md](references/timeline-and-sync.md)

### 4.5 TTS 読み正規化（必須）

`narration`（および dialogue の各 `utterances[].narration`）は SoT のまま維持する。VOICEVOX に渡す直前に、プロジェクト辞書（例: `script/pronunciation.yml`）で英字・固有語をカタカナ等へ正規化する。

- 未知の英字語を自動ローマ字推測しない（未解決として止める／警告する）
- 変換ログを残す
- 固有語の初出をスポット試聴する
- 読み辞書を話者ごとに複製しない（必要時だけ話者別 override）

詳細: [references/tts-pronunciation.md](references/tts-pronunciation.md)

### 5. TTS

monologue 既定は VOICEVOX・冥鳴ひまり。dialogue は `meta.speakers` の役割解決に従う。**合成に使う文字列は 4.5 適用後の `tts_text`**。意味内容は SoT の `narration` と一致させる。

dialogue では発話ごとに WAV を生成し、実測長と `pause_between_turns_ms` を累積してタイムラインを確定する。スライド単位の一括 WAV に戻してターン同期を失わない。

Irodori-TTS はサブプラン（[references/tts-and-stack.md](references/tts-and-stack.md)）。

### 6. 書き出し（Remotion × Motion Canvas／ffmpeg）

役割分担（混線させない）:

| 担当 | Remotion | Motion Canvas | ffmpeg 静止画結合 |
|------|----------|---------------|-------------------|
| スライド全画面表示 | ○ | 必要時のみ | ○（PNG を尺ぶん表示） |
| 音声トラック・尺合わせ | ○ | ×（書き出したクリップを載せる） | ○ |
| 単純なフェード／短いハイライト | ○ で足りれば ○ | — | ×（別手段） |
| 矢印・経路・図の組み立てアニメ | — | ○ | × |
| 最終 mp4 書き出し | ○ | × | ○ |

**動きのないスライドショー**（静止 PNG＋ナレーションのみ）は、Remotion の毎フレームキャプチャより **ffmpeg 静止画結合**を優先する。fps は **15** を候補とする。詳細は [references/tts-and-stack.md](references/tts-and-stack.md)。

Motion Canvas クリップは、キューの `at_ms` に合わせて Remotion 側で開始フレームを決める。
「喋っている箇所」と「指している箇所」がずれる状態で書き出さない。

Remotion 未使用ならその旨を README / process-log に残す。書き出し後は再生前に健全性チェック（ffprobe／1 フレーム抽出）を行う。
### 7. 検証チェックリスト

- [ ] 各スライドのナレーション終了後（次スライドへ移る前）に、おおむね 0.5 秒の無音または静止の間がある
- [ ] 早送り感がない（接続文なしの硬切替がない）
- [ ] 各 cue が、対応する発話区間内に収まっている（dialogue ではターンをまたがない）
- [ ] 全画面表示で、常設の左右要点パネルがない
- [ ] 各枚の画面がナレーションを追える密度（下位項目・具体例）で、要約しすぎていない
- [ ] 概念枚で図・表・数式が必要なとき、採用済みで、生 Mermaid／生 `$...$` が画面に出ていない
- [ ] Mermaid ノード改行に `\n` リテラルが残っていない（`<br/>` を使う）
- [ ] **全 PNG で文字が端欠けしていない**（工程 2.5 再確認）
- [ ] **埋め込み画像のアスペクト比が歪んでいない**
- [ ] dialogue の対話カードがある場合、本文と重ならず、動画プレビューでも欠けていない
- [ ] dialogue のとき、聞き手が優等生要約係になっておらず、理解確認または誤解訂正がある
- [ ] dialogue のとき、発話ごとの WAV とターン間 pause から尺が解決されている
- [ ] **読み辞書があり、主要固有語・略語の音声が破綻していない**
- [ ] TTS が既定（VOICEVOX・冥鳴ひまり）または `meta.speakers`／明示された代替である
- [ ] 最終 mp4 の健全性（`pix_fmt` が unknown でない、1 フレーム抽出可）を確認した
- [ ] `process-log.md` に工程と NG→修正が残っている

## 成果物の置き方（リポジトリ非依存の推奨）

プロジェクトに既存規約があればそれに従う。なければ次を推奨する。

```text
<video-project>/
  slides/           # .marp.md と書き出し PNG、assets/
  script/
    manuscript.md   # 通し原稿（任意）
    cues.yaml       # キューシート SoT
    pronunciation.yml  # TTS 読み辞書
  audio/            # TTS WAV、変換ログ（dialogue は発話単位のサブディレクトリ可）
  motion/           # Motion Canvas ソース（任意）
  remotion/         # Remotion ソース
  out/              # 書き出し
  process-log.md    # 制作工程の記録
```

## 追加資料

- [references/dialogue-writing.md](references/dialogue-writing.md) — 解説役＋聞き手の原稿規範
- [references/timeline-and-sync.md](references/timeline-and-sync.md) — 同期・間・スキーマ
- [references/slide-design.md](references/slide-design.md) — 全画面スライドの設計と柔軟性
- [references/slide-layout-qa.md](references/slide-layout-qa.md) — はみ出し・画像比の配置 QA
- [references/figures-and-math.md](references/figures-and-math.md) — 図・表・数式と先レンダ
- [references/tts-and-stack.md](references/tts-and-stack.md) — TTS・描画スタック方針
- [references/tts-pronunciation.md](references/tts-pronunciation.md) — 英語読みの正規化
- [references/examples.md](references/examples.md) — キューシート例
- [references/skill-memory.md](references/skill-memory.md) — 運用で得た落とし穴

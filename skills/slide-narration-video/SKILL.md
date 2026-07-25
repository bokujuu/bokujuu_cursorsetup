---
name: slide-narration-video
description: >-
  全画面スライド＋合成音声ナレーションの解説動画を設計・制作する。Marp スライド、VOICEVOX（既定）／Irodori-TTS（任意）、
  Remotion と Motion Canvas の役割分担、発話と画面注釈の同期、スライド間の認知的な「間」、
  スライド配置 QA（文字はみ出し・画像アスペクト）、英語読みの TTS 正規化を扱う。
  Use when making explain/talk-through videos from slides, Marp＋TTS 動画、Remotion／Motion Canvas 解説動画、
  スライド原稿・キューシート・注釈タイミングの設計、または「全画面で喋らせる」構成の相談・実装時。
---

# 全画面スライド解説動画

理解を深めるための解説動画を、**全画面スライド＋ナレーション＋必要時の注釈**で作る。
左右分割テンプレや編集ソフト前提のワークフローは採らない。

## 併用する規範（必須）

着手前に次を読む。本 skill は原稿・構成の品質を両 skill に委譲する。

1. [`../japanese-technical-writing/SKILL.md`](../japanese-technical-writing/SKILL.md)  
   スライド／原稿の情報提示順（境界→構成要素→因果→例外）、用語導入、テンプレート方針。
2. [`../cognitive-rhythm-writing/SKILL.md`](../cognitive-rhythm-writing/SKILL.md)  
   ナレーション原稿の緩急・拍・未回収の緊張。読み上げ文は「説明の読み上げ」ではなく、考え進む声で書く。

依存の使い分け:

| 成果物 | 主に従う skill |
|--------|----------------|
| スライドの論理構成・1枚の主張 | japanese-technical-writing |
| 喋る原稿の文の拍・接続 | cognitive-rhythm-writing |
| 尺・同期・レンダリング分担 | 本 skill |

## 適用範囲

使う:

- Marp（または同等の Markdown スライド）を全画面で映し、TTS で説明する動画
- Remotion でタイムライン／音声合成／書き出しを組むとき
- Motion Canvas で矢印・ハイライト・図解アニメを発話に同期させるとき
- スライド原稿・キューシート・注釈タイミングの新規作成／改稿

使わない:

- インタラクティブデモが主目的（PixiJS / Three.js は原則使わない）
- Adobe Premiere 等の GUI 編集ソフト前提の工程
- ライブ配信・リアルタイム会話エージェント（本 skill はバッチ生成向け）

## 既定スタック

| 層 | 既定 | 備考 |
|----|------|------|
| スライド | Marp → PNG/PDF ページ | 画面全体に表示。要点パネルを左右に常設しない |
| タイムライン・音声 mux・書き出し | Remotion | Composition の骨格 |
| 精密な注釈アニメ | Motion Canvas | 必要なクリップだけ。常時必須ではない |
| TTS | VOICEVOX（冥鳴ひまり） | キャラ変更はユーザー指定時のみ |
| TTS 代替 | Irodori-TTS（彩りTTS） | サブプラン。品質・声の自由度が必要なときだけ |

詳細: [references/tts-and-stack.md](references/tts-and-stack.md)

## 制作フロー

次の順を崩さない。後工程で論理を取り返すコストが高い。

```text
Task Progress:
- [ ] 1. 内部モデルの骨格（JT writing）
- [ ] 2. スライド設計（全画面・柔軟）
- [ ] 2.5 スライド配置 QA（はみ出し・画像比）← 合格まで 3 に進まない
- [ ] 3. ナレーション原稿（cognitive rhythm）
- [ ] 4. キューシート（間・注釈・同期）
- [ ] 4.5 TTS 読み正規化（辞書・未解決語）
- [ ] 5. TTS 生成
- [ ] 6. Remotion 組み立て（± Motion Canvas）
- [ ] 7. 検証（間・同期・配置・読み）
```

制作中は `process-log.md`（または同等）に工程・判断・NG→修正を残す。

### 1. 内部モデルの骨格

japanese-technical-writing の提示順で、動画全体の主張を一文にし、スライド枚数の上限を決める。
1 概念を不必要に細切れにしない。接続が弱い分割は、枚数を減らすか橋渡し原稿を足す。

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

Marp → PNG のあと、**全ページを画像として目視**する。合格するまで工程 3 に進まない。

確認項目:

- 文字・表・コードが端で欠けていない
- 埋め込み図が歪んでいない（`max-width` + `height: auto` 等）
- 生 Mermaid／生 `$...$` が出ていない

NG 時の修正順（情報削除を最初にしない）: note 退避 → 重複除去 → 表／コード焦点化 → **意味単位の枚分割** → 配置組替 → 下限付き局所 compact。  
`overflow: hidden` で隠すのは修正ではない。

詳細: [references/slide-layout-qa.md](references/slide-layout-qa.md)

### 3. ナレーション原稿

cognitive-rhythm-writing に従う。加えて動画固有の制約:

- **スライド間の接続文を書く**。次枚の見出しを突然出さない。
- **遷移の直前で回収または橋を置く**。「では〜を見る」型の進行実況だけで繋がない（cognitive-rhythm の駄文判定と同じ）。
- 1 枚あたり、聞き手が視線を置ける長さを確保する。早口で埋めない。

### 4. キューシート

原稿・音声・画面を結ぶ単一の SoT を置く（YAML 推奨）。最低限のフィールド:

- `slide_id` / 画像パス
- `narration`（読み上げ全文。製品名は英語のままでよい）
- `pause_after_ms`（既定 **500**。当該スライドのナレーション終了後〜次スライド開始前の認知的な間。尺は `audio_duration_ms + pause_after_ms`）
- `cues[]`: 必須は `at_ms` / `type` / `duration_ms`。空間系 cue（`highlight` 等）は `target`、`motion` は `clip` パスなど type 依存フィールドを使う

同期の設計原則とスキーマ: [references/timeline-and-sync.md](references/timeline-and-sync.md)

### 4.5 TTS 読み正規化（必須）

`narration` は SoT のまま維持する。VOICEVOX に渡す直前に、プロジェクト辞書（例: `script/pronunciation.yml`）で英字・固有語をカタカナ等へ正規化する。

- 未知の英字語を自動ローマ字推測しない（未解決として止める／警告する）
- 変換ログを残す
- 固有語の初出をスポット試聴する

詳細: [references/tts-pronunciation.md](references/tts-pronunciation.md)

### 5. TTS

既定は VOICEVOX・冥鳴ひまり。**合成に使う文字列は 4.5 適用後の `tts_text`**。意味内容は `narration` と一致させる。  
Irodori-TTS はサブプラン（[references/tts-and-stack.md](references/tts-and-stack.md)）。

### 6. Remotion × Motion Canvas

役割分担（混線させない）:

| 担当 | Remotion | Motion Canvas |
|------|----------|---------------|
| スライド全画面表示 | ○ | 必要時のみ |
| 音声トラック・尺合わせ | ○ | ×（書き出したクリップを載せる） |
| 単純なフェード／短いハイライト | ○ で足りれば ○ | — |
| 矢印・経路・図の組み立てアニメ | — | ○ |
| 最終 mp4 書き出し | ○ | × |

Motion Canvas クリップは、キューの `at_ms` に合わせて Remotion 側で開始フレームを決める。
「喋っている箇所」と「指している箇所」がずれる状態で書き出さない。

ffmpeg のみで PNG+WAV+pause を結合してもよい（プロジェクト既存に合わせる）。Remotion 未使用ならその旨を README / process-log に残す。

### 7. 検証チェックリスト

- [ ] 各スライドのナレーション終了後（次スライドへ移る前）に、おおむね 0.5 秒の無音または静止の間がある
- [ ] 早送り感がない（接続文なしの硬切替がない）
- [ ] 各 cue が、対応する発話区間内に収まっている
- [ ] 全画面表示で、常設の左右要点パネルがない
- [ ] 各枚の画面がナレーションを追える密度（下位項目・具体例）で、要約しすぎていない
- [ ] 概念枚で図・表・数式が必要なとき、採用済みで、生 Mermaid／生 `$...$` が画面に出ていない
- [ ] **全 PNG で文字が端欠けしていない**（工程 2.5 再確認）
- [ ] **埋め込み画像のアスペクト比が歪んでいない**
- [ ] **読み辞書があり、主要固有語・略語の音声が破綻していない**
- [ ] 原稿が cognitive-rhythm / JT writing の依存手順を経ている
- [ ] TTS が既定（VOICEVOX・冥鳴ひまり）または明示された代替である
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
  audio/            # TTS WAV、変換ログ
  motion/           # Motion Canvas ソース（任意）
  remotion/         # Remotion ソース
  out/              # 書き出し
  process-log.md    # 制作工程の記録
```

## 追加資料

- [references/timeline-and-sync.md](references/timeline-and-sync.md) — 同期・間・スキーマ
- [references/slide-design.md](references/slide-design.md) — 全画面スライドの設計と柔軟性
- [references/slide-layout-qa.md](references/slide-layout-qa.md) — はみ出し・画像比の配置 QA
- [references/figures-and-math.md](references/figures-and-math.md) — 図・表・数式と先レンダ
- [references/tts-and-stack.md](references/tts-and-stack.md) — TTS・描画スタック方針
- [references/tts-pronunciation.md](references/tts-pronunciation.md) — 英語読みの正規化
- [references/examples.md](references/examples.md) — キューシート例
- [references/skill-memory.md](references/skill-memory.md) — 運用で得た落とし穴

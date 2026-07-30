---
name: md-html-visual-doc
description: >-
  Agent→人間向けの視覚ドキュメントを、Markdown に選択的 HTML を混ぜて作る。
  フロー図・画像引用・折りたたみ・比較ビューが必要なとき、および「MD だと読みにくい」
  「HTML で見やすく」と言われたときに使う。アーキテクチャ長期図は system-structure-viz、
  スライド動画は slide-narration-video、Cursor 対話ダッシュボードは canvas、
  過去セッション掘り起こしは cursor-session-doc に委譲。
disable-model-invocation: false
---

# md-html-visual-doc — Markdown + 選択的 HTML の視覚ドキュメント

エージェントが人間に手順・理解・確認を促す文書で、**文章は Markdown、視覚は必要最小の HTML / 画像**にする。

## いつ使うか

- 手順・確認依頼・評価結果・ギャラリー・比較表を**人がブラウザまたは MD プレビューで読む**
- フロー図・スクリーンショット・折りたたみ詳細・リンクハブが必要
- ユーザーが「見やすい HTML」「MD だと厳しい」「ギャラリー / 左右比較」を求めた

使わない / 委譲:

| 依頼 | 委譲先 |
|------|--------|
| リポ構造・依存の長期図 | `system-structure-viz` |
| Marp + TTS 解説動画 | `slide-narration-video` |
| セッション内の対話型ダッシュボード | Cursor `canvas` skill |
| 散文の構成・文法だけ | `japanese-technical-writing` |
| 過去セッション / transcript の取得・要約 | `cursor-session-doc`（本 skill はその結果を閲覧用に整形する） |
| VisualCave 等のテーマ付き単体図 HTML の丸導入 | しない（パターンのみ [references/sources.md](references/sources.md)） |

## 成果物の型（重要度順に選ぶ）

迷ったら上から採用する。

| 優先 | 型 | いつ | 出力 |
|------|----|------|------|
| **1** | **Companion HTML** | 表が大きい、フィルタ/検索/左右比較、画像多数 | `*.html`（単体で開ける）+ MD は目的・開き方・再生成コマンド・相対リンクのみ |
| **2** | **MD + 画像フロー** | 手順・因果の流れを一目で | `.mmd` → SVG/PNG 事前レンダ → MD に `<figure>` または `![](...)` |
| **3** | **MD 内インライン HTML** | 折りたたみ・キーボード表記・小さな注釈 | `<details>` / `<kbd>` / `<figure>` 等（[references/patterns.md](references/patterns.md)） |
| **4** | **プレーン MD** | 短い確認・1 画面に収まる | HTML なし。表と見出しだけで足りるならこれ |

判断の一般化:

- 大量メディアや対話 UI → Companion HTML。短い導線・目的・再生成は薄い MD
- フローは主経路だけ。不確実なプレビュー環境では画像化を一次にする
- 比較ビューは **入力 → 出力 → 参照** を欠かさない

既定: チャット返答は短く、**成果ファイルのパスと開き方**を明示する。装飾テーマ・多色カード・Inter/Pastel 一式は入れない。

## ワークフロー

1. **読者の仕事を一文で固定する** — 「何を見て、何を決め／実行してほしいか」。
2. **型を選ぶ** — 上表。Companion が要るかは「スクロール地獄になるか」「比較・フィルタが要るか」で判定。
3. **主経路だけ図にする** — ノード目安 8〜15。枝葉は `<details>` か別節。
4. **配置先を決める** — 対象リポの `AGENTS.md` / ユーザー指定の出力先を優先。無指定なら `{成果物ディレクトリ}/`（例: `docs/`・`temp/`・依頼で示されたパス）。特定リポの `scripts/` 構成を前提にしない。
5. **書く** — 散文は `japanese-technical-writing` の境界→構成→因果の順。視覚は [references/templates.md](references/templates.md)。
6. **リンク規律** — 相対パス、`/` 区切り。Windows の `\` を MD/HTML に書かない。
7. **再生成手段** — Companion / 図をスクリプトや `mmdc` で出したなら、同じコマンドを MD 末尾に置く。
8. **自己点検** — [references/patterns.md](references/patterns.md) のチェックリスト。可能なら HTML をブラウザで開き、リンク・画像・検索/フィルタ・コンソールを確認する。

## Companion HTML の最小規約

- 外部ビルド不要なら **1 ファイル**（インライン CSS。CDN 依存は必要時のみ・オフライン可否を明記）。
- 先頭に **目的 1 行 + 使い方（フィルタ等）**。
- 比較系は **入力 → 出力 → 参照（gold 等）** の列を欠かさない。
- 画像ギャラリーはグリッド + パス表示。MD 側に全画像を埋め込まない。
- データ埋め込みは **安全に行う**（[references/templates.md](references/templates.md) の安全規約）。`textContent` / DOM API 優先。文字列連結でタグを組み立てるなら HTML エスケープ必須。`href` / `src` は相対パスまたは許可スキームのみ。
- 生成スクリプトがあるなら、リポ慣習に合わせて `{成果物ディレクトリ}` か既存 `scripts/` に置き、MD から呼ぶ。無ければ手編集と明記。

## フロー図

1. 主経路を文章で 1 文にする。
2. Mermaid（`flowchart` / `sequenceDiagram`）を `.mmd` に書く。
3. **プレビューが Mermaid を描画しない環境**（Marp、一部ビューア、チャット）では SVG/PNG にレンダしてから埋め込む:

```bat
npx --yes @mermaid-js/mermaid-cli@11.4.0 -i {成果物ディレクトリ}/flow.mmd -o {成果物ディレクトリ}/flow.svg -b transparent
```

4. GitHub 等でフェンスが確実に描画される場合のみ、二次として ```mermaid を併記してよい（一次は画像）。

アーキテクチャの長期 SoT 図は本 skill ではなく `system-structure-viz`。

## 報告テンプレ（ユーザー向け・短い）

```markdown
## 視覚ドキュメント

- **型**: Companion HTML | MD+画像フロー | インライン HTML | プレーン MD
- **成果物**: …（パス）
- **開き方**: …
- **再生成**: …（なければ「手編集」）
```

## Reference

- [references/patterns.md](references/patterns.md) — HTML 表現の優先カタログと禁止寄り
- [references/templates.md](references/templates.md) — コピペ用断片と埋め込み安全規約
- [references/sources.md](references/sources.md) — 外部 skill 調査・配置判定
- [references/skill-memory.md](references/skill-memory.md) — 運用メモ

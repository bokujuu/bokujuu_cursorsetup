# md-html-visual-doc — 出典・調査・配置判定

更新: 2026/07/30 21:10

## 外部 skill / ツール調査（2026/07）

| ソース | 概要 | 判定 |
|--------|------|------|
| [varkart/visualcave](https://github.com/varkart/visualcave) | 単体 HTML + Mermaid、テーマ・step-through・export | **丸導入しない**。抽出: 主経路優先・ノード数抑制 |
| [abrinsmead/skills mermaid-viewer](https://github.com/abrinsmead/skills/tree/main/mermaid-viewer) | `.mmd` → 自己完結 HTML | 図専用。MD 手渡し用途とは別。パターン: 事前レンダ |
| [TaiNgo6798/visual-explaining-skill](https://github.com/TaiNgo6798/visual-explaining-skill) | コード解説用単体 HTML | Node 依存が重い。配置: 参考のみ |
| [Agents365-ai/mermaid-skill](https://github.com/Agents365-ai/mermaid-skill) | NL → `.mmd` → PNG/SVG | レンダ手段として有用。slide 技能と重複しうる |
| Cursor Canvas / Docs Canvas | チャット横の React 成果 | 委譲（本 skill 対象外） |
| `templates/structure-viz/` | 構造可視化 Tier 1 / 3 | 本 skill は人間向け手順・比較・ギャラリー |

### パターンカード（abstract-source-patterns 形式）

#### パターン: 主経路優先の短図

- **定義**: 図は一つの物語（critical path）だけを描き、ノードを抑える。
- **除去**: VisualCave の色クラス名・Inter・テーマ UI
- **配置**: global（本 skill のフロー節）
- **根拠**: visualcave SKILL.md

#### パターン: 不確実ホスト向け事前レンダ

- **定義**: Mermaid ソースを残しつつ、配布面では SVG/PNG を一次表示にする。
- **除去**: 特定 CLI バージョンの固定（例は書くが必須化しない）
- **配置**: global（本 skill）+ 既存 `slide-narration-video`
- **根拠**: スライド/ビューアでのフェンス非描画という一般問題

#### パターン: 薄い索引 MD + 閲覧 HTML

- **定義**: 大量メディアや対話 UI は HTML、MD は目的・リンク・再生成に留める。
- **除去**: 案件固有のギャラリーファイル名・個人履歴
- **配置**: global（本 skill P1）
- **根拠**: 可読性のための媒体分離という一般パターン

#### パターン: 入力→出力列の明示

- **定義**: 比較ビューは変換の入出力（と参照）を並べ、読者が評価可能にする。
- **除去**: 特定データセット名
- **配置**: global（Companion 規約）
- **根拠**: 評価・差分確認の一般要件

## 既存資産との境界

| 資産 | 関係 |
|------|------|
| `japanese-technical-writing` | 文章の論理・体裁。本 skill はチャネル（MD/HTML/図） |
| `templates/structure-viz/` | リポ構造の長期図 |
| `slide-narration-video` | スライド動画。Mermaid 事前レンダは共有パターン |
| `cursor-session-doc` | transcript 掘り起こし・要約。本 skill は閲覧用整形のみ |
| Cursor `canvas` | セッション内対話ダッシュボード |

設計メモ（任意）: [docs/pr/017-md-html-visual-doc.md](../../../docs/pr/017-md-html-visual-doc.md)

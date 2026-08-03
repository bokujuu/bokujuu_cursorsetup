# PR 017 — md-html-visual-doc

更新: 2026/07/30 21:10

## 目的

Agent→人間向けの手順・比較・ギャラリー文書で、Markdown に選択的 HTML を混ぜる（または薄い MD + Companion HTML）グローバル skill を追加する。

## 採用判断

- **入れる**: 媒体選択（プレーン MD / インライン HTML / Companion HTML / 事前レンダ図）、主経路優先、相対リンク、埋め込みエスケープ、既存 skill への委譲表
- **入れない**: VisualCave 等のテーマ付き単体図ツールの丸同梱、個人チャット履歴・ローカルパスへの依存

## 既存との境界

| 既存 | 境界 |
|------|------|
| `templates/structure-viz/` | リポ構造の長期図 |
| `slide-narration-video` | スライド＋TTS。Mermaid 事前レンダは共有パターン |
| `japanese-technical-writing` | 散文の論理・体裁 |
| `cursor-session-doc` | transcript 掘り起こし。本 skill は閲覧整形 |
| Cursor canvas | セッション内ダッシュボード |

## 検証

```bat
.\scripts\install.ps1
python scripts\verify_repo_setup.py
python scripts\verify_loop_kit.py
```

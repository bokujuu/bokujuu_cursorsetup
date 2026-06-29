---
title: mizchi — 技術記事と専門家としての言語化（AI 時代）
tags:
  - ai
  - automation
  - reference
created: 2026-06-29
updated: 2026-06-29
status: active
type: reference
source_repo: bokujuu/bokujuu_cursorsetup
summary: Zennfes 2026 資料。AI 時代の技術記事の役割と専門家の言語化の再定義
---

# mizchi — 技術記事と専門家としての言語化（AI 時代）

## 背景

2026/06 ブックマークレビュー対象。Speaker Deck（Zennfes 2026）。

- https://speakerdeck.com/mizchi/ji-shu-ji-shi-zhuan-men-jia-tositenopurogurama-yan-yu-hua
- テキスト版 gist: https://gist.github.com/mizchi/7042f8ebb6e3d806555222d14d058f8b

## 判断

`bokujuu_cursorsetup` の global 設定には**採用しない**。思想・執筆方針の背景として knowledge-base に残す。

## 核心メッセージ（抽象化）

| テーマ | 内容 |
|--------|------|
| 消費者の変化 | 技術記事の一次消費者は人間から AI へシフトしつつある |
| 記事の価値 | 情報伝達より**専門家の評価・検証・ポストモーテム**の共有 |
| 言語化 | 暗黙知を分析ツール等に落とし、AI で反復検証してから記事化 |
| 専門性 | プログラマは「コード作業員」ではなく、ドメイン抽象と検証の専門家 |

## global に入れない理由

- 執筆哲学であり、常時適用の手順ではない
- 既存 `japanese-technical-writing` は体裁・構成の手順が中心。思想は references で足りる

## knowledge-base に残す理由

- 今後、postmortem テンプレや `retrospective-codify` の説明背景として参照できる
- AI 生成記事との差別化の判断材料

## 再利用できる観点

- 技術記事に「失敗談・採用後の推移」を必ず含める基準
- 言語化 = ツール化 + 検証ループ + 記事化の順序

## 関連

- bokujuu_cursorsetup: `skills/japanese-technical-writing/`
- 採用判断 skill: `abstract-source-patterns`（cursorsetup 側 PR 004）

---
title: 2026-06 ブックマーク採用判断まとめ
tags:
  - ai
  - automation
  - reference
created: 2026-06-29
updated: 2026-06-29
status: active
type: reference
source_repo: bokujuu/bokujuu_cursorsetup
summary: 週次ブックマークの abstract-source-patterns 判定結果と配置先
---

# 2026-06 ブックマーク採用判断まとめ

## 判定方法

`bokujuu_cursorsetup` の skill `abstract-source-patterns` に従い 2 段階判定。

## 結果一覧

| ソース | cursorsetup | knowledge-base |
|--------|-------------|----------------|
| [7人の意地悪なQA](https://zenn.dev/nexta_/articles/be13a2395a5d2a) | `templates/project-skills/qa-multi-perspective/`（**項目 3**） | — |
| [TAKT Faceted prompting](https://github.com/nrslib/takt) | `templates/loop-orchestration/facets/`（**項目 4**） | [takt-agent-coordination.md](takt-agent-coordination.md)（CLI 比較） |
| [ds-ai-coding-skills](https://github.com/atsushi-green/ds-ai-coding-skills) | —（項目 4 と誤マッピングしていた） | [ds-ai-coding-skills-template.md](ds-ai-coding-skills-template.md) |
| mizchi Speaker Deck | — | [mizchi-technical-writing-ai-era.md](mizchi-technical-writing-ai-era.md) |
| goal-setter-skill | — | [goal-setter-completion-contracts.md](goal-setter-completion-contracts.md) |
| サイバネティクス記事 | — | [loop-engineering-cybernetics.md](../../research/loop-engineering-cybernetics.md) |
| headroom | — | [headroom-context-compression.md](headroom-context-compression.md) |

## 項目 3 と 4 の対応（正）

| 項目 | アイデア | 配置 |
|------|----------|------|
| 3 | 7 ペルソナによるテスト観点固定 | project-skill |
| 4 | Faceted prompting（5 種 facet 分離） | loop-orchestration/facets |

## 設計メモ（cursorsetup）

- [PR 004 設計](https://github.com/bokujuu/bokujuu_cursorsetup/blob/main/docs/pr/004-qa-faceted-adoption.md)

## 関連

- [bokujuu-cursorsetup-integration.md](../bokujuu-cursorsetup-integration.md)

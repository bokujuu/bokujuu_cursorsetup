---
title: ds-ai-coding-skills — DS 向けエージェント指示テンプレ
tags:
  - ai
  - automation
  - reference
created: 2026-06-29
updated: 2026-06-29
status: active
type: reference
source_repo: bokujuu/bokujuu_cursorsetup
summary: Data Science 向け AGENTS/skills テンプレ。bokujuu_cursorsetup には非採用
---

# ds-ai-coding-skills — DS 向けエージェント指示テンプレ

## 背景

- https://github.com/atsushi-green/ds-ai-coding-skills
- Copilot / Claude Code 向け DS 分析プロジェクトテンプレ（AGENTS ルーター、10 スキル、raw データ保護 verify）

## 判断

`bokujuu_cursorsetup` には**非採用**。2026/06 ブックマークの「項目 4」と誤ってマッピングされていたが、ユーザー意図の項目 4 は **TAKT Faceted prompting**（cursorsetup には `templates/loop-orchestration/facets/` として採用）。

## 抽象パターン（参考程度）

| パターン | 説明 |
|----------|------|
| 薄いルーター AGENTS | タスク → skill / docs への分岐 |
| docs/agent SoT | 指標・データ意味は docs、手順は skill |
| データ安全 verify | raw コミット・秘密パターン検出 |

DS 案件で必要なら、対象 repo で `repo-agent-bootstrap` + `skill-lifecycle` から個別に構築する。

## 関連

- 採用済み（項目 4）: bokujuu_cursorsetup `templates/loop-orchestration/facets/`
- [bookmark-adoption-2026-06.md](bookmark-adoption-2026-06.md)

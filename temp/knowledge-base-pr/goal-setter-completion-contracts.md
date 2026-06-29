---
title: goal-setter-skill — /goal 完了契約パターン
tags:
  - ai
  - automation
  - reference
created: 2026-06-29
updated: 2026-06-29
status: active
type: reference
source_repo: bokujuu/bokujuu_cursorsetup
summary: Codex /goal 向け完了契約整形 skill。本 repo には非採用、パターンのみ記録
---

# goal-setter-skill — /goal 完了契約パターン

## 背景

- https://github.com/gotalab/goal-setter-skill
- 雑な依頼を「完了条件・検証・制約・停止条件・subagent 割り当て」を含む短い `/goal` 用プロンプトに整形する Agent Skill

## 判断

`bokujuu_cursorsetup` には**非採用**（Codex `/goal` 専用。Cursor Ralph キットとは別プロダクト機能）。

## 抽象パターン

**完了契約（completion contract）**: 作業開始前に、証拠で閉じられる完了定義を短文化する。

| 要素 | 意味 |
|------|------|
| 完了条件 | 何ができたら終わりか |
| 検証方法 | どのコマンド・観測で確認するか |
| 制約 | 触ってはいけない範囲 |
| 停止条件 | ループ・試行の打ち切り |
| 役割割り当て | 別スレッド / subagent が必要な場合のみ |

## 本 repo との関係

- `ralph-loop` + `templates/loop-orchestration/` は外側ループと `ROADMAP.md` で類似の「完了シグナル」を持つ
- goal-setter は**1 セッション内の goal 整形**に特化。統合するなら `PROMPT.md.template` や完了契約テンプレへのパターン移植が候補（別 PR）

## global に入れない理由

- 外部 repo の install 依存
- `/goal` コマンドへの結合

## knowledge-base に残す理由

- ループ設計・依頼の書き方の比較表の 1 行として再利用
- 「手順固定より検証固定」の設計思想の参照

## 関連

- Addy Osmani Loop Engineering
- bokujuu_cursorsetup: `docs/loop-engineering.md`, `skills/ralph-loop/`

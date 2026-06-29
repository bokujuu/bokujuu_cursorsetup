---
title: TAKT — YAML エージェント協調 CLI
tags:
  - ai
  - automation
  - reference
created: 2026-06-29
updated: 2026-06-29
status: active
type: reference
source_repo: bokujuu/bokujuu_cursorsetup
summary: plan-implement-review-fix を YAML で強制する外部 CLI。採用せず比較参照として記録
---

# TAKT — YAML エージェント協調 CLI

## 背景

- https://github.com/nrslib/takt
- `npm install -g takt`。ワークフローを YAML で定義し、plan → implement → review → fix をエージェントの裁量に任せない
- Cursor / Codex / Claude Code 等をプロバイダとして利用可能

## 判断

`bokujuu_cursorsetup` には**CLI 本体は非採用**。Faceted prompting パターンのみ `templates/loop-orchestration/facets/` に抽象化して採用済み（2026/06 ブックマーク項目 4）。

## 抽象パターン（取り込み可能な思想）

| パターン | 説明 |
|----------|------|
| プロセスの外部化 | プロンプトでお願いするのではなく、遷移を宣言的に所有 |
| レビュースキップ不可 | review → fix の明示ループ |
| コンテキスト分割 | persona / policy / knowledge / output contract をステップごとに分離 |
| worktree 分離 | タスクごとに隔離実行・ログ・PR まで追跡 |

## 比較（本 repo Ralph キット）

| 観点 | TAKT | bokujuu Ralph キット |
|------|------|----------------------|
| オーケストレータ | takt CLI（npm） | `ralph.ps1` / `ralph.mjs` / Automations |
| 状態 | `.takt/runs/` 等 | git + `ROADMAP.md` + `progress.txt` |
| レビューループ | YAML 組み込み | テンプレ拡張で対応可能（未同梱） |
| 依存 | Node + プロバイダ CLI/SDK | Cursor CLI / SDK |

## いつ TAKT を検討するか

- レビュー・fix ループを**ツール側で強制**したい
- 複数プロバイダを YAML で切り替えたい
- worktree キュー運用が主用途

## いつ Ralph キットを使うか

- Cursor Cloud / `cursor-agent -p` 中心
- 状態を git とファイルに残すシンプルな Ralph パターンで足りる

## 関連

- bokujuu_cursorsetup: `docs/loop-engineering.md`, `skills/ralph-loop/`
- knowledge-base: [loop-engineering-cybernetics.md](../../research/loop-engineering-cybernetics.md)

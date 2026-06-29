---
title: ループエンジニアリングとサイバネティクス
tags:
  - ai
  - automation
  - research
created: 2026-06-29
updated: 2026-06-29
status: active
type: research
source_repo: bokujuu/bokujuu_cursorsetup
summary: 2026 流行語「ループエンジニアリング」の理論的背景（サイバネティクス・制御・reconcile）
---

# ループエンジニアリングとサイバネティクス

## 背景

- はてなブログ: https://syu-m-5151.hatenablog.com/entry/2026/06/23/215158
- 2026/06 に Steinberger・Osmani 等により広まった「Loop Engineering」を、サイバネティクス・Kubernetes reconcile・t-wada の Reconciliation Loop で測り直す記事

## 判断

`bokujuu_cursorsetup` の `docs/loop-engineering.md` は実装寄り。理論背景は knowledge-base に残し、必要時に cursorsetup からリンクする。

## 核心（抽象化）

| 概念 | ループエンジニアリングでの意味 |
|------|-------------------------------|
| 新しさの半分 | サイバネティクス・制御理論の再発見 |
| 新しさの半分 | 舵を握る主体が決定論的コントローラから LLM へ |
| Reconciliation | desired state と observed state の差分を縮める反復 |
| 人間の役割 | 実行者 → ループの設計者・統治者 |

## 3 段階モデル（参考: Zenn noragrammer 等）

| 段階 | ループの主体 | 停止判定 |
|------|-------------|----------|
| Loop in the Human | 人間 | 人間 |
| Loop on the Human | エージェント | 人間 |
| Loop Engineering | エージェント + 独立 Evaluator | Evaluator |

bokujuu の Ralph キットは「verify exit 0 + COMPLETE シグナル」で Evaluator 寄りの設計を志向。

## global に入れない理由

- 長文の理論解説は配布ドキュメントのスコープ外
- 実装手順は既に `loop-engineering.md` にある

## knowledge-base に残す理由

- 流行語の実体を説明する際の背景資料
- takt / goal-setter / Ralph の比較議論の共通語彙

## 関連

- [goal-setter-completion-contracts.md](../ai/automations/goal-setter-completion-contracts.md)
- [takt-agent-coordination.md](../ai/automations/takt-agent-coordination.md)
- Addy Osmani: https://addyosmani.com/blog/loop-engineering/
- bokujuu_cursorsetup: `docs/loop-engineering.md`

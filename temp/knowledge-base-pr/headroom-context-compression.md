---
title: Headroom — LLM 向けコンテキスト圧縮
tags:
  - ai
  - automation
  - reference
created: 2026-06-29
updated: 2026-06-29
status: active
type: reference
source_repo: bokujuu/bokujuu_cursorsetup
summary: tool output / log / RAG を LLM 投入前に圧縮する OSS。採用せずツールカタログとして記録
---

# Headroom — LLM 向けコンテキスト圧縮

## 背景

- https://github.com/chopratejas/headroom
- tool output・ログ・ファイル・RAG chunk を LLM 到達前に圧縮（60–95% 削減を主張）
- library / proxy / MCP / agent wrap（`headroom wrap cursor` 等）

## 判断

`bokujuu_cursorsetup` には**非採用**。外部ランタイム依存であり、全 repo への global 強制は副作用が大きい。

## 抽象パターン

| パターン | 説明 |
|----------|------|
| コンテキスト予算 | 送る前に圧縮し、トークンコストと latency を抑える |
| 可逆圧縮（CCR） | 原文をキャッシュし、必要時に retrieve |
| コンテンツルーティング | JSON / AST / テキストで圧縮器を切り替え |

## 検討タイミング

- verify ログや RAG チャンクがコンテキスト上限に頻繁に達する
- API コストがボトルネックになったとき
- MCP 経由でエージェントに圧縮ツールを渡したいとき

## 注意

- 星数は注目度の指標であり品質保証ではない
- 圧縮により検証に必要な情報が落ちるリスク — タスクに応じて on/off

## 関連

- bokujuu_cursorsetup: `skills/cursor-session-doc/`（巨大 jsonl 要約）
- `docs/fast-agent-test-loop.md`（verify 高速化は別軸）

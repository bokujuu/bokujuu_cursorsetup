# Agent handoff recovery — 設計メモ

更新: 2026/06/02 15:30

## 目的

エージェントへの指示が伝わらず実装がずれる、セッションをまたいで Plan とコードが乖離する、サブエージェント結果が統合されない、といった**横断的な失敗**を、プロジェクトごとではなくグローバル設定で検知・折り返す。

## 3 層

| 層 | 配布物 | 役割 |
|----|--------|------|
| Skill | `skills/agent-handoff-recovery/` | 回復ループ・状況整理テンプレ（本体） |
| Hook（任意） | `hooks/handoff-stop-check.py` | `stop` / `subagentStop` で follow-up |

プロジェクト固有の verify コマンドは **リポジトリ側** の `.cursor/handoff-recovery.local.md`（テンプレ: skill 内 `project-extension-template.md`）。

## Hook の制限

- stdin なしでスクリプトを実行すると `read()` でブロックする（Cursor 経由のみ想定）
- 出力は ASCII のみ（Windows コンソール cp932 対策）
- 既存 `hooks.json` がある環境では上書きせず手動マージ（`hooks/README.md`）

## 関連 skill

- `anti-human-bottleneck` — 回復は自律、質問は最小

## 出自

PCAF モック開発で Plan / 実装 / 検証のズレが再発したことを契機に設計（2026/06）。

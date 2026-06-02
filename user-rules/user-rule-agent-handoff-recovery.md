---
name: エージェント引き継ぎ回復
version: 1.0.0
description: 指示ずれ・Plan未整合・検証スキップ・サブエージェント未統合を検知したとき、実装を止めて状況整理する。層B（タスク時）または cursor-integrated への短い追記用。
appliesTo: always
---

# エージェント引き継ぎ回復（トリガー）

次のいずれかなら、**実装を止めて** skill `agent-handoff-recovery` を読み、回復ループを実行する。

- ユーザーが期待と違う・伝わっていないと述べた
- Plan の todo が `pending`/`in_progress` のまま完了扱い（またはその逆）
- バックグラウンド subagent 完了後、親が統合・検証せず確認だけした
- 無関係な複数トラックを同一セッションで編集した
- `AGENTS.md` の verify/build を実行せず「完了」と言おうとしている

ユーザー向けには短い **状況整理**（トラック / SoT / Plan / 検証 / 次）を出す。トラックと完了条件が読んでも不明なときだけ質問する。

詳細ワークフローは skill `agent-handoff-recovery`（`install.ps1` 後は `~/.codex/skills/agent-handoff-recovery/`）を正とする。

# PR 設計メモ: fable-style-reasoning

更新: 2026/07/07

## 目的

Anthropic 公式開示（Fable 5 認識論）を**主骨**とし、公式にない模倣手順を**補助**として載せたグローバル skill。任意エージェントで観測優先の推論を再現する。

## 層構造

| 層 | 出典 |
|----|------|
| 主骨 | [System Prompts — Fable 5](https://platform.claude.com/docs/en/release-notes/system-prompts) |
| 補助 | [shotatykr 挙動トレース](https://x.com/shotatykr/status/2074035238116769851) |
| 参考 | CL4R1T4S 等（パターンのみ） |

## 設計判断

| 項目 | 決定 |
|------|------|
| slug | `fable-style-reasoning`（Anthropic 非公式を明示） |
| モード | 使わない / 軽量（主骨のみ）/ フル（Phase 0–4）/ 回復委譲 |
| 錨の SoT | `.cursor/plans/*.plan.md` 先頭 |
| 有効性セクション | SKILL.md には置かない（[Skill best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices): description で発見、詳細は references） |
| eval | `references/eval-scenarios.md` |
| 運用メモ | `references/skill-memory.md` |

## 関連更新

- `MANIFEST.md` / `docs/rule-index.md`
- `.codex/practice-registry.json`（draft）
- `skills/repo-agent-bootstrap` — AGENTS 雛形・関連 skill 一覧
- `skills/abstract-source-patterns/references/sources.md` — 採用先例
- `skills/agent-handoff-recovery` — サブエージェント統合の相互参照

## 検証

```bash
bash scripts/install.sh
python3 scripts/verify_repo_setup.py
```

手動: `references/eval-scenarios.md` の 3 シナリオ。

## 意図的に後回し

- 他 skill との詳細な優先順位表（`anti-human-bottleneck` 等）— 運用で摩擦が出たら skill-memory へ

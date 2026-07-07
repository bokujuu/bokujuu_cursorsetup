# fable-style-reasoning — 出典・層構造

## 層の定義

| 層 | 意味 | 採用基準 |
|----|------|----------|
| **主骨** | skill 設計の**基本思想** | Anthropic **公式**開示のみ |
| **補助** | 主骨を手順に落とす**実践知** | 公式にないが主骨と矛盾しないもの |
| **参考** | 非公式抽出のパターン | パターンのみ。本文コピー禁止 |

補助は公式の穴埋め。軽量モードでは主骨のみで足りる。

---

## 主骨 — Anthropic 公式

| ソース | skill への反映 |
|--------|----------------|
| [System Prompts — Claude Fable 5 (2026-06-09)](https://platform.claude.com/docs/en/release-notes/system-prompts) | 認識論、自己確認、誠実な訂正、カットオフ後の確認姿勢 |
| [Fable 5 safeguards (2026-07-02)](https://www.anthropic.com/news/fable-safeguards-jailbreak-framework) | 開示方針の文脈（安全拒否のコピーではない） |

### 公式周辺（release-notes 系列）

- skill 優先 Read、ツール確認、複雑度に応じた確認深度

### 公式にないもの（→ 補助）

- Phase 0–4、錨テンプレ、事実/仮定/不明、リスク順分解、模倣ロジック全般

---

## 補助 — コミュニティ実践知

| ソース | skill への反映 |
|--------|----------------|
| [shotatykr — Fable skill 構想](https://x.com/shotatykr/status/2074035238116769851) | Phase 0–4、補助三原則、4 自問、全体検証 5 点 |
| [shotatykr — 思考の言語化](https://x.com/shotatykr/status/2074148603619348887) | 手順言語化の動機 |

---

## 参考 — 非公式（未検証）

| ソース | 扱い |
|--------|------|
| [CL4R1T4S / CLAUDE-FABLE-5.md](https://github.com/elder-plinius/CL4R1T4S/blob/main/ANTHROPIC/CLAUDE-FABLE-5.md) | 主骨と整合するパターンのみ |
| [ayautomate — leak 解説](https://www.ayautomate.com/blog/claude-fable-5-system-prompt-leak) | 設計教訓のみ |

---

## 関連 skill

| skill | 関係 |
|-------|------|
| `abstract-source-patterns` | 層分け・配置判定 |
| `agent-handoff-recovery` | ずれ発生後・サブエージェント統合 |
| `repo-agent-bootstrap` | 新規 repo の AGENTS 雛形から参照 |

## global suitability

- 公式思想を主骨に据えた汎用エージェント推論。slug は `fable-style-reasoning`（Anthropic 非公式であることを明示）。

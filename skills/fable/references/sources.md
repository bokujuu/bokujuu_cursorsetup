# fable — 出典・層構造

## 層の定義

| 層 | 意味 | 採用基準 |
|----|------|----------|
| **主骨** | skill 設計の**基本思想** | Anthropic **公式**開示のみ |
| **補助** | 主骨を手順・チェックリストに落とす**実践知** | 公式にないが主骨と矛盾しないもの |
| **参考** | 非公式抽出から得たパターン | パターンのみ。本文コピー禁止 |

補助は「公式の穴埋め」として置く。主骨だけで足りる単純タスクでは Phase 0–4 を省略してよい。

---

## 主骨 — Anthropic 公式

| ソース | 信頼度 | skill への反映 |
|--------|--------|----------------|
| [System Prompts — Claude Fable 5 (2026-06-09)](https://platform.claude.com/docs/en/release-notes/system-prompts) | **公式** | 認識論、自己確認、誠実な訂正、カットオフ後の確認姿勢 |
| [Fable 5 safeguards (2026-07-02)](https://www.anthropic.com/news/fable-safeguards-jailbreak-framework) | **公式** | システムプロンプト開示方針の文脈（本 skill は安全拒否のコピーではない） |

### 公式から取り込んだ思想（要旨）

- **good epistemology**: 検証不能なこと（他者の心理状態等）を断定しない。エージェント文脈では「未確認の技術状態」にも適用。
- **check for itself**: プロンプトがファイル等の存在を示唆しても、自分で確認する。
- **knowledge cutoff**: 変わりうる現状は記憶より確認・検索。
- **mistake handling**: 誤りを認め、観測に基づき修正する。

### 公式周辺（同一 release-notes 系列・エージェント向け拡張）

Fable 5 単体エントリに明文化されていないが、Anthropic 消費者プロンプト系列で一貫する方針として主骨に含めたもの:

- コード・ファイル作業前の **skill 優先 Read**
- ツール可用性の確認
- タスク複雑度に応じた確認の深さ

これらは**思想の延長**であり、Phase 番号付きワークフローではない。

### 公式に**ない**もの（→ 補助へ）

- Phase 0–4 の手順番号
- 「錨の 3 行」テンプレート
- 事実 / 仮定 / 不明の仕分け表
- リスク順分解・4 自問・全体検証 5 点のチェックリスト
- Fable 挙動の**模倣ロジック**全般

---

## 補助 — コミュニティ実践知

| ソース | 信頼度 | skill への反映 |
|--------|--------|----------------|
| [豊藏 翔太 @shotatykr — Fable skill 構想](https://x.com/shotatykr/status/2074035238116769851) | コミュニティ（挙動トレース） | Phase 0–4、補助三原則、4 自問、全体検証 5 点 |
| [豊藏 翔太 @shotatykr — 思考プロセスの言語化](https://x.com/shotatykr/status/2074148603619348887) | コミュニティ | 手順の言語化・模倣の動機の補足 |

採用理由: 公式主骨だけでは「エージェントが Fable 型に**どう動くか**」まで手順化されない。shotatykr 氏のトレースはその**穴埋め**として位置づける。

採用しないもの: 主骨（公式認識論）と矛盾する shortcut、モデル固有の製品話、検証なき完了。

---

## 参考 — 非公式抽出（未検証）

| ソース | 信頼度 | 扱い |
|--------|--------|------|
| [CL4R1T4S / CLAUDE-FABLE-5.md](https://github.com/elder-plinius/CL4R1T4S/blob/main/ANTHROPIC/CLAUDE-FABLE-5.md) | 非公式・未確認 | 主骨の skills-first 等と整合するパターンのみ参考。採用判断は公式優先 |
| [ayautomate — leak 解説](https://www.ayautomate.com/blog/claude-fable-5-system-prompt-leak) | 二次解説 | 命名セクション・ネガティブ例等の**設計教訓**のみ |

---

## 本 repo 内の関連 skill

| skill | 関係 |
|-------|------|
| `abstract-source-patterns` | 外部ソースの層分け・配置判定 |
| `agent-handoff-recovery` | ずれ発生後。fable は主骨＋予防 |
| `anti-human-bottleneck` | Phase 3 のエスカレーション境界 |
| `ralph-loop` | 外側ループ |

## global suitability 判定メモ

- **採用理由**: 公式思想を主骨に据えたエージェント推論パターン。複数 repo で再利用可能。
- **補助の位置づけ**: 公式の代替ではなく、模倣手順の明示的な穴埋め。
- **不採用**: 安全拒否ハンドリング全文、ツール JSON スキーマ、非公式プロンプトのコピペ。

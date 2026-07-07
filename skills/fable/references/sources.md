# fable — 出典・採用経緯

## 着想（コミュニティ）

| ソース | 内容 | 採用したもの |
|--------|------|--------------|
| [豊藏 翔太 @shotatykr — Fable skill 構想](https://x.com/shotatykr/status/2074035238116769851) | Fable 5.0 の出力をトレースし `/fable` skill 化。三原則・Phase 0–4・4 自問・全体検証 5 点 | **本 skill の主骨**（抽象化してモデル非依存に再実装） |
| [豊藏 翔太 @shotatykr — 思考プロセスの言語化](https://x.com/shotatykr/status/2074148603619348887) | 高能力モデルの手順をなぞる効果 | skill 化の動機の補足 |

## Anthropic 公式開示

| ソース | 信頼度 | 本 skill への反映 |
|--------|--------|-------------------|
| [System Prompts — Claude Fable 5 (2026-06-09)](https://platform.claude.com/docs/en/release-notes/system-prompts) | **公式**（消費者向け chat の一部。API には非適用と明記） | 認識論（観測不能なことは断定しない）、現状確認の優先、ファイル存在の自己確認 |
| [Fable 5 safeguards / jailbreak framework (2026-07-02)](https://www.anthropic.com/news/fable-safeguards-jailbreak-framework) | **公式** | システムプロンプト開示方針の文脈。本 skill は安全制限のコピーではない |

公式 Fable 5 エントリに含まれる関連抜粋（要旨）:

- 個人の心理状態等について、検証不能な主張を避ける（good epistemology）
- プロンプトがファイル存在を示唆しても、実際に確認する
- 知識カットオフ以降の現状は、必要なら検索・確認する

**注意**: 公式開示は製品情報・振る舞い・安全の大部分であり、shotatykr 氏が観測した **Phase 0–4 のエージェント手順は公式ドキュメントには含まれない**。それらはコミュニティの挙動トレースに基づく。

## 非公式抽出（参考のみ・未検証）

| ソース | 信頼度 | 本 skill への反映 |
|--------|--------|-------------------|
| [CL4R1T4S / CLAUDE-FABLE-5.md](https://github.com/elder-plinius/CL4R1T4S/blob/main/ANTHROPIC/CLAUDE-FABLE-5.md) | 非公式・未確認 | skills をコード前に Read する方針、ツール可用性の確認、タスク複雑度に応じたツール回数 |
| [ayautomate — 9 lessons from leak](https://www.ayautomate.com/blog/claude-fable-5-system-prompt-leak) | 二次解説 | 命名セクション・ネガティブ例・能力仕様優先の設計教訓（パターンのみ採用、本文コピーなし） |

非公式テキストは**そのまま転載しない**。パターンが他 repo でも有効なものだけ抽象化した。

## 本 repo 内の関連 skill

| skill | 関係 |
|-------|------|
| `agent-handoff-recovery` | ずれ発生後のリカバリ。fable は予防・実行規律 |
| `abstract-source-patterns` | 外部ソースからの抽象化手順。本 skill 作成時に参照 |
| `anti-human-bottleneck` | Phase 3 の人間エスカレーション境界 |
| `ralph-loop` | 外側ループとの併用 |

## global suitability 判定メモ

- **採用理由**: モデル・リポ非依存のエージェント推論パターン。複数 repo で再利用可能。
- **不採用にしたもの**: Fable 固有の製品説明、安全拒否ハンドリング、ツール JSON スキーマの全文、非公式プロンプトのコピペ。

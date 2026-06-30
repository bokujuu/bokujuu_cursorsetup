# 出典

## ユーザー運用・設計源

- `htmlPCAFmock` — 運用 Excel（COM ビルド・承認ワークフロー）でのダミー／素データ運用。
  不満の顕在化（行数・グループ・境界）の契機。帳票側は `excel-deliverable-quality`。
- `utf_ken_all` — 取込 CSV・文字コード・`dtype=str` 前提の整形運用。

## 本リポジトリ内

- `skills/excel-deliverable-quality` — 成果物品質・ビルド・検証（素データ設計は本 skill）
- `templates/project-skills/qa-multi-perspective/` — データ整合・移行観点（P4/P5）
- `templates/project-rules/excel/pcaf-excel-agent.mdc.example` — SoT・検証の例

## 外部（一般原則のみ参照・本文コピーなし）

| テーマ | URL | 採用した考え方 |
|--------|-----|----------------|
| 決定性・seed・manifest | https://www.elysiate.com/blog/deterministic-csv-for-tests-seeds-timestamps-and-ids | 固定 seed、凍結時刻、明示ソート、checksum |
| テストデータ戦略 | https://archman.dev/docs/testing-strategy/test-automation/test-data-fixtures-synthetic-data | fixture / factory / synthetic の使い分け、分離 |
| 合成データ運用 | https://beefed.ai/en/test-data-management-synthetic-generation | 回帰は決定的、探索はランダム、バージョン管理 |
| 並列・一意制約 | https://elliot-digital.co.uk/qa/test-data-management | シーケンス衝突、worker オフセット、ビジネス不変条件の検証 |

## 併用ツール（設計 skill と併記。本文コピーなし）

| ツール | URL | 本 skill との関係 |
|--------|-----|-------------------|
| factory_boy | https://factoryboy.readthedocs.io/ | Python Factory。グループ内行の組み立て → CSV/JSON 書き出し |
| Faker | https://faker.readthedocs.io/ | フィールド単位の疑似値。`Faker.seed` で spec と同期 |
| lifelike-synthetic-data-generator | https://github.com/jovd83/lifelike-synthetic-data-generator | config + CLI。seed・locale・分布。大規模生成はコンテキスト外 |

併用の選定・接続手順は [companion-tools.md](companion-tools.md)。API 詳細は `implement-with-practices` で repo-local 化する。

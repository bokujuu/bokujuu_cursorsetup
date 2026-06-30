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

固有スタック名・ツール名は skill 本文では例示に留め、プロジェクト側 spec で上書きする。

# 出典

## 設計源

本スキルは、ユーザー運用の Power Query Workbench（クラウド: [bokujuu/powerquery_refactor](https://github.com/bokujuu/powerquery_refactor)）で使っていた編集方針・コメント方針・Buffer 指針を、特定リポのパス・スクリプト・案件名に依存しない形へ選別・一般化したもの。

採用した核:

- M 編集時の意味保持と `let ... in` 維持
- データ処理配置（早く減らす・遅く飾る・分岐前を重くしない・結合を高コスト扱い）
- notes（コメント）の優先順位
- `Table.Buffer` 等は配置見直し後の再評価抑制手段（キャッシュ保証ではない）

採用しなかった／委譲したもの:

- 特定設定ファイル・絶対パス・作業ブック名
- export / import / validate の COM オーケストレーション
- 案件固有デバッグ手順
- 行数目安やインポート手順のリポ固有運用

## 近接スキルとの境界

- `excel-deliverable-quality` — Excel/CSV **成果物**の品質・レイアウト。M の編集判断は本スキル。ブックを成果物として更新するときは併用を検討する。
- 各リポの workflow / import-guard 等 — ブックへの出し入れと機械的ゲート。本スキルは編集判断のみ。

---
name: excel-deliverable-quality
description: >-
  Excel/スプレッドシート成果物（.xlsx/.xlsm/.csv）を作成・編集・修正・レビューするときに使う、
  ツール非依存の品質基準スキル。数式エラーゼロ、ハードコードでなく数式を使う、数表記・桁・色・
  ソース注記の規約、既存テンプレ書式の踏襲、納品前検証チェックリストを定める。
  「Excelを作って/直して」「集計表/取込用CSVを作って」「数式が壊れていないか確認して」
  「この帳票の品質を見て」などで起動する。実行系は COM Automation（win32com）を第一とし、
  Windows 以外やヘッドレス（Cursor Cloud 等）では openpyxl + LibreOffice 再計算を代替に使う。
  COM の API 手順そのものは `templates/project-rules/excel/excel-com-automation.mdc` を参照し、
  本スキルは成果物の品質規約と検証に責務を限定する。Word/PowerPoint/PDF が主成果物のとき、
  および単なるデータ分析スクリプトが目的のときは起動しない。
---

# excel-deliverable-quality — Excel 成果物の品質規約

Excel/スプレッドシートを「**壊れていない・読める・更新できる**」状態で納品するための、
ツール非依存の品質規約と検証手順。Anthropic の `xlsx` skill が持つ普遍的に有用な部分
（数式エラーゼロ・ハードコード回避・表記規約・ソース注記・検証）を、COM Automation 運用に
合わせて再構成したもの。出典と方針は [references/sources.md](references/sources.md)。

## 役割分担（重複を作らない）

- **本スキル**: 成果物そのものの品質規約（何を満たせば納品可か）と納品前検証。
- **`excel-com-automation.mdc`**（プロジェクト rule・雛形は `templates/project-rules/excel/`）:
  win32com の初期化・プロパティ・クリーンアップ等、**API 操作の手順**。
- **`vba-coding-policy.mdc`**: VBA コーディング規約。
- 実装手順は上記を参照し、本スキルでは再掲しない。

## いつ使うか

- Excel/CSV を新規作成・編集・修正・変換するとき（取込用ファイル生成を含む）。
- 既存帳票・モデルの数式や書式の品質をレビューするとき。
- 「数式が壊れていないか」「#REF! が出ていないか」を確認するとき。

主成果物が Word/PowerPoint/PDF のとき、または目的が単なるデータ分析・可視化スクリプトの
ときは起動しない。

## 絶対要件（すべての Excel 成果物）

1. **数式エラーゼロ** — `#REF! #DIV/0! #VALUE! #N/A #NAME? #NULL! #NUM!` を残さない。
   納品前に必ず全シート全セルを走査して確認する（[検証](#納品前検証)）。
2. **計算は数式で持つ** — Python 側で計算した確定値をセルに直接書き込まない。
   合計・比率・差分などは Excel 数式（`=SUM(...)` 等）として埋め、元データ変更で再計算できる
   状態を保つ。確定値の貼り付けが要件のときだけ例外とし、その旨を明示する。
3. **既存テンプレの書式を踏襲** — 既存ファイルを更新するときは、その配色・桁・フォント・
   命名規約を**そのまま**踏襲する。既存の規約は本スキルの既定値より優先する。
4. **一貫したフォント** — 1 つの成果物内でフォントを混在させない。

詳細な表記規約（数値書式・桁区切り・年・通貨・パーセント・負数・色分け・ハードコード注記）は
[references/quality-standards.md](references/quality-standards.md) を読む。

## 実行系の選択

| 環境 | 第一選択 | 理由 |
|------|----------|------|
| Windows + Excel | **COM Automation（win32com）** | 数式再計算・書式・保護・VBA Import など Excel 固有処理に強い。ユーザー運用の標準。 |
| Windows 以外 / ヘッドレス（Cursor Cloud 等） | **openpyxl + LibreOffice 再計算** | COM 不可。openpyxl で生成し、LibreOffice ヘッドレスで再計算してエラー走査。 |
| 1000 行以上のデータ加工 | pandas（その後 COM/LibreOffice で再計算） | 大量データはセル単位 API より配列処理が速い。 |

各経路の具体手順・再計算・エラー走査は [references/com-and-fallback.md](references/com-and-fallback.md)。

## 納品前検証

成果物を返す前に必ず実施する。

1. 全シート全セルを走査し、エラー値（上記 7 種）が 0 件であることを確認する。
2. 代表セル 2–3 件で、数式が意図した参照を引いているかをサンプル確認する。
3. 既存テンプレ更新時は、配色・桁・フォントが元の規約と一致しているかを確認する。
4. ハードコード値には出典注記（[quality-standards.md](references/quality-standards.md) の形式）が
   付いているかを確認する。

検証コードのひな形（COM / openpyxl+LibreOffice 両対応）は
[references/com-and-fallback.md](references/com-and-fallback.md) を参照する。

## メモ

運用で得た知見は [references/skill-memory.md](references/skill-memory.md) に 1 行ずつ追記する。

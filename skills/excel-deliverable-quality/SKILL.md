---
name: excel-deliverable-quality
description: >-
  Excel/スプレッドシート成果物（.xlsx/.xlsm/.csv）を作成・編集・修正・レビューするときに使う、
  COM Automation 第一の品質・レイアウト規約スキル。スクリプトでビルドし .xlsm は手編集しない、
  数式エラーゼロ、確定値でなく数式、VBA は Core+Silent で自動テストを止めない、安全ビルド（temp→検証→置換）、
  納品前の全件検証を定める。加えて場面依存（必須でない）の指針として、人間が入力する成果物では役割を
  色で区別する（特定カラーコードは固定しない）・配布帳票では印刷規律を採る・内部データの very hidden 隔離。
  「Excelを作って/直して」「帳票/集計表/取込用CSVを作って」「数式が壊れて
  いないか確認して」「この帳票の見た目/色/レイアウトを整えて」「COMビルドを検証して」などで起動する。
  Word/PowerPoint/PDF が主成果物のとき、および単なるデータ分析スクリプトが目的のときは起動しない。
---

# excel-deliverable-quality — Excel 成果物の品質・レイアウト規約

Excel/スプレッドシートを「**壊れていない・見て分かる・更新できる**」状態で納品するための、
COM Automation 第一の実務規約。`utf_ken_all` / `htmlPCAFmock`（COM でビルドする運用 Excel）で確立した
運用を、特定業務に依存しない形へ一般化した。出典は [references/sources.md](references/sources.md)。

## このスキルの柱

1. **作り方（常に）** — スクリプトで生成し `.xlsm` は手編集しない（[references/build-and-verify.md](references/build-and-verify.md)）。
2. **中身（常に）** — 数式エラーゼロ・確定値でなく数式・出典注記（[references/quality-standards.md](references/quality-standards.md)）。
3. **見た目（場面で）** — 配置・配色・印刷は**ケースによる**。特に**人間が入力する成果物**では役割を色で
   区別すると効く（ただし**カラーコードは固定しない**）。既定例は [references/design-and-layout.md](references/design-and-layout.md)。

## 役割分担（重複を作らない）

- **本スキル**: 成果物そのものの規約（何を満たせば納品可か）と納品前検証。
- **`excel-com-automation.mdc`**（対象リポの `.cursor/rules/`・雛形は `templates/project-rules/excel/`）:
  win32com の初期化・プロパティ・クリーンアップ等、**API 操作の手順**。
- **`vba-coding-policy.mdc`**: VBA コーディング規約。
- API・VBA の実装手順は上記を参照し、本スキルでは再掲しない。

## いつ使うか

- Excel/CSV を新規作成・編集・修正・変換するとき（帳票・集計表・取込用ファイル生成を含む）。
- 既存帳票・モデルの数式・**レイアウト・配色**の品質をレビュー／整備するとき。
- 「数式が壊れていないか」「#REF! が出ていないか」を確認するとき。
- COM ビルドを検証して納品可否を判断するとき。

主成果物が Word/PowerPoint/PDF のとき、または目的が単なるデータ分析・可視化スクリプトのときは
起動しない。

## 成果物に適用する要件

CSVにはブック用の数式・書式・再計算規約を適用しない。利用環境に適した操作ツールと既存の生成手順を使う。

1. **スクリプトでビルドする** — `.xlsm` を直接手編集しない。VBA・リボン・ビルド定数を直して
   再ビルドする。既存ビルドがないブックはVBA等を保持できるツールで扱い、必要な読取りや小さな修正を禁止しない。
2. **数式エラーゼロ** — `#REF! #DIV/0! #VALUE! #N/A #NAME? #NULL! #NUM!` を残さない。納品前に
   全シートの使用範囲・数式セルを走査して 0 件を確認する（[build-and-verify.md](references/build-and-verify.md) §4）。
3. **計算は数式で持つ** — Python 側で計算した確定値をセルに直接書き込まない。合計・比率・差分は
   Excel 数式として埋め、元データ変更で再計算できる状態を保つ。確定値貼付が要件のときだけ例外と
   し、その旨を明示する。
4. **既存テンプレを踏襲** — 既存ファイル更新時は配色・桁・フォント・命名・シート構成をそのまま
   踏襲する。既存規約は本スキルの既定値より優先する。
5. **一貫したフォント** — 1 つの成果物内でフォントを混在させない。

## 場面で適用する規約（必須ではない・ケースによる）

成果物の用途によって採否を判断する。下記は**思想と既定例**であって、固定の規定ではない。

- **役割を色で区別する（人間が入力する成果物では極めて重要）** — 利用者が手入力するステップが
  ある帳票・申請書では、「触る／触らない（入力 / 自動計算 / 無効）」をセルの色で区別すると誤入力を
  大きく減らせる。**この思想は重要だが、特定のカラーコードに確定する必要はない**。読みやすく区別
  できれば配色は自由（既定例: 入力＝薄い黄・自動計算＝薄い灰・無効＝灰）。動的に役割が変わるセルは
  条件付き書式で切り替える。一覧出力・取込用データなど人手入力のない成果物では不要。
- **印刷で完結させる** — 印刷・配布が前提の帳票でのみ採用する。印刷範囲の明示・`FitToPages` での
  1 枚化・向き/余白の固定など。画面操作のみ・データ受け渡しが目的の成果物には適用しない。

詳細・既定例は配置・配色 → [references/design-and-layout.md](references/design-and-layout.md)、
表記・数式 → [references/quality-standards.md](references/quality-standards.md)。

## 実行系の選択

| 環境 | 第一選択 | 理由 |
|------|----------|------|
| Windows + Excel | **COM Automation（win32com）** | 数式再計算・書式・保護・VBA Import・リボン注入に強い。運用の標準。 |
| Windows 以外 / ヘッドレス（Cursor Cloud 等） | **openpyxl + LibreOffice 再計算** | COM 不可。規約自体はツール非依存で、同じ基準を満たす。 |
| 1000 行以上のデータ加工 | pandas（その後 COM/LibreOffice で再計算） | 大量データは配列処理が速い。 |

各経路の手順・安全ビルド（temp→検証→置換）・VBA の Core+Silent・エラー走査は
[references/build-and-verify.md](references/build-and-verify.md)。

## 納品前検証（完了宣言の前に必ず）

1. 全シートの使用範囲・数式セルを走査し、エラー値（上記 7 種）が 0 件であることを確認する。
2. 代表セル 2–3 件で、数式が意図した参照を引いているかをサンプル確認する。
3. **桁・日付/率の書式・フォント**が規約（既存テンプレ）と一致するか。配置・配色・印刷を採った成果物
   では、役割の色分け・印刷範囲も既存規約と一致するか（採用していなければスキップ）。
4. ハードコード値に出典注記が付いているか（[quality-standards.md](references/quality-standards.md) の形式）。
5. シナリオは全件完走し、終了コードで集約失敗を返す。ログは `[SUMMARY]` / `[FAIL]` 要約行を優先。

検証コードのひな形（COM / openpyxl+LibreOffice 両対応）は
[references/build-and-verify.md](references/build-and-verify.md) を参照する。

## メモ

運用で得た知見は [references/skill-memory.md](references/skill-memory.md) に 1 行ずつ追記する。

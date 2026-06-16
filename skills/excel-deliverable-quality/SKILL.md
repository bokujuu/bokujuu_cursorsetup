---
name: excel-deliverable-quality
description: >-
  Excel/スプレッドシート成果物（.xlsx/.xlsm/.csv）を作成・編集・修正・レビューするときに使う、
  COM Automation 第一の品質・レイアウト・配色規約スキル。スクリプトでビルドし .xlsm は手編集しない、
  数式エラーゼロ、確定値でなく数式、入力＝黄/計算＝灰のセル役割配色、印刷範囲・1枚化の印刷規律、
  内部データの very hidden 隔離、VBA は Core+Silent で自動テストを止めない、安全ビルド（temp→検証→置換）、
  納品前の全件検証を定める。「Excelを作って/直して」「帳票/集計表/取込用CSVを作って」「数式が壊れて
  いないか確認して」「この帳票の見た目/色/レイアウトを整えて」「COMビルドを検証して」などで起動する。
  Word/PowerPoint/PDF が主成果物のとき、および単なるデータ分析スクリプトが目的のときは起動しない。
---

# excel-deliverable-quality — Excel 成果物の品質・レイアウト・配色規約

Excel/スプレッドシートを「**壊れていない・見て分かる・そのまま印刷できる・更新できる**」状態で
納品するための、COM Automation 第一の実務規約。`utf_ken_all` / `htmlPCAFmock`（COM でビルドする運用
Excel）で確立した運用を、特定業務に依存しない形へ一般化した。出典は [references/sources.md](references/sources.md)。

## このスキルの 3 本柱

1. **作り方** — スクリプトで生成し `.xlsm` は手編集しない（[references/build-and-verify.md](references/build-and-verify.md)）。
2. **見た目** — セルの役割を色で示し、印刷で完結させる（[references/design-and-layout.md](references/design-and-layout.md)）。
3. **中身** — 数式エラーゼロ・確定値でなく数式・出典注記（[references/quality-standards.md](references/quality-standards.md)）。

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

## 絶対要件（すべての Excel 成果物）

1. **スクリプトでビルドする** — `.xlsm` を直接手編集しない。VBA・リボン・ビルド定数を直して
   再ビルドする。`.xlsm` を Read しない。都度 win32com ワンオフを書かない。
2. **数式エラーゼロ** — `#REF! #DIV/0! #VALUE! #N/A #NAME? #NULL! #NUM!` を残さない。納品前に
   全シート全セルを走査して 0 件を確認する（[build-and-verify.md](references/build-and-verify.md) §4）。
3. **計算は数式で持つ** — Python 側で計算した確定値をセルに直接書き込まない。合計・比率・差分は
   Excel 数式として埋め、元データ変更で再計算できる状態を保つ。確定値貼付が要件のときだけ例外と
   し、その旨を明示する。
4. **役割を色で示す** — 入力＝薄い黄 `(255,255,204)`・数式/自動計算＝薄い灰 `(242,242,242)`・無効＝
   灰 `(220,220,220)`。意味の数＝色の数。動的に変わるセルは条件付き書式で切り替える。
5. **印刷で完結させる** — 印刷範囲を明示し、集計・メタ・内部欄は印刷範囲外。`FitToPages` で 1 枚に
   収め、向き・余白を固定する。
6. **既存テンプレを踏襲** — 既存ファイル更新時は配色・桁・フォント・命名・シート構成をそのまま
   踏襲する。既存規約は本スキルの既定値より優先する。
7. **一貫したフォント** — 1 つの成果物内でフォントを混在させない。

詳細は配置・配色 → [references/design-and-layout.md](references/design-and-layout.md)、
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

1. 全シート全セルを走査し、エラー値（上記 7 種）が 0 件であることを確認する。
2. 代表セル 2–3 件で、数式が意図した参照を引いているかをサンプル確認する。
3. **配置・配色** — 役割色・桁・日付/率の書式・フォント・印刷範囲が規約（既存テンプレ）と一致するか。
4. ハードコード値に出典注記が付いているか（[quality-standards.md](references/quality-standards.md) の形式）。
5. シナリオは全件完走し、終了コードで集約失敗を返す。ログは `[SUMMARY]` / `[FAIL]` 要約行を優先。

検証コードのひな形（COM / openpyxl+LibreOffice 両対応）は
[references/build-and-verify.md](references/build-and-verify.md) を参照する。

## メモ

運用で得た知見は [references/skill-memory.md](references/skill-memory.md) に 1 行ずつ追記する。

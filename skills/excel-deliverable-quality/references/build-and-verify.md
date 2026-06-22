# ビルドと検証（COM 第一・スクリプト生成）

成果物の品質規約は [quality-standards.md](quality-standards.md)、配置・配色は
[design-and-layout.md](design-and-layout.md)。本書は **どう作って・どう検証するか** の手順。
COM の API 詳細（初期化・プロパティ・クリーンアップ）は対象リポの
`templates/project-rules/excel/excel-com-automation.mdc` を正とし、ここでは再掲しない。

## 0. 原則 —「スクリプトで生成し、`.xlsm` は手で触らない」

`htmlPCAFmock` 等の運用で確立した中核方針。再現性とレビュー性のために、成果物は**常にコードから
ビルド**する。

- **`.xlsm` / `.xlsx` を直接手編集しない**。VBA・リボン XML・ビルドスクリプト（座標／数式／色の定数）
  を直し、**再ビルド**する。成果物は再ビルドで上書きされる前提で扱う。
- **`.xlsm` を Read しない**（バイナリ・zip 断片でコンテキストを浪費する）。仕様は SoT ドキュメントと
  ビルドスクリプトを読む。
- **都度 win32com のワンオフを書かない**。既存のビルド／検証スクリプトを修正して実行する。
- **座標・定数を1か所に集約**する（ビルドスクリプトの定数。VBA と共有する値は両方を同期）。

## 1. 経路の選択

- **Windows + Excel**: COM Automation（win32com）が第一選択。数式再計算・書式・保護・VBA Import・
  リボン注入など Excel 固有処理に強く、運用の標準。
- **Windows 以外 / ヘッドレス（Cursor Cloud 等）**: COM 不可。openpyxl で生成 → LibreOffice ヘッドレス
  で再計算 → エラー走査、という**代替**を使う（[5](#5-ヘッドレス代替openpyxl--libreoffice)）。配置・配色・
  品質の**規約自体はツール非依存**で、どちらの経路でも同じ基準を満たす。
- **大量データ（1000 行以上）**: pandas で加工し、確定値が要る箇所だけ後段で再計算する。

## 2. 安全ビルド（temp → 検証 → 置換）

既存の配布物を壊さないため、**いったん `temp/` の作業ファイルに保存 → COM 検証 → 成功時のみ本番へ
置換**する。検証に落ちたら既存ファイルを残す。

```python
# 概念フロー（実装は build スクリプト側）
staging = TEMP / "out.new.xlsm"
wb.SaveAs(str(staging), FileFormat=52)     # 52 = xlOpenXMLWorkbookMacroEnabled
inject_custom_ui(staging, ribbon_xml)      # リボンは zip 注入
if not run_verify(staging):                # COM 検証
    staging.unlink(missing_ok=True)
    raise RuntimeError("verify failed; 既存ブックを保持")
os.replace(staging, target)                # 成功時のみ本番へ
```

- 保存前に **`excel.CalculateFullRebuild()`** で全再計算してから保存する。
- リボンは **imageMso（Office 組込みアイコン）のみ**にすると `getImage` コールバックや PNG 同梱が
  不要になり、注入が単純になる。
- **`.xlam` アドイン**で zip 注入後にリボンが出ない場合は、注入直後に Excel COM で `Open → Save` して
  パッケージを正規化する（詳細はグローバル skill `excel-xlam-ribbon-build`）。

## 3. VBA は「Core + Silent」パターン（自動テストを止めない）

COM 自動テストはモーダル UI で停止する。`MsgBox` / `InputBox` / `GetSaveAsFilename` / Outlook の
`Display` を**COM から呼ぶ経路に置かない**。

- ロジックは `Private *Core` に集約する。
- COM から呼ぶ入口は `Public Function *Silent As String`（空文字＝成功・エラーは戻り値で返す）。
- `MsgBox` / `InputBox` / ファイルダイアログは**手動 Sub・リボン用 Sub にだけ**置く。
- `Application.Run` で呼ぶ名は **ASCII**（日本語 Sub 名は文字化けしうる）。
- VBA ソースは **`*.bas`（UTF-8）で版管理**し、ビルド時に cp932 へ変換して `VBComponents.Import`。
- `DisplayAlerts=False` だけでは VBA の `MsgBox` は抑止できない点に注意。

## 4. 検証（完了宣言の前に必ず）

成果物を返す前に、全件チェックを自動で回す。

1. **数式エラー走査** — 全シート全セルを走査し、`#REF! #DIV/0! #VALUE! #N/A #NAME? #NULL! #NUM!`
   が 0 件であることを確認する（コードは下記）。
2. **代表セルのサンプル確認** — 合計・比率など 2〜3 件で、数式が意図した参照を引いているか。
3. **書式・（採用していれば）配置・配色の一致** — 既存テンプレ更新時は桁・フォントが元の規約と一致
   するか。色分け・印刷範囲を採っている成果物では、それらも元の規約と一致するか（任意項目）。
4. **シナリオは全件完走** — 1 件失敗でも残りを実行し、**終了コードで集約失敗**を返す。途中例外で
   止めない。ログは `[SUMMARY]` / `[FAIL]` の要約行を優先し、全ログを会話に貼らない。

```python
# COM: 全シート全セルのエラー走査（配列一括・セル単位ループ禁止）
ERRORS = ("#REF!", "#DIV/0!", "#VALUE!", "#N/A", "#NAME?", "#NULL!", "#NUM!")
bad = []
for ws in wb.Worksheets:
    used = ws.UsedRange
    vals = used.Value
    if vals is None:
        continue
    rows = vals if isinstance(vals, tuple) else ((vals,),)
    for r, row in enumerate(rows, start=used.Row):
        cells = row if isinstance(row, tuple) else (row,)
        for c, v in enumerate(cells, start=used.Column):
            if isinstance(v, str) and v in ERRORS:
                bad.append((ws.Name, r, c, v))
assert not bad, f"数式エラー: {bad}"
```

### COM の後始末（プロセス残留対策）

- ビルド／検証は **セッションの Excel PID を登録**し、終了時に確実に `Quit` する。
- 残留時の強制終了は**登録した PID のみ**を対象にする。**`taskkill /IM excel.exe` 等で全 Excel を
  落とさない**（利用者の他ブックを巻き込む）。

## 5. ヘッドレス代替（openpyxl + LibreOffice）

Windows・Excel が無い環境（Cursor Cloud 等）で**規約どおりの成果物を作り、検証する**ための代替。

```python
# 生成（openpyxl）— 確定値でなく数式で持つ
from openpyxl import Workbook
wb = Workbook(); ws = wb.active
ws["A1"] = 10; ws["A2"] = 20
ws["A3"] = "=SUM(A1:A2)"
wb.save("out.xlsx")
```

openpyxl は数式を文字列保持するだけで**計算しない**。確定値が要るなら LibreOffice で再計算する。

```bash
soffice --headless --calc \
  --convert-to "xlsx:Calc MS Excel 2007 XML" \
  --outdir recalc/ out.xlsx
```

```python
# エラー走査（再計算後を data_only で読む。data_only で開いたまま保存しない）
from openpyxl import load_workbook
ERRORS = {"#REF!", "#DIV/0!", "#VALUE!", "#N/A", "#NAME?", "#NULL!", "#NUM!"}
wb = load_workbook("recalc/out.xlsx", data_only=True)
bad = [(ws.title, c.coordinate, c.value)
       for ws in wb.worksheets for row in ws.iter_rows() for c in row
       if isinstance(c.value, str) and c.value in ERRORS]
assert not bad, f"数式エラー: {bad}"
print("OK: 数式エラー 0 件")
```

（LibreOffice 24.2 で、openpyxl が確定値を持たない `=SUM` / `=A4/B1` を上記往復で再計算できることを
確認済み。）再計算をかけられない環境では、最低限**数式文字列を静的に点検**する（参照・分母・関数名）。

## 6. 大量データ（pandas）

- 1000 行以上は pandas で加工・集計し、確定値が要る箇所だけ後段で再計算する。
- 取込用 CSV は文字コード（UTF-8 / BOM 有無）と改行を**取込先の仕様に合わせる**。
- ID 等のゼロ落ち防止に `dtype=str` を指定する（`pd.read_excel(..., dtype={"id": str})`）。

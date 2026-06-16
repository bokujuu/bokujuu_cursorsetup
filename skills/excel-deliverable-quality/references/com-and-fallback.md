# 実行系: COM 第一・openpyxl/LibreOffice 代替

成果物の品質規約は [quality-standards.md](quality-standards.md)。本書は「どう作って・どう検証するか」の
実行手順。COM の API 詳細（初期化・クリーンアップ等）は
`templates/project-rules/excel/excel-com-automation.mdc` を正とし、ここでは再掲しない。

## 経路の選択

- **Windows + Excel**: COM Automation（win32com）。数式再計算・書式・保護・VBA Import に強い。
- **Windows 以外 / ヘッドレス（Cursor Cloud 等）**: openpyxl で生成し、LibreOffice ヘッドレスで
  再計算してからエラー走査。COM は使えない。
- **1000 行以上のデータ加工**: pandas で加工 → 確定値が要るなら COM / LibreOffice で再計算。

## COM 経路（Windows・第一選択）

API 操作は `excel-com-automation.mdc` に従う。品質観点で必須なのは次の 2 点。

1. **保存前に再計算**して確定値を反映する。

   ```python
   excel_app.CalculateFullRebuild()   # 全再計算
   wb.Save()
   ```

2. **全シート全セルのエラー走査**。`Range.Value` を配列一括で取得し、`-2146826281`
   などのエラー定数ではなく、まず文字列表現で `#` 始まりのエラーを拾うのが簡単。

   ```python
   import win32com.client as win32
   ERRORS = ("#REF!", "#DIV/0!", "#VALUE!", "#N/A", "#NAME?", "#NULL!", "#NUM!")
   bad = []
   for ws in wb.Worksheets:
       used = ws.UsedRange
       vals = used.Value  # タプルのタプル（配列一括・セル単位ループ禁止）
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

## openpyxl + LibreOffice 経路（ヘッドレス・代替）

### 1. 生成（openpyxl）

```python
from openpyxl import Workbook
wb = Workbook()
ws = wb.active
ws["A1"] = 10
ws["A2"] = 20
ws["A3"] = "=SUM(A1:A2)"   # 確定値でなく数式で持つ
wb.save("out.xlsx")
```

openpyxl は数式を文字列として保持するだけで**計算しない**。確定値が必要なら次の再計算を行う。

### 2. 再計算（LibreOffice ヘッドレス）

LibreOffice は読み込み時に数式を再計算できる。最も単純な方法は変換での往復（フィルタを
明示すると確実）:

```bash
soffice --headless --calc \
  --convert-to "xlsx:Calc MS Excel 2007 XML" \
  --outdir recalc/ out.xlsx
```

（検証環境 LibreOffice 24.2 で、openpyxl が確定値を持たない `=SUM`/`=A4/B1` を上記往復で
600/150 に再計算できることを確認済み。）
それでも自動再計算が効かない場合は、Basic マクロ（`ThisComponent.calculateAll()`）で明示的に
再計算するか、`Tools > Options > Calc > Formula` 相当の `ooxmlRecalcMode` を「常に再計算」に
設定する。

### 3. エラー走査（openpyxl・確定値読み）

再計算後のファイルを `data_only=True` で開き、確定値からエラーを拾う。
（`data_only=True` で開いたまま保存すると数式が失われるので、走査専用で開く。）

```python
from openpyxl import load_workbook
ERRORS = {"#REF!", "#DIV/0!", "#VALUE!", "#N/A", "#NAME?", "#NULL!", "#NUM!"}
wb = load_workbook("recalc/out.xlsx", data_only=True)
bad = [
    (ws.title, cell.coordinate, cell.value)
    for ws in wb.worksheets
    for row in ws.iter_rows()
    for cell in row
    if isinstance(cell.value, str) and cell.value in ERRORS
]
assert not bad, f"数式エラー: {bad}"
print("OK: 数式エラー 0 件")
```

再計算をかけられない環境では、少なくとも**数式文字列を静的に点検**する
（`data_only=False` で開き、`=` 始まりセルの参照・分母・関数名を目視/正規表現で確認）。
確定値の検証は COM か LibreOffice を使える環境で行う。

## 大量データ（pandas）

- 1000 行以上は `pandas` で加工・集計し、確定値が要る箇所だけ後段で再計算する。
- 取込用 CSV は文字コード（UTF-8 / BOM 有無）と改行を取込先仕様に合わせる。
- ID 等のゼロ落ち防止に `dtype=str` を指定する（`pd.read_excel(..., dtype={"id": str})`）。

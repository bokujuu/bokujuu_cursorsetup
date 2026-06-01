---
name: COM Automationスクリプト作成時の注意事項
version: 1.1.0
description: Python(win32com)でExcelを操作する際の注意事項。COM vs Pandas/NumPyの使い分け（1000行以上）を追記。
appliesTo: python
---

# COM Automationスクリプト作成時の注意事項

このドキュメントは、Pythonの`win32com`を使用してExcelを操作するCOM Automationスクリプトを作成する際に注意すべき点をまとめています。

**セクション一覧**: 0. 使い分け / 0.1 並列 / 0.2 パフォーマンス / 1. 初期化 / 2. プロパティ / 3. クリーンアップ / 4. エンコーディング（COM特化） / 5. パス / 6. エラーハンドリング / 実装時の課題と解決策

## 0. 使い分け（COM Automation vs Pandas/NumPy）

### 原則
- **COM Automation**は「Excel固有の構造/設定/Refresh等」に限定して使います。
- **データの読み込み/加工/検証/集計**は原則として **Pandas/NumPy（必要に応じてopenpyxl）** で行います。

### 目安（低性能PC前提）
- **1000行以上**のデータ処理: Pandas優先（Excelを起動しない運用を検討）
- ピボット/接続/Refresh/保護/書式/アドイン: COM優先

### ハイブリッド（推奨）
1) COMでRefreshや設定変更 → 保存 
2) Pandasで値の検証・差分検出・集計 → 出力（`xlsx`/`csv`）

### 注意（openpyxl/pandasの読み取り）
- 数式の計算結果は「最後に保存された値」を読む挙動になり得ます。Refresh/再計算が必要な場合は、先にCOMで更新→保存してからPandas等で読む運用にします。

## 0.1 並列処理の注意（重要）

- **原則**: ThreadPool等の"同一プロセス内の並列"は避けます（Excel COMは基本STA前提で不安定化しやすい）。
- **並列が必要な場合**: 「プロセス分離 + 1プロセス1 Excel」を検討します（PC負荷/安定性/運用要件の確認が前提）。

## 0.2 COM側パフォーマンス原則

- **禁止**: セル1つずつの読み書き（ループで `Cells(i,j)` を回す）
- **推奨**: `Range.Value` をまとめて配列で取得→Python側で処理→まとめて書き戻す
- **推奨**: 設定は`try/finally`で必ず戻す（例: `DisplayAlerts/ScreenUpdating/EnableEvents/Calculation`）

## 1. Excelアプリケーションの初期化

### Dispatch vs DispatchExの使い分け

`win32com.client.Dispatch`と`win32com.client.DispatchEx`には重要な違いがあります：

- **`Dispatch`**: 既存のExcelインスタンスがあればそれを使用し、なければ新規に起動します
- **`DispatchEx`**: 常に新しいExcelインスタンスを起動します（推奨）

**推奨実装**：

```python
import win32com.client

# DispatchExを使用して新規インスタンスを起動（推奨）
try:
 excel_app = win32com.client.DispatchEx("Excel.Application")
 print("Excelアプリケーションを起動しました（DispatchEx使用）")
except Exception as e:
 # フォールバック: 通常のDispatchを使用
 print(f"警告: DispatchExでの起動に失敗、通常のDispatchを使用します: {e}")
 excel_app = win32com.client.Dispatch("Excel.Application")
 print("Excelアプリケーションを起動しました（通常Dispatch）")
```

**理由**：
- 既存のExcelインスタンスを使用すると、予期しない動作やリソースの競合が発生する可能性があります
- 新規インスタンスを起動することで、スクリプトの動作が安定します

### その他の初期化
- **gencache.EnsureDispatch**: タイプライブラリ事前生成でパフォーマンス向上の可能性あり。初回は時間がかかる。「This COM object can not automate the makepy process」の場合は通常の `Dispatch` を使用。必要時は公式ドキュメントを参照。
- **既存インスタンス取得**: `GetActiveObject("Excel.Application")` で取得可能。状態に依存するため、通常は新規 `DispatchEx` を推奨。必要時は公式ドキュメントを参照。

## 2. プロパティ設定のエラーハンドリング

Visible / DisplayAlerts / ScreenUpdating 等は、COM の初期化方法や Excel バージョンにより設定できない場合がある。**すべて try-except で囲む**。同様に setattr でループし、AttributeError は pass する。

```python
properties = {'Visible': False, 'DisplayAlerts': False, 'ScreenUpdating': False}
for prop_name, prop_value in properties.items():
    try: setattr(excel_app, prop_name, prop_value)
    except AttributeError: pass
```

## 3. COMオブジェクトのクリーンアップ

### Quitメソッドの呼び出し方法

Excelアプリケーションを終了する際は、必ず`Quit`メソッドを呼び出してください：

```python
finally:
 # Excelアプリケーションを終了
 if excel_app:
 try:
 excel_app.Quit()
 except AttributeError:
 pass # Quitメソッドが呼び出せない場合は無視
 except Exception as e:
 print(f"警告: Excelアプリケーションの終了中にエラー: {e}")
 finally:
 excel_app = None
```

**理由**：
- `Quit`メソッドを呼び出さないと、Excelプロセスが残り続ける可能性があります
- リソースリークを防ぐため、必ずクリーンアップ処理を実装してください

### エラー時の安全な終了処理

エラーが発生した場合でも、必ずクリーンアップ処理を実行してください：

```python
try:
 # Excel操作の処理
 workbook = excel_app.Workbooks.Open(file_path)
 # ... 処理 ...
 workbook.Close(SaveChanges=False)
except Exception as e:
 print(f"エラー: {e}")
finally:
 # 必ずクリーンアップ処理を実行
 if excel_app:
 try:
 excel_app.Quit()
 except:
 pass
 finally:
 excel_app = None
```

### リソースリークの防止

以下の点に注意してください：

1. **ワークブックのクローズ**: 開いたワークブックは必ず閉じる
2. **Excelアプリケーションの終了**: 処理完了後は必ず`Quit`を呼び出す
3. **例外処理**: try-finallyブロックで確実にクリーンアップを実行

```python
workbook = None
try:
 workbook = excel_app.Workbooks.Open(file_path)
 # ... 処理 ...
finally:
 if workbook:
 try:
 workbook.Close(SaveChanges=False)
 except:
 pass
```

## 4. エンコーディング（COM 特化）

Python のエンコーディング（ファイル `open` の `encoding`、PYTHONUTF8 等）は [user-rule-python-coding-policy.md](user-rule-python-coding-policy.md) を参照。**COM 特化として以下を追加**。

- **コンソール**: Windows は cp932 のため、Unicode 文字（例: ✓）は `UnicodeEncodeError` になりやすい。**ASCII のみ使用**（例: `[OK]`）。
- **ファイル出力**: CSV/ログ等は `encoding='utf-8-sig'` を指定する。

```python
print(" [OK] 処理完了")  # ✓ は使わない
with open(log_file, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
```

## 5. ファイルパスの扱い

### 絶対パスへの変換（resolve()）

相対パスを絶対パスに変換することで、パスの問題を回避できます：

```python
from pathlib import Path

# 絶対パスに変換
file_path = Path("relative/path/to/file.xlsx")
absolute_path = str(file_path.resolve())

# Excelで開く
workbook = excel_app.Workbooks.Open(absolute_path)
```

**理由**：
- ネットワークドライブやUNCパスでも正しく動作します
- カレントディレクトリの変更による影響を受けません

### ネットワークパスの扱い

ネットワークドライブ上のファイルも処理可能ですが、以下の点に注意してください：

```python
# ネットワークパスも正しく処理される
network_path = Path(r"\\192.168.2.45\Share\path\to\file.xlsx")
absolute_path = str(network_path.resolve())

# Excelで開く
workbook = excel_app.Workbooks.Open(absolute_path)
```

**注意**：
- ネットワークドライブへのアクセス権限を確認してください
- ネットワーク接続が不安定な場合、エラーが発生する可能性があります

### パス区切り文字の統一

`pathlib.Path`を使用することで、パス区切り文字の問題を回避できます：

```python
from pathlib import Path

# pathlibを使用（推奨）
base_path = Path("base/path")
file_path = base_path / "subfolder" / "file.xlsx"

# 文字列に変換してExcelで使用
excel_path = str(file_path.resolve())
```

## 6. エラーハンドリングのベストプラクティス

### 詳細なエラーメッセージの出力

エラーが発生した場合、詳細な情報を出力することで、問題の特定が容易になります：

```python
import traceback

try:
 # 処理
 workbook = excel_app.Workbooks.Open(file_path)
except Exception as e:
 error_details = traceback.format_exc()
 print(f"エラー: {file_path} の処理中にエラーが発生しました")
 print(f" エラー内容: {str(e)}")
 print(f" 詳細: {error_details}")
```

### tracebackの活用

`traceback`モジュールを使用することで、スタックトレースを取得できます：

```python
import traceback

try:
 # 処理
 pass
except Exception as e:
 # スタックトレースを取得
 tb_str = traceback.format_exc()
 print(f"エラー詳細:\n{tb_str}")
```

### 処理継続 vs 中断の判断

エラーが発生した場合、処理を継続するか中断するかを判断する必要があります：

```python
# 処理を継続する場合（推奨）
for file in files:
 try:
 process_file(file)
 except Exception as e:
 print(f"警告: {file} の処理中にエラー: {e}")
 continue # 次のファイルの処理を継続

# 処理を中断する場合
try:
 process_file(file)
except Exception as e:
 print(f"エラー: {file} の処理中にエラー: {e}")
 raise # エラーを再発生させて処理を中断
```

**推奨**：
- 複数ファイルを処理する場合は、1つのファイルでエラーが発生しても他のファイルの処理を継続する
- 致命的なエラー（Excelの起動失敗など）の場合は、処理を中断する

## 実装時の課題と解決策

| 課題 | 解決策（1行） |
|------|----------------|
| Workbooks にアクセスできない（AttributeError） | `DispatchEx` で新規インスタンスを起動する |
| Visible / DisplayAlerts 等が設定できない | try-except で AttributeError を pass する（セクション2参照） |
| Quit が呼び出せない | try-except で AttributeError を pass する。finally で確実に呼ぶ |
| UnicodeEncodeError（コンソール cp932） | コンソール出力は ASCII のみ（例: `[OK]`）。セクション4参照 |

## まとめ

COM Automationスクリプトを作成する際は、以下の点に注意してください：

1. **Excelアプリケーションの初期化**: `DispatchEx`を使用して新規インスタンスを起動
2. **プロパティ設定**: try-exceptでエラーを捕捉して無視
3. **クリーンアップ**: 必ず`Quit`メソッドを呼び出してリソースを解放
4. **エンコーディング**: Unicode文字を避け、ASCII文字のみを使用
5. **ファイルパス**: `pathlib.Path`を使用して絶対パスに変換
6. **エラーハンドリング**: 詳細なエラーメッセージを出力し、処理を継続可能にする

これらの注意事項を守ることで、安定したCOM Automationスクリプトを作成できます。

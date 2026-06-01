---
name: VBAコーディングポリシー
version: 1.0.0
description: VBAマクロ開発におけるパフォーマンス最適化とベストプラクティス
appliesTo: vba
---

# VBAコーディングポリシー

## 目的と適用範囲

- VBAマクロ開発におけるパフォーマンス最適化とコード品質向上を目的とする
- 大量データ処理時の効率化を重視
- Excel操作におけるベストプラクティスを定義

## パフォーマンス最適化ルール

### 1. 配列操作による高速化（必須）

**原則**: 大量データ（100行以上）を処理する場合は、必ず配列操作を使用する

#### 推奨実装

```vba
' 良い例: 配列操作による一括処理
Dim dataArray As Variant
Set sourceRange = ws.Range("A1:F1000")
dataArray = sourceRange.Value ' 配列に一括読み込み

' データ処理（配列内で処理）
' ...

' 配列を一括書き込み
Set targetRange = ws.Range("J1:O1000")
targetRange.Value = dataArray
```

#### 非推奨実装

```vba
' 悪い例: Forループによる個別処理（遅い）
Dim i As Long
For i = 1 To 1000
 ws.Cells(i, "J").Value = ws.Cells(i, "A").Value
 ws.Cells(i, "K").Value = ws.Cells(i, "B").Value
 ' ...
Next i
```

**理由**:
- 配列操作はセルへのアクセス回数を大幅に削減
- 100行以上のデータ処理では、配列操作が10倍以上高速
- 数万行のデータでも数秒で処理可能

### 2. Findメソッドによる高速検索

**原則**: 大量データから特定の値を検索する場合は、Findメソッドを使用する

#### 推奨実装

```vba
' 良い例: Findメソッドによる高速検索
Dim foundCell As Range
Dim searchRange As Range
Set searchRange = ws.Range("P1:P10000")
Set foundCell = searchRange.Find(What:=targetDate, LookIn:=xlValues, LookAt:=xlWhole, MatchCase:=False)

If Not foundCell Is Nothing Then
 ' 見つかった場合の処理
End If
```

#### 非推奨実装

```vba
' 悪い例: Forループによる検索（遅い）
Dim i As Long
Dim found As Boolean
found = False
For i = 1 To 10000
 If ws.Cells(i, "P").Value = targetDate Then
 found = True
 Exit For
 End If
Next i
```

**理由**:
- Findメソッドは内部最適化されており、Forループより高速
- 数万行のデータでも瞬時に検索可能

### 3. 値のみの貼り付け（書式をコピーしない）

**原則**: データコピー時は、値のみを貼り付け、書式はコピーしない

#### 推奨実装

```vba
' 良い例: 配列操作による値のみの貼り付け
Dim sourceData As Variant
sourceData = ws.Range("A1:F100").Value
ws.Range("J1:O100").Value = sourceData
```

#### 非推奨実装

```vba
' 悪い例: Range.Copyによる書式込みのコピー（エラーの原因になりやすい）
ws.Range("A1:F100").Copy Destination:=ws.Range("J1:O100")
```

**理由**:
- 書式をコピーしないことで、エラーの原因を排除
- 値のみの貼り付けは配列操作で実現可能
- パフォーマンスも向上

### 4. Range操作の一括処理

**原則**: 複数のセルに同じ値を設定する場合は、範囲指定で一括処理する

#### 推奨実装

```vba
' 良い例: 範囲指定による一括入力
ws.Range("P1:P100").Value = todayDate
```

#### 非推奨実装

```vba
' 悪い例: Forループによる個別入力（遅い）
Dim i As Long
For i = 1 To 100
 ws.Cells(i, "P").Value = todayDate
Next i
```

**理由**:
- 範囲指定による一括処理は、Forループより大幅に高速
- コードも簡潔になる

## パフォーマンス判定基準

### 処理行数による推奨方法

| 処理行数 | 推奨方法 | 理由 |
|---------|---------|------|
| 1-10行 | Forループ可 | オーバーヘッドが小さい |
| 11-99行 | 配列操作推奨 | パフォーマンス向上が期待できる |
| 100行以上 | 配列操作必須 | 大幅なパフォーマンス向上 |

### 検索処理

| 検索対象行数 | 推奨方法 | 理由 |
|------------|---------|------|
| 1-100行 | Forループ可 | オーバーヘッドが小さい |
| 101行以上 | Findメソッド推奨 | 大幅なパフォーマンス向上 |

## コード品質ルール

### 1. エラーハンドリング

- 必ず`On Error GoTo ErrorHandler`を実装
- エラー発生時は詳細な情報を表示
- リソースのクリーンアップを確実に実行

### 2. 変数の型宣言

- 必ず`Option Explicit`を使用
- すべての変数に型を明示的に宣言
- `Variant`型は配列操作時のみ使用

### 3. 定数の使用

- マジックナンバーや文字列リテラルは定数化
- 設定値はファイル先頭で定数として定義

### 4. コメント

- 処理の目的を明確に記述
- 複雑なロジックには説明を追加
- 拡張ポイントを明示

## 実装例

### 完全な実装例

```vba
Sub データ処理サンプル()
 Dim ws As Worksheet
 Dim sourceData As Variant
 Dim targetRange As Range
 Dim sourceRange As Range
 Dim lastRow As Long
 
 On Error GoTo ErrorHandler
 
 Set ws = ThisWorkbook.Worksheets("Sheet1")
 
 ' 最終行を取得
 lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row
 
 ' 配列に一括読み込み（高速化）
 Set sourceRange = ws.Range("A1:F" & lastRow)
 sourceData = sourceRange.Value
 
 ' データ処理（配列内で処理）
 ' ...
 
 ' 配列を一括書き込み（値のみ、書式なし）
 Set targetRange = ws.Range("J1:O" & lastRow)
 targetRange.Value = sourceData
 
 ' 日付列に一括入力
 ws.Range("P1:P" & lastRow).Value = Date
 
 Exit Sub
 
ErrorHandler:
 MsgBox "エラーが発生しました。" & vbCrLf & _
 "エラー番号: " & Err.Number & vbCrLf & _
 "エラー内容: " & Err.Description, vbCritical, "エラー"
End Sub
```

## チェックリスト

コードレビュー時に以下の項目を確認：

- [ ] 100行以上のデータ処理で配列操作を使用しているか
- [ ] Findメソッドによる検索を実装しているか（該当する場合）
- [ ] 値のみの貼り付けを実装しているか（書式をコピーしていないか）
- [ ] 範囲指定による一括処理を活用しているか
- [ ] エラーハンドリングを実装しているか
- [ ] 変数の型宣言が適切か
- [ ] 定数を使用しているか（マジックナンバーがないか）

## 参考資料

- Excel VBA パフォーマンス最適化ガイド
- 配列操作による高速化のベストプラクティス
- Findメソッドの活用方法

## 更新履歴

- 2025/11/28: 初版作成（配列操作、Findメソッド、値のみ貼り付けのルールを追加）

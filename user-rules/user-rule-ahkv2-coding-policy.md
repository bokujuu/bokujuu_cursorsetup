---
name: AHKv2コーディングポリシー
version: 1.0.0
description: AutoHotkey v2開発におけるバージョン混在防止とベストプラクティス
appliesTo: autohotkey
---

# 目的と適用範囲
- AutoHotkey v2（AHKv2）のみを使用したスクリプト開発を保証。v1とv2の混在による不具合を防止

# バージョン指定（必須）
- スクリプト先頭に`#Requires AutoHotkey v2`を必須記載
- v1インタープリターでの誤実行を防止

# 禁止構文（v1特有）
- `=`演算子での変数代入（例: `Var = value`）は禁止
- `%変数%`形式の変数参照は禁止
- 動的変数作成（`%VarName% = value`）は禁止
- `ErrorLevel`によるエラーハンドリングは禁止

# 必須構文（v2）
- 変数代入は必ず`:=`を使用（例: `Var := "value"`）
- 変数参照は直接変数名を使用（例: `MsgBox Var`）
- エラーハンドリングは`try/catch`を使用

# Context7使用時の制約
- Context7から取得するドキュメントは`autohotkey_v2`のみ参照
- v1のドキュメントや構文例を参照しない

# コード生成時のチェックポイント
- `#Requires AutoHotkey v2`ディレクティブが先頭にあるか
- v1特有の構文（`=`, `%変数%`など）が含まれていないか
- v2の新構文（例外処理、関数形式など）を正しく使用しているか

# 構文比較例

## 変数代入
```autohotkey
# 正しい（v2）
Var := "value"
Number := 42

# 禁止（v1）
Var = value
```

## 変数参照
```autohotkey
# 正しい（v2）
MsgBox Var
Result := Var + Number

# 禁止（v1）
MsgBox %Var%
```

## エラーハンドリング
```autohotkey
# 正しい（v2）
try {
 content := FileRead("file.txt", "UTF-8")
} catch as err {
 MsgBox "エラーが発生しました: " err.Message
}

# 禁止（v1）
FileRead, content, file.txt
if ErrorLevel {
 MsgBox エラーが発生しました
}
```

# チェックリスト
- [ ] スクリプト先頭に`#Requires AutoHotkey v2`が記載されているか
- [ ] v1特有の構文（`=`, `%変数%`など）が使用されていないか
- [ ] 変数代入は全て`:=`を使用しているか
- [ ] エラーハンドリングは`try/catch`を使用しているか
- [ ] Context7からはv2のドキュメントのみを参照しているか

# 更新履歴
- 2025/12/08 00:44: 初版作成

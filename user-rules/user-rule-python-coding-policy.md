---
name: Pythonコーディングポリシー
version: 1.0.0
description: Python開発におけるベストプラクティス。コーディングエージェント向けフォルダ構成と日本語エンコーディング対策を含む。
appliesTo: python
---

# 目的と適用範囲
- Python開発における標準的なコーディングポリシーを定義
- コーディングエージェント向けのフォルダ構成と、日本語エンコーディング問題の回避を重視
- Windows環境での動作を考慮（cp932 対策は本セクションおよびコンソール出力の注意で代替。詳細は別途 Cp932.md を用意した場合は参照可）

# プロジェクト構造

## 標準フォルダ構成
```
project_root/
├── README.md
├── LICENSE
├── pyproject.toml # 依存関係とプロジェクト設定（推奨）
├── requirements.txt # 依存関係（pyproject.tomlがない場合）
├── .gitignore
├── src/ # メインソースコード
│ └── project_name/
│ ├── __init__.py
│ └── module1.py
├── tests/ # テストコード
│ ├── __init__.py
│ └── test_module1.py
├── docs/ # ドキュメント
│ └── index.md
└── temp/ # 一時ファイル（.gitignoreに含める）
```

## フォルダの役割
- **`src/`**: メインソースコードを配置。パッケージ構造で整理
- **`tests/`**: テストコードを配置。`src/`の構造と対応
- **`docs/**`: プロジェクトドキュメントを配置
- **`temp/`**: 一時ファイル・スクリプト出力を保存（既存ルールと整合）

## 命名規則（PEP 8準拠）
- **モジュール・パッケージ**: `snake_case`（例: `data_processing.py`）
- **クラス**: `PascalCase`（例: `DataProcessor`）
- **関数・変数**: `snake_case`（例: `process_data`）
- **定数**: `UPPER_SNAKE_CASE`（例: `MAX_RETRIES`）

# 依存関係管理

- **新規**: `uv init`。**既存**: `venv` 継続使用。**パッケージ**: `uv add <pkg>` / `uv sync`。詳細は [user-rule-cursor-integrated.md](user-rule-cursor-integrated.md) のパッケージ管理を参照。

# エンコーディング対策

## ソースコードのエンコーディング宣言
- **必須**: ファイル先頭に`# -*- coding: utf-8 -*-`を明記
- **理由**: Pythonがソースコードを正しく解釈するため

```python
# -*- coding: utf-8 -*-
"""モジュールの説明"""
```

## ファイル操作時のエンコーディング指定
- **必須**: `open()`で`encoding='utf-8'`を必ず指定
- **理由**: プラットフォーム依存のデフォルトエンコーディングによる問題を回避

```python
# 良い例: エンコーディングを明示
with open('example.txt', 'w', encoding='utf-8') as f:
 f.write('こんにちは、世界！')

with open('example.txt', 'r', encoding='utf-8') as f:
 content = f.read()
```

## Windows環境での設定
- **環境変数**: `PYTHONUTF8=1`を設定（推奨）
- **効果**: ファイル操作時のデフォルトエンコーディングがUTF-8に

```python
import os
os.environ['PYTHONUTF8'] = '1' # スクリプト先頭で設定
```

## コンソール出力の安全な処理
- **問題**: Windowsコンソールはcp932（Shift_JIS）を使用し、Unicode文字でエラーが発生する可能性
- **対策**: Unicode文字出力時はtry-exceptでハンドリング（詳細は本セクションの例および Cp932.md を用意した場合は参照可）

```python
# 良い例: エラーハンドリング付き出力
try:
 print(f"[OK] {file_path.name} -> {new_name}")
except UnicodeEncodeError:
 print(f"[OK] Renamed: {file_path.name}") # ASCII文字のみ
```

## 文字列の正規化
- **推奨**: `unicodedata.normalize()`を使用した正規化
- **用途**: 全角/半角の統一、結合文字の統合

```python
import unicodedata

def normalize_string(s: str) -> str:
 """文字列を正規化（NFC形式）"""
 return unicodedata.normalize('NFC', s)
```

# コード品質管理

- **必須チェック**: [user-rule-cursor-integrated.md](user-rule-cursor-integrated.md) の「Python品質保証」に従う（`uv sync` / `ruff check` / `pyright`）。本ルールはフォルダ構成・エンコーディングを担当する。

# 既存ルールとの統合

## 参照すべき既存ルール
- **Python 品質保証・開発環境（ruff/pyright/uv）**: 詳細は [user-rule-cursor-integrated.md](user-rule-cursor-integrated.md) の「Python品質保証」「Python開発環境」を参照。本ルールはフォルダ構成・エンコーディングを担当する。
- **Cp932.md**: 用意している場合は Windows 環境の cp932 回避の詳細として参照可。

## 重複の回避
- 本ポリシーはフォルダ構成・エンコーディング対策を SoT とする。品質チェック（ruff/pyright）の必須手順は統合版に従う。

# チェックリスト
- [ ] プロジェクト構造が標準フォルダ構成に従っているか
- [ ] ソースコードに`# -*- coding: utf-8 -*-`を記載しているか
- [ ] ファイル操作で`encoding='utf-8'`を指定しているか
- [ ] Windows環境で`PYTHONUTF8`環境変数を設定しているか
- [ ] Unicode文字出力時にエラーハンドリングを実装しているか
- [ ] `ruff check`と`pyright`が通過しているか

# 更新履歴
- 2025/12/02 10:44: 初版作成

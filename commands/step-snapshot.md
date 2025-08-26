# ステップスナップショット（手動フロー）

## 概要
- **目的**: 現在の作業ファイル群を `steps/step-XXX/` に保存し、`STEP_DIFFS.md` に追記します。
- **出力**:
  - `steps/step-XXX/`（3桁ゼロ埋めの連番ディレクトリ）
  - `STEP_DIFFS.md` の新規セクション（ヘッダー、対象ファイル、差分メモ）

## 手順（チェックリスト）
- [ ] **対象ファイルの決定**
  - Git 利用時: `git status --porcelain` で変更ファイル一覧を確認
  - Git 未使用時: 変更した相対パスを手動で列挙
- [ ] **次のステップ番号の決定**
  - 既存の `steps/step-XXX/` を確認し、次の連番（001 → 002 → ...）を採番
- [ ] **フォルダの作成**
  - `steps/step-XXX/` を新規作成（必要に応じてサブディレクトリも作成）
- [ ] **ファイルのコピー**
  - 決定した対象ファイルを相対パスを保って `steps/step-XXX/` 配下にコピー
- [ ] **STEP_DIFFS.md への追記**
  - 下記テンプレートを `STEP_DIFFS.md` 末尾に追加
  - Git 利用時は `git diff` の要点（または抜粋）を貼り付けても良い

## 追記テンプレート
```
## step-XXX - 2025-MM-DD HH:mm:ss
### Files
- path/to/file1
- path/to/file2

### Diff
- 変更の要点を箇条書き、または `git diff` の抜粋を貼り付け
```

## 任意（運用ヒント）
- **対象抽出（Git）**: `git status --porcelain`
- **差分確認（Git）**: `git diff --no-ext-diff --no-color`
- **命名**: `step-XXX` の XXX は 001, 002, ... の3桁ゼロ埋め
- **粒度**: 変更が大きい場合はステップを小さく分割して複数回記録

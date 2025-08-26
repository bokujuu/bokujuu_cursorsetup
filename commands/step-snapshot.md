# ステップスナップショット（手動フロー）

## まずは自動化スクリプト（推奨）
- `scripts/step_snapshot.py` を使うと、変更ファイルのコピーと `STEP_DIFFS.md` 追記を自動化できます。
- 使い方（例）:
  - Git の変更を検出してスナップショット（差分省略）:
    ```bash
    python3 scripts/step_snapshot.py --git --verbose
    ```
  - 明示ファイルでスナップショットし、差分も埋め込む:
    ```bash
    python3 scripts/step_snapshot.py --files commands/step-snapshot.md mcp_enhanced.json --include-diff --message "ドキュメント更新"
    ```
  - ドライラン（実行内容のみ表示）:
    ```bash
    python3 scripts/step_snapshot.py --git --dry-run --verbose
    ```
- 主なオプション:
  - `--files <paths...>`: 直接対象ファイルを列挙（Git未使用時に便利）
  - `--git` / `--no-git`: Git による変更検出の強制/無効化
  - `--include-diff`: `git diff` の出力を `STEP_DIFFS.md` に埋め込み
  - `--diff-context <n>`: 差分の前後文脈行数（デフォルト 3）
  - `--max-diff-lines <n>`: 差分の最大行数（超えると末尾にトランケート表示）
  - `--message "..."`: Diff セクション冒頭に任意メッセージを追加
  - `--steps-dir <name>`: `steps/` のディレクトリ名を変更
  - `--root <path>`: リポジトリルートを明示

---

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

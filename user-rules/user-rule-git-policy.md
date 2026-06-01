---
name: Git運用ポリシー
version: 1.0.0
description: バージョン管理におけるコミット方針とメッセージフォーマット。全プロジェクト共通の運用ルール。
appliesTo: always
---

# Git運用ポリシー

## 目的と適用範囲
- 全プロジェクト（Python、HTML/CSS、VBA、M言語、JavaScript等）で統一されたGit運用方針を定義
- Conventional Commits形式によるコミットメッセージの標準化
- タスク完了時の一貫したコミット実行を目的とする

## コミット方針

### タイミング
- **タスク完了ごと**: 機能追加、バグ修正、リファクタリング、ドキュメント更新など一連の作業が完了した時点
- **品質チェック後**: リンター・型チェッカーが通過した後にコミット
- **論理的な単位**: 1つのコミットは1つの論理的な変更を含む

### 必須事項
- 変更内容を明確に説明するコミットメッセージを必須化
- 複数の無関係な変更は別々のコミットに分割

## コミットメッセージフォーマット

### Conventional Commits形式
日本語で具体的な変更内容を記述：

- **feat**: 新機能追加（例: `feat: ユーザー認証機能を追加`）
- **fix**: バグ修正（例: `fix: ログイン時のエラーハンドリングを修正`）
- **docs**: ドキュメント更新（例: `docs: README.mdにセットアップ手順を追加`）
- **chore**: ビルド・設定変更（例: `chore: .gitignoreを更新`）
- **refactor**: リファクタリング（例: `refactor: データ処理ロジックを最適化`）
- **style**: フォーマット変更（例: `style: ruffでコードフォーマットを統一`）
- **test**: テスト追加・修正（例: `test: ユーザー登録のテストケースを追加`）
- **perf**: パフォーマンス改善（例: `perf: データベースクエリを最適化`）

### 記述例
```bash
# 良い例
git commit -m "feat: Git運用ポリシーを追加"
git commit -m "fix: cp932エンコーディングエラーを修正"
git commit -m "docs: API仕様書のエンドポイント一覧を更新"
git commit -m "refactor: Excel処理を配列操作に変更してパフォーマンス向上"

# 悪い例（曖昧・具体性なし）
git commit -m "更新"
git commit -m "バグ修正"
git commit -m "いろいろ変更"
```

## ブランチ戦略

### 基本方針
プロジェクトの規模に応じて柔軟に選択：

- **小規模・個人プロジェクト**: mainブランチのみでシンプル運用
- **チーム・大規模プロジェクト**: feature/fixブランチを使用し、プルリクエスト経由でマージ

### ブランチ命名規則（チームプロジェクト）
```bash
feature/<機能名> # 例: feature/user-authentication
fix/<バグ内容> # 例: fix/login-error
refactor/<対象> # 例: refactor/database-queries
docs/<ドキュメント> # 例: docs/api-specification
```

## コミット対象

### 管理対象
- **ソースコード**: 
 - Python: `.py`, `pyproject.toml`, `requirements.txt`
 - HTML/CSS/JavaScript: `.html`, `.css`, `.js`, `.json`, `.jsx`, `.tsx`, `.ts`
 - VBA: `.bas`, `.cls`, `.frm`（エクスポート可能な場合）
 - M言語: `.pq`, `.m`
- **設定ファイル**: `.gitignore`, `.editorconfig`, `pyproject.toml`, `package.json`
- **ドキュメント**: `.md`, `.txt`, `.csv`（小規模データ）

### 除外対象
- **バイナリファイル**: 画像・ドキュメント・メディア（`.png`, `.pdf`, `.mp4` 等）
- **一時ファイル**: `temp/`, `.trash/`, `csv/`, `__pycache__/`, `node_modules/`, `.venv/`, `venv/`。一時ファイル・削除の運用詳細は [user-rule-cursor-integrated.md](user-rule-cursor-integrated.md) の「一時ファイル管理」を参照。
- **環境固有**: `.env`, `.env.local`, `.vscode/`, `.idea/`（チーム共有を除く）

## AIアシスタントの動作

### タスク完了時の処理
- コミットを提案または実行
- 変更ファイル数と主要な変更内容を要約

### コミットメッセージの自動生成
- Conventional Commits形式で自動生成
- 変更内容を解析し、適切なプレフィックスを選択
- 具体的で簡潔な日本語メッセージを作成

### 品質チェックとの連携
以下のチェックが通過した後にコミット：
- **Python**: `ruff check`, `pyright`
- **JavaScript**: `eslint`, `prettier`
- **VBA**: 構文チェック、命名規則確認

### コミット前の確認事項
- [ ] リンター・型チェッカーが通過しているか
- [ ] 意図しない変更が含まれていないか
- [ ] コミットメッセージが具体的で明確か
- [ ] 1つのコミットが1つの論理的な変更を表しているか

## プロジェクト別の補足

### Obsidian Vault
- Obsidian Vault 利用時は当該 Vault の `AGENTS.md` の「Git運用」セクションを参照。`.md` 中心の管理、`attachments/` 内テキストは管理対象。

### プロジェクト別
- Python: `pyproject.toml` を真実の情報源、`.venv/` 除外、`uv.lock` 管理対象。フロント: `node_modules/` 除外、lock ファイル管理、`dist/` 等は除外。その他は各プロジェクトの AGENTS.md / README を参照。

## チェックリスト

コミット前に以下を確認：
- [ ] コミットメッセージがConventional Commits形式に従っているか
- [ ] 日本語で具体的な変更内容を記述しているか
- [ ] 品質チェック（リンター・型チェッカー）が通過しているか
- [ ] 不要な変更（デバッグコード、一時ファイル）が含まれていないか
- [ ] 機微情報（パスワード、APIキー）が含まれていないか

## 更新履歴

- 2025/12/02 10:44: 初版作成。Conventional Commits形式のコミット方針とタスク完了時のコミットルールを定義

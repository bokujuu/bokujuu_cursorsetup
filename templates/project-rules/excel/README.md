# Excel / COM / VBA — プロジェクトローカル Cursor ルール

グローバル User Rules に COM・VBA の長文を載せると、全セッションでコンテキストを消費します。  
**Excel 運用があるリポジトリだけ**、以下を `.cursor/rules/*.mdc` にコピーして使います。

## 手順

1. 対象リポの `.cursor/rules/` を作成（無ければ）
2. 本フォルダから必要な `.mdc` をコピー
3. `globs` をプロジェクトのパスに合わせて編集
4. リポの `AGENTS.md` に「グローバル COM/VBA ルールは使わない」と 1 行記載
5. Cursor **Settings → User Rules** から `user-rule-com-automation` / `user-rule-vba-coding-policy` を**削除**

## 同梱ファイル

| ファイル | 用途 |
|----------|------|
| `excel-com-automation.mdc` | `scripts/**` 等の win32com スクリプト |
| `vba-coding-policy.mdc` | `**/vba/**` 等の `.bas` ソース |
| `pcaf-excel-agent.mdc.example` | PCAF 型（SoT・検証・トークン効率）の例。コピー後リネーム可 |

## 参照実装

- [htmlpcafmock](https://github.com/bokujuu/htmlpcafmock) — `.cursor/rules/` に本テンプレを反映済み

## 更新履歴

- 2026/06/03 09:49: 初版（グローバル user-rules から分離）

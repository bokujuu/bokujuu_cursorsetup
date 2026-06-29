# Faceted prompting — 出典と抽象化

## 一次ソース

- [nrslib/takt](https://github.com/nrslib/takt) — [Faceted Prompting](https://github.com/nrslib/takt/blob/main/docs/faceted-prompting.md)（ドキュメント）
- TAKT ワークフロー: 各 step が persona / policy / knowledge / instruction / output contract を分離

## 取り込んだパターン

- 5 種 facet のファイル分離
- implement / review で facet セットを切り替え
- ステップごとに必要なコンテキストだけを渡す

## 除去した固有要素

- takt CLI・npm パッケージ・YAML ワークフロースキーマ
- `.takt/` ディレクトリレイアウト
- プロバイダ固有（Claude Code / Codex SDK 等）の設定
- worktree キュー・`takt run` コマンド

## 配置理由

Ralph ループ（`templates/loop-orchestration/`）の **反復プロンプト設計** に直結。global skill ではなくキット内 facet として同梱。

## 関連（knowledge-base）

- takt 全体の比較: `docs/ai/automations/takt-agent-coordination.md`（CLI は非採用）

# qa-multi-perspective — 出典と抽象化

## 一次ソース

- [Claude Code に「7人の意地悪なQA」を仕込んでテストケースの観点漏れを潰した](https://zenn.dev/nexta_/articles/be13a2395a5d2a)（Nexta Tech Blog / Ayaka, 2026）

## 取り込んだパターン

- 7 ペルソナで観点列挙フェーズを固定
- new-feature / migration でスキル（モード）を分離
- 根拠列必須・推測禁止

## 除去した固有要素

- Blazor + Radzen + SQL Server の製造業 SaaS 前提
- 25 列 CSV・ISO 25010 の固定列定義
- Claude Code 専用のスキルファイルパス
- 「AI 工場」チーム構成の比喩（手順には含めない）

## 配置理由

QA テスト設計はドメイン・表形式・スタックに依存するため **project-skills** に配置。観点固定の**考え方**は汎用。

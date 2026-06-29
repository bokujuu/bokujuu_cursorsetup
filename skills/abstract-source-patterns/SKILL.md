---
name: abstract-source-patterns
description: >-
  Extract reusable abstract patterns from articles, repos, and talks before
  adopting them into global skills, project templates, or knowledge-base notes.
  Use when reviewing bookmarks, evaluating external tools, or deciding what to
  copy versus what to record as reference only. Outputs pattern cards with
  placement (global / template / knowledge-base / skip) and stripping notes.
disable-model-invocation: false
---

# Abstract Source Patterns

外部ソース（記事・GitHub・Speaker Deck 等）から**再利用可能な抽象パターン**を抜き出し、`bokujuu_cursorsetup` / `knowledge-base` への配置判断材料を作る。

直接取り込み（fork・install・全文コピー）の前に必ずこの skill を通す。抽象化そのものが成果物の主目的になる場面で使う。

## いつ使うか

- ブックマークやタイムラインで見つけた記事・repo を「この repo に入れるか」判定するとき
- PR レビューで global suitability を判定するとき（[global-suitability-and-knowledge-capture.md](../../docs/review/global-suitability-and-knowledge-capture.md) と併用）
- 外部 skill / ツールから**パターンだけ**取り込みたいとき
- ユーザーが「抽象化して取り込めるか」「何が残せるか」を聞いたとき

使わない場面:

- ソースをそのままインストール・コピーするだけ（抽象化不要）
- 単なる要約・翻訳（配置判断が不要）
- 既に同梱済みパターンの重複確認だけ → 該当 skill の `references/sources.md` を読む

## ワークフロー

1. **ソース把握** — URL・著者・日付・種別（記事 / repo / ツール）を記録。README または本文を読み、主張と実装を分離する。
2. **パターン抽出** — 下の「抽出レンズ」で抽象概念を列挙。各パターンは **20 語以内の名前** + **1〜3 文の定義** + **除去した固有要素**。
3. **配置判定** — 各パターンを配置表（後述）で分類。1 ソースから複数パターン・複数配置先がありうる。
4. **加工方針** — 採用候補には「何を落とすか」「既存の何に統合するか」を書く。新規 global skill は最後の手段。
5. **出力** — パターンカード形式（後述）で提示。knowledge-base 向けは front matter 付き Markdown 草案まで含めてよい。

## 抽出レンズ（必ず通す観点）

| レンズ | 問い | 例 |
|--------|------|-----|
| **制御構造** | プロセスを誰が・何で閉じるか | レビューループ、完了契約、独立 Evaluator |
| **コンテキスト分割** | 何をファイル・役割・反復で分けるか | persona / policy / knowledge 分離 |
| **観点固定** | 抜けやすい視点をどう構造化するか | 多ペルソナレビュー、観点チェックリスト |
| **ルーティング** | 薄い入口から詳細へどう誘導するか | AGENTS.md ルーター、スキル分岐 |
| **検証ゲート** | 何をもって完了・安全とするか | verify スクリプト、根拠列必須 |
| **メタ認識** | 流行語の下にある古い概念は何か | サイバネティクス、reconcile loop |

固有要素（スタック名・CLI 名・社名・特定列数 CSV 等）はパターン名に入れない。`除去:` 行に書く。

## 配置判定

| 配置先 | 条件 |
|--------|------|
| `skills/`（global） | 複数 repo・複数タスクで再利用。判断基準として抽象化済み。既存 skill と責務重複なし |
| `templates/project-skills/` | タスクカテゴリは汎用だが、適用は特定ドメイン repo が自然（QA・DS 等） |
| `templates/project-rules/` | コピーして使う規約・ルーター・verify 雛形。global install では効かない |
| `docs/`（本 repo） | maintainer 向け設計・採用経緯。配布物ではない |
| `knowledge-base` | global/template にしないが、将来の配置判断・比較・背景として残す価値あり |
| **skip** | 重複・一次情報不足・ドメイン外・加工コスト対効果が低い |

迷ったら **knowledge-base の `docs/research/`** に下書きし、後で整理する。

## パターンカード（出力形式）

各パターンを次の形式で 1 枚ずつ出す。

```md
### パターン: {短い名前}

- **定義**: {抽象化した 1〜3 文}
- **除去**: {落とした固有要素}
- **配置**: global | templates/... | knowledge-base | skip
- **加工**: {既存への統合先、または新規パス}
- **根拠**: {ソース URL}
```

ソース全体の末尾に **サマリ表** を付ける。

## global に入れない典型（再確認）

- 外部 CLI / npm パッケージの丸ごと同梱
- 単一スタック・単一プロダクト機能（Codex `/goal` 等）への依存
- 具体手順の羅列で判断基準に昇華していないもの
- 既存 `ralph-loop` / `skill-lifecycle` と責務が重なるもの（追記を優先）

## 関連 skill・ドキュメント

| 参照 | 用途 |
|------|------|
| [global-suitability-and-knowledge-capture.md](../../docs/review/global-suitability-and-knowledge-capture.md) | 2 段階判定（global → knowledge-base） |
| `skill-lifecycle` | 抽出パターンを repo-local skill 化するとき |
| `retrospective-codify` | 採用後の失敗からルール化するとき |
| `repo-agent-bootstrap` | ルーター型 AGENTS パターンの展開先 |
| [references/sources.md](references/sources.md) | 本 skill の着想・採用先例 |

## 検証

本 skill 自体に自動テストはない。次を満たせば完了:

- 各パターンに `除去:` が書かれている（抽象化の証跡）
- 配置先が表のいずれかに明示されている
- 採用候補に既存資産との統合先または重複チェック結果がある

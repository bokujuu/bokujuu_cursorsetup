---
name: qa-multi-perspective
description: >-
  Generate test perspectives and cases using fixed reviewer personas so
  normal-path bias and recurring blind spots are structurally reduced. Use for
  new-feature test design or legacy migration validation—not for one-off bug
  fixes. Requires primary sources (spec, ticket, code) cited per finding.
---

# QA Multi-Perspective

**多ペルソナ固定**でテスト観点の抜けを減らす repo-local skill。AI に「テストケースを書いて」と一度頼むだけでは正常系偏重になりやすい問題を、**観点の列挙フェーズ**で構造化する。

## いつ使うか

- 新機能のテスト設計（課題・仕様・コードが手元にある）
- 既存システムからの移行・データ投入の検証設計
- 観点リストのレビュー（ケース化の前段）

使わない場面:

- 単発バグ修正の回帰 1 本
- 仕様・一次情報が無い状態（先に入手する）
- 自動 E2E の実装そのもの（観点出しの後）

## モード選択

| モード | 参照 | 正とする一次情報 |
|--------|------|------------------|
| **new-feature** | [references/mode-new-feature.md](references/mode-new-feature.md) | 課題・仕様 + 実装コード |
| **migration** | [references/mode-migration.md](references/mode-migration.md) | 移行仕様・旧データ定義 + 実装 |

モードを混ぜない。ユーザー指示が曖昧なら先に確認する。

## 7 ペルソナ（抽象版）

各ペルソナは **最低 1 観点**を必須とする。観点は「疑う問い」として書く（ケース文にしない）。

| ID | ペルソナ | 疑う点（代表） |
|----|----------|----------------|
| P1 | 初見ユーザー | 説明を読まず直感操作。誤タップ・空送信・連打 |
| P2 | 熟練オペレータ | キーボード・ショートカット・高速入力・IME 変換中の確定 |
| P3 | 敵対的操作者 | 境界値・不正値・権限外・二重送信・バリデーション迂回 |
| P4 | データ整合監査 | UI を信用せず永続化層（DB・API・ファイル）の整合 |
| P5 | 移行担当 | 既存データの欠損・形式差・件数・文字コード・参照整合 |
| P6 | 回帰番人 | 周辺機能・リロード後・「以前動いていた」経路の退化 |
| P7 | 仕様懐疑者 | 実装＝正しい仕様と仮定しない。一次情報との突合 |

P5 は **migration モードで必須**。new-feature では「既存データとの境界」に限定してよい。

## ワークフロー

1. **モード確定** — new-feature / migration。
2. **一次情報収集** — 仕様・課題・関連モジュールを列挙。不足は `要確認` と明示（推測で埋めない）。
3. **観点フェーズ** — P1〜P7 それぞれから観点を箇条書き。ケース化はまだしない。
4. **人間または別セッションでレビュー** — 重複削除・優先度（P1/P2/P3 等）付け。
5. **ケースフェーズ** — 確定観点からケース表を生成。各ケースに **根拠**（仕様節・ファイル・チケット）を必須。
6. **出力** — プロジェクトの CSV / 表形式テンプレに合わせる（列定義は repo 側で上書き）。

## 出力ルール

- 根拠のない期待結果を書かない。不明は `要静的解析` / `要確認`。
- 正常系だけで完了としない。P4・P6・P7 から最低 1 件ずつ観点があること。
- 実装詳細（フレームワーク名・画面部品名）は観点の**例**に留め、ペルソナ定義自体は汎用のまま維持。

## 検証

```bat
{{VERIFY_COMMAND}}
```

例: 観点表の lint（必須ペルソナ列の空欄チェック）や、スプレッドシート用 TSV の列数検証。プロジェクトで `scripts/validate_test_design.py` 等を定義すること。

## 関連

- 着想・除去した固有要素: [references/sources.md](references/sources.md)
- グローバル: `abstract-source-patterns`（パターン抽出）、`skill-lifecycle`（skill 化）

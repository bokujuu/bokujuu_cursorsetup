---
name: natural-japanese
description: 日本語の不自然な言い回し・翻訳調・AI臭を、意味を保って修正する。明示的な採点には同梱診断スクリプトを使う。
license: MIT
---

# 自然な日本語への改稿

元の意味・事実・語り手の文体を保ち、読者がつまずく表現だけ直す。短くすること自体を目標にしない。

- 主語と述語、係り受け、指示語を明確にする。専門語は必要な位置で説明する。
- 意味のない前置き、進行実況、同じ対比や結びの反復を減らす。
- 見出しや箇条書きを全文一律の型へ変えない。重要度に応じた文章の濃淡を保つ。
- 材料の不足を架空の事実や数値で補わない。調査や確認が必要なら、影響する箇所を明示する。
- 読者や文体は依頼・元資料から判断する。任意の文体指定がないだけで作業を止めない。

通常の改稿は修正後の通読で仕上げる。長文・繰り返す癖・機械診断の依頼には、必要な検査を選ぶ。lint全件解消、判断台帳、複数担当によるレビューは完了条件にしない。

## 任意の検査

本スキルのディレクトリから実行する。uv が使えない場合は [手動の観点](references/manual-checklist.md) を使う。

```
uv run scripts/lint.py --json <file>
uv run scripts/lint.py --reading-load <file>
uv run scripts/outline.py <file>
uv run scripts/terms.py <file>
```

lint は疑いの検出であり、文書品質の合否ではない。修正箇所に新たな問題が疑われる場合だけ再検査し、改善のない反復は止める。

`score` は書換えをせず [診断仕様](references/diagnose.md) の指標と限界を示す。`full` は必要な構造・読みやすさの観点を広げる指定であり、固定人数のサブエージェントや長時間ループを要求しない。重い `semantic.py` は `exp` / 深層検出の明示指定時だけ使う。

個別の迷いには [読みやすさ](references/readability-principles.md)、[悪文例](references/readability-antipatterns.md)、[改稿例](references/examples.md) を参照する。文体学習を依頼された場合は [プロファイル雛形](assets/style-profile-template.md) を使う。

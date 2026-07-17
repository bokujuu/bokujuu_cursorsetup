---
name: anti-human-bottleneck
description: >-
  Reduce unnecessary questions to the human. Resolve locally and reversibly on
  your own; do not ask before read/search/edit/test within the request. Require
  explicit ask or clear prior approval for commit, push, PR, deploy, send, or
  publish. Confirm individually for force-push, production, irreversible delete,
  credentials, or billing. Load before pausing for confirmation or presenting
  options solely from uncertainty.
disable-model-invocation: false
metadata:
  author: nyosegawa
  version: 2.0.0
---

# Anti-Human-Bottleneck（ローカル自律と承認境界）

人間への不要な質問を減らし、**ローカルかつ可逆な範囲**では自律的に解決する。  
User Rules（明示のない commit / push / 破壊的操作は行わない）を最上位の安全境界とし、本 skill はそれと矛盾しない。

## 方針

- 調査・編集・検証で止まれるなら、確認せず進める。
- 「should I…?」「is this OK?」「what's next?」は、ローカル可逆なら自分で決めて実行する。
- 外部・不可逆・高リスク操作は、依頼または明確な承認なしに実行しない。

## 自動実行してよい

- Read / Grep / Glob / Web 検索
- ローカルの非破壊的な調査
- 依頼範囲内のファイル編集
- test / lint / typecheck / build
- `git diff` / `git status` / log 確認
- 一時ファイル・test fixture の作成と後片付け
- ローカルかつ可逆な設計判断（複数案があれば最良案を選び、理由を短く述べて進む）

## 明示的な依頼または既存の明確な承認が必要

- commit
- push
- PR 作成・更新
- 外部サービスへの書込み
- email / Slack / issue comment 等の送信
- package / article / release の公開
- deploy

## 個別確認が必要

次は「依頼に含まれているように見える」だけでは足りない。実行前に確認する。

- force-push
- 本番環境の変更
- data / branch / file の不可逆な削除
- real user data の変更
- 課金・購入を伴う操作
- security / permission / credential 境界の変更
- 依頼範囲を大きく広げる変更

## 人間を呼ぶとき

次のいずれかのときだけ質問する。

1. 上の「個別確認が必要」に該当する
2. 物理的・資格的に実行できない（SMS / CAPTCHA / 生体認証 / 未所持クレデンシャル / 法的署名など）
3. ローカル可逆でも、同等に妥当な案が残り、選択が依頼の成果物・スコープを本質的に変える

呼ぶときは:

- 選択肢を 2〜4 個示し、推奨を最初に置く
- なぜ自分で決められないかを一文で述べる
- 人間に求める操作は最小（例: SMS コードの貼付）にし、残りは自分が続ける

## 自己検証

人間に確認させず、ツールで確かめる。

- test / lint / typecheck / build
- `git diff` で自分の変更を読む
- 必要ならブラウザ・API・ログで状態を確認（読取・検証に限る。送信・公開は承認境界に従う）

## 継続

ゴールが残っている間は「次は何をしますか？」と聞かず、依頼と SoT から次手を決める。  
完了したら結果を報告する。自然な follow-up は提案してよいが、承認が必要な操作は実行しない。

## Anti-Patterns

| 言いたくなること | 代わりに |
|---|---|
| 「テストを回しますか？」 | 回す。 |
| 「この設計でいいですか？」（ローカル可逆） | 自分で判断して進める。必要なら理由を短く書く。 |
| 「次は何をしますか？」 | ゴールから次手を決めて進める。 |
| 「push しますか？」（依頼にない） | しない。必要なら提案のみ。 |
| 「削除してよいですか？」（不可逆） | 確認してから。 |
| 「どれがいいですか？」（評価可能な差がある） | 最良案を選び、理由を述べて進める。 |

# メンテナンス チェックリスト

AGENTS.md が既にある repo で実施。所要 10–20 分を目安に、全項目を順に確認する。

## 1. ドリフト検出

- [ ] `git log --oneline --since="<AGENTS.md の更新日>"` で AGENTS.md 更新後の変更を一覧
- [ ] AGENTS.md の「主要コマンド」を全て実行 — 存在しないコマンド・引数変更がないか
- [ ] AGENTS.md の「SoT」リンク先が存在し、内容が現状と矛盾しないか
- [ ] SKILL.md のドメイン知識（列番号・期待件数・手順）が SoT ドキュメントと一致するか
- [ ] AGENTS.md「未決事項」のうち解決済みのものを消し込み

## 2. 検証の再実行

- [ ] `.codex/practice-registry.json` の `verification_commands` を全て実行
- [ ] 失敗した場合: コードのバグか、ルール進化への検証の追従漏れかを切り分ける
      （ルール進化なら SoT → 実装 → 検証 → skill の順で更新）
- [ ] lint / 型チェック（設定があれば）

## 3. skill の更新

- [ ] 前回以降の手戻り・気づきを `references/skill-memory.md` に1行追記
- [ ] 2回以上問題なく再利用できた draft skill を `approved` に昇格
- [ ] 新しい繰り返しタスクがあれば skill 追加（`skill-lifecycle` の検索→作成順で）
- [ ] 使われなくなった skill は registry から外すか SKILL.md に廃止予定を明記

## 4. 仕上げ

- [ ] AGENTS.md の「更新:」日付を実時刻で更新（`Get-Date -Format 'yyyy/MM/dd HH:mm'`）
- [ ] 変更があれば報告テンプレート（SKILL.md 参照）で要約

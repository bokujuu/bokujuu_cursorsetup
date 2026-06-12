---
name: {{SLUG}}
description: >-
  {{SUMMARY}}の標準手順。{{TRIGGER_HINT}}のときに使う。
---

# {{SLUG}} — {{SUMMARY}}

ルール・仕様の SoT は {{SOT_DOC_LINK}}。実装は {{IMPL_PATH}}。
SoT・実装・成果物を常に同期させる。

## いつ使うか

- {{WHEN_1}}
- {{WHEN_2}}

## 手順（この順を崩さない）

1. **SoT 更新** — ルールが変わる場合は先にドキュメントを直す
2. **実装** — {{IMPL_PATH}} を最小変更
3. **再生成/実行**

   ```bat
   {{RUN_COMMAND}}
   ```

4. **検証**（全て通るまで完了と言わない）

   ```bat
   {{VERIFY_COMMAND}}
   {{LINT_COMMAND}}
   ```

5. **ドキュメント反映** — 関連 docs と日付を更新

## ドメイン知識（落とし穴）

<!-- 具体的に書く: 列番号・期待件数・命名・過去の手戻り。汎用論は書かない -->

- {{PITFALL_1}}
- {{PITFALL_2}}

## 検証の合格基準

- {{PASS_CRITERIA_1}}（期待件数など具体値で）
- lint / 型チェックがエラー 0

## メモ

運用で得た知見は [references/skill-memory.md](references/skill-memory.md) に1行ずつ追記する。
`.codex/practice-registry.json` に `draft` で登録済み。安定したら `approved` へ。

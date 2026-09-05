---
name: implement-with-practices
description: 繰り返し使うライブラリ・APIの実装手順を既存のrepo-local practiceへ反映する。通常の実装だけでは新スキルを作らない。
---

# 実装手順の再利用

対象 repo に既存の手順や検証コマンドがあれば再利用する。APIの不確かな点は対象バージョンの一次資料や小さな実験で確かめる。

手順の記録を依頼された場合、または同じ不足が繰り返し確認できた場合に、既存の手順を修正する。成功した実装を毎回スキル化しない。

既存の登録簿を使う案件では `.codex/practice-registry.json` と登録先を維持する。新設する必要がある場合だけ以下の同梱ツールを使う。コマンドは本スキルのディレクトリから実行する。

```
python scripts/scaffold_local_skill.py --help
python scripts/validate_local_skill.py --target <repo>
python scripts/promote_local_skill.py --target <repo> --slug <slug>
```

形式の詳細は [references/local-practice-format.md](references/local-practice-format.md)。昇格ツールの出力は追記案であり、AGENTS.md を自動的に肥大化させない。

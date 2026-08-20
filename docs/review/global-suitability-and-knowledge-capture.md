# Global suitability 判定と knowledge-base 知見化

更新: 2026/08/03 11:01

## 目的

`bokujuu_cursorsetup` は Cursor / Codex 向けの**グローバル設定**を配布する repo である。
ここに入れる内容は「今回の作業で役に立ったもの」ではなく、複数 repo・複数タスクで再利用できる汎用性・メタ性を持つ必要がある。

一方で、global 設定としては不適切でも、将来の配置判断に有用な知見はある。
その場合は `bokujuu_cursorsetup` に入れず、[bokujuu/knowledge-base](https://github.com/bokujuu/knowledge-base) に知見として記録する。

役割分担の概要は knowledge-base 側の [bokujuu-cursorsetup-integration.md](https://github.com/bokujuu/knowledge-base/blob/main/docs/ai/bokujuu-cursorsetup-integration.md) も参照。

## レビューの 2 段階判断

PR レビューでは、次の順で判断する。

1. `bokujuu_cursorsetup` の global 設定として入れるべきか（global suitability）
2. 入れない場合、`knowledge-base` に知見として残すべきか（knowledge capture）

## Global に入れてよい条件

次を満たすものは、`bokujuu_cursorsetup` に入れる候補になる。

- 複数 repo で再利用できる
- 特定案件・特定ファイル・特定ユーザー作業に依存しない
- 個別手順ではなく、判断基準・作業パターン・検証手順として抽象化されている
- 適用条件と対象外が明確である
- 既存 user-rules / skills / templates / docs と責務が重複しない
- Cursor Cloud / Codex CLI / Windows / Linux の差異を不必要に固定しない
- 無関係な repo に特定スタック・コマンド・設計思想を強制しない

グローバル skill を追加・更新する場合は、`.cursor/skills/maintain-global-skill/SKILL.md` の手順も併用する。

## Global に入れない条件

次は、原則として `bokujuu_cursorsetup` の global 設定には入れない。

- 単一 repo 固有の作業手順
- 単発のトラブル対応
- 個人の一時的な運用メモ
- 特定案件名・特定顧客名・特定ファイル名に依存するルール
- 具体例の羅列に留まり、判断基準へ抽象化されていない内容
- 特定環境のローカルパス、個人設定、秘密情報を含む内容
- 既存 skill / user-rule / template で既に扱っている内容
- global にすると他 repo で副作用が大きい内容

既存方針との整合:

- [user-rules-guide.md](../user-rules-guide.md) — User Rules はコミュニケーション枠のみ。技術手順は各リポへ委譲
- [docs/pr/003-excel-rules-project-local.md](../pr/003-excel-rules-project-local.md) — ドメイン特化ルールは `templates/project-rules/` へ移行した先例

## 配置判断

| 内容 | 配置先 |
|------|--------|
| 常時適用される会話・作業姿勢 | `user-rules/` |
| 複数 repo で再利用するタスク手順 | `skills/` |
| 特定技術・特定 repo にコピーして使う規約 | `templates/project-rules/` |
| repo-local skill の雛形 | `templates/project-skills/` |
| 背景説明・設計思想・比較・判断基準 | `docs/` |
| この repo 自体の作業ルール | `AGENTS.md` または `.cursor/skills/` |
| global にはしないが将来参照したい知見 | [bokujuu/knowledge-base](https://github.com/bokujuu/knowledge-base) |

### 判断の目安

- **user-rules/** — 口調・出力形式・最小変更など、常時適用のコミュニケーション枠のみ（約 50 行規模）。コーディング規約や MCP 方針は入れない。
- **skills/** — タスク起動時に適用する手順。`description:` でトリガーと対象外を明示する。
- **templates/** — 対象リポへコピーして使う規約・雛形。global install だけでは効かない。
- **docs/** — 配布物ではなく、設計・運用・移行の説明。本 repo の reviewer / maintainer 向け。
- **AGENTS.md** — この repo 内エージェントの作業ルール。グローバル設定そのものではない。
- **knowledge-base** — 長期的な知見保存。global 化の判断材料・失敗例・調査メモを残す。

## knowledge-base に知見化する条件

global には入れないが、次に該当する場合は `bokujuu/knowledge-base` への PR を作成する。

- 今後の global / local / template 配置判断に使える
- 失敗例として再利用価値がある
- 判断基準の背景として残す価値がある
- PR コメントだけでは後から探しにくい
- 具体例を抽象化する材料になる
- automation / agent / prompt / repo 運用の知見として再利用できる

## knowledge-base に知見化しない条件

次の場合は、source PR へのコメントのみでよい。

- typo や軽微な文言修正
- 単なる構文エラー
- 既存ノートと重複する
- 将来参照価値が低い
- 機密・個人情報・非公開情報を一般化できない
- 内容が曖昧で、記録しても判断材料にならない

## knowledge-base の推奨配置

knowledge-base のディレクトリ規約に従う（[knowledge-base AGENTS.md](https://github.com/bokujuu/knowledge-base/blob/main/AGENTS.md)）。

| 内容 | 配置先 |
|------|--------|
| AI agent / prompt / automation / review 運用 | `docs/ai/automations/` |
| GitHub / repo 運用一般 | `docs/technology/github/` |
| 未整理の調査メモ | `docs/research/` |
| トラブルシュート | `docs/technology/` または `docs/research/` |
| 作業手順として安定したもの | `docs/technology/` または `docs/work/` |

配置に迷う場合は `docs/research/`（`layer: inbox`）に置き、後で整理する。常時入口は knowledge-base の [docs/desk.md](https://github.com/bokujuu/knowledge-base/blob/main/docs/desk.md)。セッション中の知見化手順はグローバル skill `capture-external-intelligence`。

## knowledge-base ノートの front matter 例

knowledge-base 標準に加え、出典を追跡できるフィールドを付ける。

```yaml
---
title:
tags:
  - ai
  - automation
  - github
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
type: note
source_repo: bokujuu/bokujuu_cursorsetup
source_pr:
---
```

## knowledge-base ノートの推奨構成

```md
# タイトル

## 背景

## 判断

## global に入れない理由

## knowledge-base に残す理由

## 再利用できる観点

## 関連

- Source repo:
- Source PR:
```

## source PR へのコメント例

重大度は先頭に `low` / `medium` / `high` を付ける。

```md
medium: この内容は `bokujuu_cursorsetup` の global 設定としては範囲が狭いです。特定 repo の作業手順に依存しており、複数 repo に常時適用するには副作用があります。

ただし、global / local / template の配置判断の具体例としては有用なため、`bokujuu/knowledge-base` 側に知見化する対象として扱うのが適切です。
```

global に入れてよい場合の例:

```md
low: 既存の skill と責務が重複しています。新規 skill ではなく、既存 skill の references 更新を検討してください。
```

知見化不要の例:

```md
low: typo の修正です。knowledge-base への記録は不要です。
```

## Automation / Agent の実行手順

本 repo 内に source PR レビュー用 Automation の実体ファイルはない（2026/06/22 時点）。
Cursor Cloud Agent や手動レビューでは、次の手順に従う。

1. **差分を確認する** — 変更ファイル・意図・既存方針との整合を読む
2. **抽象パターンを抽出する**（外部ソース由来の場合）— グローバル skill `abstract-source-patterns` のパターンカード形式で加工方針を明示
3. **global suitability を判定する** — 上記「入れてよい / 入れない条件」と配置判断表を適用
4. **知見化価値を判定する** — global 不適合の場合のみ、knowledge capture 条件を確認
5. **source PR に重大度付きでコメントする** — 判定理由を簡潔に書く
6. **知見化価値がある場合** — `bokujuu/knowledge-base` に Markdown ノートを追加する PR を別 repo で作成する
7. **knowledge-base PR を作れない環境** — 作成予定のファイルパスと Markdown 本文を source PR コメントまたはレビュー出力に含める

### 禁止事項

- **source PR のコードは自動修正しない** — レビューは判定とコメントのみ
- knowledge-base への記録は、source PR の修正ではなく、別 repo への知見保存として扱う
- global 不適合かつ知見価値ありと判断した場合に限り、knowledge-base 側にノートを追加する

### 関連ドキュメント

- 外部ソースの抽象化: `abstract-source-patterns`（`skills/abstract-source-patterns/`）
- グローバル skill 追加・更新: `.cursor/skills/maintain-global-skill/SKILL.md`
- User Rules 方針: [user-rules-guide.md](../user-rules-guide.md)
- タスク別 skill 参照: [rule-index.md](../rule-index.md)
- knowledge-base 運用: [knowledge-base AGENTS.md](https://github.com/bokujuu/knowledge-base/blob/main/AGENTS.md)

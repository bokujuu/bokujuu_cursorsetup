# Faceted prompting（ループ反復用）

[TAKT](https://github.com/nrslib/takt) の **Faceted Prompting** を抽象化した雛形。1 本の巨大プロンプトではなく、**役割・制約・知識・手順・出力契約**をファイル分離し、反復ごとに必要な facet だけを渡す。

takt CLI / YAML ワークフロー自体は同梱しない（[knowledge-base: takt 参照](https://github.com/bokujuu/knowledge-base/blob/main/docs/ai/automations/takt-agent-coordination.md)）。

## 5 種の facet

| 種別 | 役割 | 例ファイル |
|------|------|------------|
| **persona** | 誰として振る舞うか | `persona-implementer.md`, `persona-reviewer.md` |
| **policy** | 権限・禁止・スコープ | `policy-edit-minimal.md`, `policy-readonly.md` |
| **knowledge** | 事実・リポ文脈（手順は書かない） | `knowledge-repo.md` |
| **instruction** | この反復で何をするか | `instruction-implement.md`, `instruction-review.md` |
| **output-contract** | 出力の形・完了シグナル | `output-contract-iteration.md`, `output-contract-review.md` |

## なぜ分けるか

- 実装反復にレビュー用の長い制約を載せない（コンテキスト汚染を防ぐ）
- レビュー反復では編集禁止を policy で明示し、実装の言い訳を構造で抑える
- 同じ knowledge を複数ステップで再利用できる

## コピー手順

1. 対象リポの `loop/` に [loop-orchestration](../) をコピー済みであること
2. 本 `facets/` フォルダを `loop/facets/` にコピー
3. 各 `*.template` を `.md` にリネームし `{{...}}` を置換
4. `PROMPT-faceted.md.template` を `PROMPT.md` の代替またはベースにする
5. 外側ループ（`ralph.ps1`）はそのまま。反復ごとに PROMPT が指す facet セットだけ切り替える

## 推奨ステップ構成（2 フェーズ）

| フェーズ | persona | policy | instruction | output-contract |
|----------|---------|--------|-------------|-----------------|
| **implement** | implementer | edit-minimal | implement | iteration（`ITERATION_DONE`） |
| **review** | reviewer | readonly | review | review（`REVIEW_PASS` / `NEEDS_FIX`） |

implement → verify 失敗なら implement のみ繰り返し。verify 成功後に review 反復を 1 回挟む運用が最小構成。

## PROMPT の組み立て

`PROMPT-faceted.md.template` は次の順で facet を読み込む指示を含む:

1. persona
2. policy
3. knowledge（AGENTS.md・skills への参照を含む）
4. instruction
5. output-contract

オーケストレータは反復開始前に、使用する facet パスを `current-facets.txt` に 1 行ずつ書いてもよい。

## 関連

- 設計: [docs/pr/004-qa-faceted-adoption.md](../../../docs/pr/004-qa-faceted-adoption.md)
- ループ全体: [docs/loop-engineering.md](../../../docs/loop-engineering.md)
- 出典: [references/sources.md](references/sources.md)

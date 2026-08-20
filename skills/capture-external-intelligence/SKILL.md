---
name: capture-external-intelligence
description: >-
  Persist reusable judgments from this work session to bokujuu/knowledge-base
  instead of growing AGENTS.md. Use for 知見化, 書庫, desk/library, or a failure
  that should survive the next chat. Lookup history with ctx. Not for typo
  fixes, secrets, or third-party article/repo pattern extraction
  (abstract-source-patterns).
---

# capture-external-intelligence

チャットで払った思考コストを、次の AI のスタート地点に残す。常時プロンプトは長くしない。

正本は [bokujuu/knowledge-base](https://github.com/bokujuu/knowledge-base)。入口はそこの `docs/desk.md`。

## いつ動くか

次のいずれかなら、ユーザーに聞かずこの手順に入る（commit / push / PR は依頼があるときだけ）。

- 同じ失敗や調査を、新しいチャットでやり直しそう
- 配置判断（global / template / 案件ローカル / 書庫）が出た
- 再開に必要な「何が終わったか / 未解決 / 次の一手」がチャットの外に無い

やらない: 挨拶だけのセッション、typo、秘密情報、既存ノートの重複コピー。

## 手順

1. **既存を探す**（この順）
   - `ctx` が PATH にあれば: `ctx search --limit 10 --term "<キーワード>"`（必要なら `--workspace`）。ヒットしたら `ctx show event <id> --window 8` で引用する。
   - 無ければ knowledge-base の `docs/desk.md` と `_index.md`、対象フォルダ README。
   - 外部記事のパターン抽出だけなら `abstract-source-patterns` に委譲。
2. **層を決める**
   - `inbox` — 1回目。`docs/research/`
   - `library` — 次の判断を変える。`docs/ai/` `docs/technology/` `docs/work/` など
   - `case` — 過去案件へ戻る。固有名は本文に残してよい
   - skill 昇格 — **2案件以上で再現**し、固有名を剥がせるときだけ。`maintain-global-skill` へ。1回では昇格しない。
3. **ノートを書く**
   - knowledge-base のテンプレ（`docs/_templates/note-template.md`）
   - front matter に `layer:` を付ける
   - 本文は判断・根拠・対象外。チャット全文は貼らない
   - 再開が要る仕事は What changed / Unresolved / Restart を短く
4. **机を更新するか**
   - 再接続トリガーが増えたときだけ `docs/desk.md` に1行
   - 昇格したら `docs/promotion-ledger.md` に1行
5. **索引** — 主要ノートなら `_index.md` またはフォルダ README
6. **PR** — ユーザーが PR を依頼したとき。knowledge-base と cursorsetup は別 PR

## 置かない場所

| 置きがち | 代わり |
|----------|--------|
| 作業中 repo の `AGENTS.md` に長文追記 | 書庫ノート + desk の1行 |
| Gmail / チャット | 控え。正本は git |
| cursorsetup `skills/` への即時フルコピー | ledger 経由。手順化できるまで待 |

## 検証

- ノートに `layer` がある
- desk を読んだだけで再接続先が分かる
- 秘密情報がない

## 関連

- 配置判定のレビュー: `docs/review/global-suitability-and-knowledge-capture.md`（cursorsetup）
- 外部ソース抽象化: `abstract-source-patterns`
- セッション掘り起こし（ctx が使えないとき）: `cursor-session-doc`
- knowledge-base 保守: 対象 repo の `maintain-knowledge-base`
- 出典: [references/sources.md](references/sources.md)

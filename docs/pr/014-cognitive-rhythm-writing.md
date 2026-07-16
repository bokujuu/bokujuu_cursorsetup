# PR design note: cognitive-rhythm-writing

Updated: 2026/07/16

## Purpose

説明的な日本語文章に「認知リズム」（観察→逡巡→断定→再観察、未回収の緊張、緩みと駄文の判別）を設計するグローバル skill。
読み物として読ませたい章・記事・解説の生成、または密度はあるが平坦な文の診断・修正に使う。

## Source

| Item | Value |
|------|-------|
| Upstream | [gist k16shikano/eb2929f13ed19c97188393d297be8432](https://gist.github.com/k16shikano/eb2929f13ed19c97188393d297be8432) |
| Author | [@k16shikano](https://github.com/k16shikano) |
| Raw pin | `6b60201952443293dbc5ac306125439ed1977101` |
| Local slug | `cognitive-rhythm-writing`（upstream `name:` と同一） |

## Design decisions

| Item | Decision |
|------|----------|
| Placement | `skills/`（複数 repo で再利用可能な執筆規範。global suitability OK） |
| Body | upstream 準拠 |
| Local delta | 併用パスのみ `japanese-tech-writing` → `japanese-technical-writing` |
| Ops files | `references/sources.md` / `references/skill-memory.md` |
| Relation | 土台は `japanese-technical-writing`。校正指摘は `japanese-doc-review` |

## Related updates

- `MANIFEST.md` / `docs/rule-index.md` / `INSTALL.md`
- `.codex/practice-registry.json`（draft）

## Verification

```bash
bash scripts/install.sh
python3 scripts/verify_repo_setup.py
python3 scripts/verify_loop_kit.py
```

## Deferred

- gist コメントの LLM 使用例サンプルは同梱しない（運用で必要なら `references/` へ追加）
- upstream の「点検手順」番号と症状処方の対応ずれは upstream 追従時に再確認

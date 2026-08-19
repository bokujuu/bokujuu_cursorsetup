# PR design note: natural-japanese

Updated: 2026/08/19 11:37

## Purpose

仕事の日本語を読みやすく書く・直すグローバル skill。設計→執筆→機械 lint→収束で AI臭さを抑え、議事録・レポート・ガイドから note / エッセイまで扱う。

## Source

| Item | Value |
|------|-------|
| Upstream | [coji/natural-japanese](https://github.com/coji/natural-japanese) |
| Author | [coji](https://github.com/coji) |
| Pin | `0f1cc1c5a4e2aa7590598c88a15c213a60d9545a` |
| Local slug | `natural-japanese`（upstream `name:` と同一） |
| License | MIT |

## Pattern cards

### パターン: 機械検出と判断の分離

- **定義**: AI は自作文の AI臭を認識しにくい。決定的 lint で疑いを突きつけ、直す/残すは文脈判断に委ねる。
- **除去**: `uv` / sudachipy / Claude plugin marketplace / `npx skills add`
- **配置**: global（`skills/natural-japanese`）。scripts は同梱するが verify では実行しない
- **加工**: `uv` 欠如時は既存の `manual-checklist.md` へフォールバック
- **根拠**: https://github.com/coji/natural-japanese

### パターン: 生成時制約（文体憲法）

- **定義**: 事後修正より、書く前の読者・主メッセージ・見出しと、書くときの制約で不自然さを防ぐ。
- **除去**: 12箇条の全文を User Rules に載せない
- **配置**: global skill。User Rules はチャット口調の境界だけ
- **加工**: 技術文書の型・常体は既存 `japanese-technical-writing` を先に使う
- **根拠**: 同上

## Design decisions

| Item | Decision |
|------|----------|
| Placement | `skills/`（複数 repo で再利用。global suitability OK） |
| Body | upstream 準拠 |
| Local delta | 隣接 skill 分担表、`uv` 任意と手動チェックリスト、`sources.md` / `skill-memory.md` |
| Scripts | 同梱。`semantic.py` は opt-in のまま。Cloud / 標準ライブラリ制約の verify では走らせない |
| User Rules | です／ますはチャット応答。文書の文体は skills へ委譲、と1行明確化。憲法は載せない |
| Relation | 型・常体は `japanese-technical-writing`。指摘のみは `japanese-doc-review`。緩急は `cognitive-rhythm-writing` |

## Related updates

- `MANIFEST.md` / `docs/rule-index.md` / `INSTALL.md`
- `user-rules/user-rule-cursor-communication.md` / `docs/user-rules-guide.md`
- `skills/japanese-technical-writing/SKILL.md`、`japanese-doc-review/SKILL.md`、`cognitive-rhythm-writing/SKILL.md`
- `templates/project-skills/README.md`
- `.codex/practice-registry.json`（draft）

## Verification

```powershell
.\scripts\install.ps1
python scripts\verify_repo_setup.py
python scripts\verify_loop_kit.py
```

## Deferred

- `uv` + sudachipy を Cloud / verify の必須にしない
- upstream の corpus / evals / plugin marketplace は同梱しない
- lint.py の Windows 実測は、利用側 PC に `uv` があるときだけ

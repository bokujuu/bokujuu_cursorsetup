# PR: skill-lifecycle + system-structure-viz

## Summary

- グローバル skill `skill-lifecycle`（MUSE 由来の汎用 Skill 進化手順）
- グローバル skill `system-structure-viz`（構造・依存の Tier 別可視化）
- テンプレ `templates/project-skills/`、`templates/structure-viz/`
- 参照 doc `docs/references/muse-autoskill.md`
- MANIFEST / rule-index / INSTALL / implement-with-practices overview 更新

## 背景

- 繰り返しタスクを Skill 資産として増殖・検証・改良する運用（[MUSE-Autoskill](https://arxiv.org/abs/2605.27366)）を配布可能にする。
- 規模に関わらずモジュール・依存の可視化を Tier で選べるようにする。

## Test plan

- [ ] `.\scripts\install.ps1` 後、`%USERPROFILE%\.codex\skills\skill-lifecycle\SKILL.md` が存在
- [ ] 同上で `system-structure-viz\SKILL.md` が存在
- [ ] `templates/project-skills/` を別リポに README 通りコピーできる
- [ ] `templates/structure-viz/site/index.html` をブラウザで開き Mermaid が表示される
- [ ] [docs/rule-index.md](../rule-index.md) から新 skill と muse 参照に辿れる
- [ ] `skill-lifecycle` と `implement-with-practices` の description が役割分担している（目視）

## マージ後

1. `git pull` → `.\scripts\install.ps1`
2. 対象プロジェクトで必要に応じ `templates/project-skills/` または `templates/structure-viz/` をコピー

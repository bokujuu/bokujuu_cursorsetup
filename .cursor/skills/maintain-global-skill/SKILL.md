---
name: maintain-global-skill
description: >-
  bokujuu_cursorsetup の skills/ にグローバル skill を追加・更新する標準手順。
  「skill を追加して」「MANIFEST を更新して」「install して検証」「skill の validation と PR」
  のときに使う。
---

# maintain-global-skill — グローバル skill の追加・更新

ルール・仕様の SoT は [MANIFEST.md](../../../MANIFEST.md) と [docs/rule-index.md](../../../docs/rule-index.md)。
実装は `skills/<slug>/`。配布は `scripts/install.ps1` → `~/.codex/skills/`。

## いつ使うか

- `skills/` に新しいグローバル skill を追加するとき
- 既存 skill の SKILL.md / references を更新し、同梱一覧と整合させるとき
- skill 追加後に検証して PR を出すとき（過去セッションで繰り返し依頼あり）

## 手順（この順を崩さない）

1. **SoT 更新** — 仕様・公開範囲が変わる場合は先に MANIFEST / rule-index を直す
2. **実装** — `skills/<slug>/` を作成または最小変更
   - `SKILL.md` frontmatter: `name:` はフォルダ名と一致
   - `description:` は長さではなく、発火条件・用途・主要な除外条件をモデルが判別できる最短の記述にする。trigger 語の羅列を目的にしない。body の責務を description で過大に宣言しない。近接 Skill との境界が曖昧な場合だけ除外条件を書く。同じ情報を言い換えて重複させない。`templates/project-skills/`（タスクカテゴリ）と `implement-with-practices`（ライブラリ/API 特化）の境界を守る
   - 外部取込みは `references/sources.md` に upstream URL を記載
3. **一覧反映** — [MANIFEST.md](../../../MANIFEST.md) の skills 表に行追加。[docs/rule-index.md](../../../docs/rule-index.md) にユーザー向け行を追加（必要時）。[INSTALL.md](../../../INSTALL.md) の動作確認項目を追加（任意 skill の場合は「任意」明記）
4. **インストール**

   ```bat
   .\scripts\install.ps1
   ```

   Linux / macOS / WSL: `bash scripts/install.sh`

5. **検証**（install の後。`verify_repo_setup.py` は `~/.codex/skills/` 配置も確認）

   ```bat
   python scripts\verify_repo_setup.py
   python scripts\verify_loop_kit.py
   ```

   Linux / Cloud: `python3 scripts/verify_repo_setup.py`（repo のみなら `--repo-only`）

6. **ドキュメント反映** — README / PR 設計メモ（`docs/pr/`）を必要最小限で更新

## ドメイン知識（落とし穴）

- **本 repo を正とする場合** `sync-from-local.ps1` は使わない（`$Root` が二重 `Split-Path` で誤パスになる）。`skills/` を直接編集する
- **再利用性の高い skill** は global（`skills/`）に置き、必要なら対象リポへ `templates/project-skills/` や skill コピーでローカル展開も検討（Japanese skills の先例）
- **PR 前**は `verify_repo_setup.py` を必ず通す。過去セッションでは「validation とテストまで行い PR」と明示依頼あり
- **並行セッション**: `git status` で他人の未コミット変更と衝突しないか確認。検証失敗時はファイルを Read し直す
- `install.ps1` は `skills/` 配下を**全ディレクトリ上書きコピー** — 部分だけ試すなら `-WhatIf` または手動コピー

## 検証の合格基準

- `install.ps1` / `install.sh` 実行後、`verify_repo_setup.py` が exit 0（repo 整合 + 全 skill が `~/.codex/skills/` に配置）
- `verify_loop_kit.py` が exit 0（loop テンプレ同梱）
- 新規 skill の `SKILL.md` が存在し、`name:` が slug と一致

## メモ

運用で得た知見は [references/skill-memory.md](references/skill-memory.md) に1行ずつ追記する。
`.codex/practice-registry.json` に `draft` で登録済み。安定したら `approved` へ。

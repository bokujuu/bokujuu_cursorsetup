# PR 004: QA 多ペルソナ・DS ルーターテンプレの採用設計

更新: 2026/06/29

## 背景

2026/06 のブックマークレビューで、次の 2 件を**抽象化した上で**本 repo に取り込むと判断した。

| # | ソース | 採用パターン |
|---|--------|--------------|
| 3 | [7人の意地悪なQA](https://zenn.dev/nexta_/articles/be13a2395a5d2a) | 多ペルソナ観点固定 |
| 4 | [ds-ai-coding-skills](https://github.com/atsushi-green/ds-ai-coding-skills) | ルーター型 AGENTS + データ安全 verify |

それ以外（mizchi、goal-setter、takt、サイバネティクス記事、headroom）は **knowledge-base** のみ。

新規グローバル skill **`abstract-source-patterns`** で、今後同様の「抽象化→配置」判断を再利用する。

## 項目 3: qa-multi-perspective — 反映の詰め

### 採用する核心

1. **観点フェーズとケースフェーズの分離** — いきなりケース表を出させない
2. **7 ペルソナの固定** — 正常系偏重を構造で抑える
3. **モード 2 分岐** — new-feature / migration（混在禁止）
4. **根拠必須** — 仕様・チケット・コードのいずれか。推測は `要確認`

### 配置

```
templates/project-skills/qa-multi-perspective/
  SKILL.md
  references/
    mode-new-feature.md
    mode-migration.md
    sources.md
    skill-memory.md
```

**global にしない理由**: 出力列（CSV/TSV）、スタック、チケット体系はプロジェクト依存。ペルソナ定義は汎用だが、主用途は QA テスト設計。

### 対象 repo への展開手順

1. `Copy-Item -Recurse templates/project-skills/qa-multi-perspective <repo>/.codex/skills/qa-multi-perspective`
2. `SKILL.md` の `{{VERIFY_COMMAND}}` をプロジェクトの列検証コマンドに差し替え
3. `.codex/practice-registry.json` に `draft` 登録
4. `AGENTS.md` の作業表に「テスト設計 → qa-multi-perspective」を 1 行追加
5. 初回運用後 `skill-memory.md` に摩擦を追記

### 既存 skill との関係

| skill | 関係 |
|-------|------|
| `abstract-source-patterns` | 本テンプレの着想抽出に使用 |
| `skill-lifecycle` | repo-local 化・registry 更新 |
| `japanese-technical-writing` | ケース説明文の体裁（任意） |
| `implement-with-practices` | スタック固有の E2E 実装はこちら |

### 将来の拡張（本 PR 範囲外）

- `multi-perspective-review` として code review に一般化 → 運用実績後に global 化を検討
- `scripts/validate_test_design.py` の共通雛形（列名はプロジェクト設定）

## 項目 4: data-science テンプレ — 反映の詰め

### 採用する核心

1. **薄い AGENTS.md** — タスク種別 → skill / `docs/agent/` へのルーターのみ
2. **`docs/agent/` を SoT** — 指標・データ意味・用語。手順は skill へ
3. **verify 3 本** — raw コミット防止・秘密パターン・文書整合

### 配置

```
templates/project-rules/data-science/
  README.md
  AGENTS.md.template
  data-safety-rules.md
  docs/agent/README.md.template
  scripts/
    check_no_raw_data_commit.py
    check_no_sensitive_patterns.py
    validate_agent_docs.py
  references/sources.md
```

**global にしない理由**: パッケージマネージャ、ディレクトリレイアウト、指標定義はプロジェクトごとに異なる。

### 対象 repo への展開手順

1. `repo-agent-bootstrap` で AGENTS / registry の骨格を作成
2. 本テンプレから `AGENTS.md`・`docs/agent/`・`scripts/` をコピー
3. `{{SETUP_COMMAND}}` 等をプロジェクトの実コマンドに置換
4. `data-safety-rules.md` を `docs/agent/data-safety.md` として配置（リンク整合）
5. CI または pre-commit で verify 3 本を実行
6. DS 固有 skill（`safe-data-handling`, `sql-analysis` 等）は `skill-lifecycle` で追加

### repo-agent-bootstrap との統合

`repo-agent-bootstrap` の `AGENTS.md.template` は汎用。DS 案件では:

- 汎用テンプレで骨格 → **本テンプレでルーター節とデータ安全節を上書き**
- または初回から `data-science/AGENTS.md.template` を SoT として使う

bootstrap skill の README に「DS は `templates/project-rules/data-science/`」を追記するのが次 PR の候補（本 PR では rule-index のみ）。

### 除去の明示（再掲）

- uv / polars 固定コマンド
- Copilot + Claude 二重 skill ツリーの同梱
- 10 種スキルの本文 — 必要なものだけ `implement-with-practices` で scaffold

## abstract-source-patterns skill

| 項目 | 内容 |
|------|------|
| 配置 | `skills/abstract-source-patterns/` |
| 役割 | ソース → パターンカード → 配置判定 |
| 検証 | 手動（パターンカードの `除去:` 必須） |

`skill-lifecycle`（タスク skill 化）・`retrospective-codify`（事後ルール化）・本ドキュメントの global suitability 判定と三角関係。

## knowledge-base 側（本 repo 非採用）

| ソース | ノートパス |
|--------|------------|
| mizchi Speaker Deck | `docs/ai/automations/mizchi-technical-writing-ai-era.md` |
| goal-setter-skill | `docs/ai/automations/goal-setter-completion-contracts.md` |
| takt | `docs/ai/automations/takt-agent-coordination.md` |
| サイバネティクス記事 | `docs/research/loop-engineering-cybernetics.md` |
| headroom | `docs/ai/automations/headroom-context-compression.md` |

## 検証

```bash
bash scripts/install.sh
python3 scripts/verify_repo_setup.py --repo-only
python3 -m py_compile templates/project-rules/data-science/scripts/*.py
python3 scripts/verify_loop_kit.py
```

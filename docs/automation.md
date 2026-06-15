# 自動監査・自動PRのセットアップ

PR/コミットの自動監査と、「新しい汎用概念が話題化したら自動でドラフトPRを起票する」運用を、
GitHub Actions と Cursor Automations の2系統で実現するための手順とプロンプト雛形をまとめる。

対応表:

| やりたいこと | 手段 | 補助（本repoの資産） |
|---|---|---|
| PR/コミットの機械的監査 | GitHub Actions CI（[.github/workflows/ci.yml](../.github/workflows/ci.yml)） | `temp/validate_new_skills.py` |
| PR/コミットのAI監査 | Cursor Automations（イベント起動） | `AGENTS.md`（監査基準） |
| 新概念→ドラフトPR | Cursor Automations（cronスケジュール） | `web-research-resolve` / `skill-lifecycle` / `retrospective-codify` |

> Bugbot は本運用では使わない方針。AI監査は下記 Cursor Automations（イベント起動）で代替する。

---

## 1. GitHub Actions CI（機械的監査）

[.github/workflows/ci.yml](../.github/workflows/ci.yml) が `pull_request` と `main` への `push` で起動し、
以下を監査する。追加設定は不要（GitHub 上で Actions が有効であること）。

- `bash -n`（全 `*.sh` の構文チェック）
- `python3 -m py_compile`（全 `*.py` のコンパイルチェック）
- 全 `*.json` の妥当性チェック
- `bash scripts/install.sh` 実行後に `python3 temp/validate_new_skills.py`（スキル/テンプレ整合性 60 チェック）

`validate_new_skills.py` は `~/.codex/skills/` への配置を前提に検証するため、CI では
`scripts/install.sh` を先に実行している（ローカルでも同順で実行すること）。

---

## 2. Cursor Automations

Cursor のクラウドエージェントを cron もしくはイベント（PR open / push / merge 等）で起動する仕組み。
作成は Cursor ダッシュボード（Automations）で行い、リポジトリ・トリガー・プロンプト・利用ツールを指定する。
詳細: <https://cursor.com/docs/cloud-agent/automations>

設定の流れ:

1. トリガーを選ぶ（例: `Pull request opened` / `cron`）。
2. プロンプト（下記雛形）を貼る。
3. ツールを選ぶ（`Comment on Pull Request` など）。
4. リポジトリを指定する（コード変更やPR作成を伴う場合は必須）。

### 2.1 PR/コミットのAI監査（イベント起動）

- **トリガー**: `Pull request opened` または `Push`
- **リポジトリ**: 本リポジトリ
- **ツール**: `Comment on Pull Request`
- **プロンプト雛形**:

```text
あなたは bokujuu_cursorsetup（Cursor/Codex 設定配布repo）のレビュー担当です。
このPRの差分のみを対象に監査してください。

監査基準:
- リポジトリ直下の AGENTS.md「## Cursor Cloud specific instructions」に従っているか
  （標準ライブラリのみ・python3 前提・install スクリプトの整合 など）。
- skills/ と user-rules/ の追加・変更が既存と重複していないか（rg で確認）。
- *.sh は bash -n、*.py は py_compile、*.json は妥当性が通る変更か。
- temp/validate_new_skills.py の前提（~/.codex/skills へ install 後に検証）を壊していないか。

出力:
- 重大度（high/medium/low）付きで指摘を箇条書き。
- 既にPRコメントで議論済みの点は重複させない。
- 問題なしなら「監査OK」とだけコメントする。
コードの自動修正はせず、コメントのみ行うこと。
```

### 2.2 新概念キャッチアップ → ドラフトPR（cron）

- **トリガー**: `cron`（例: 週次 `0 0 * * 1`）
- **リポジトリ**: 本リポジトリ
- **ツール**: リポジトリへの書き込み（PR作成）
- **プロンプト雛形**:

```text
あなたは bokujuu_cursorsetup のメンテナです。最新の「汎用的な」AIエージェント/開発の
概念・プラクティスを調査し、本リポジトリに未収録なら草案を追加するドラフトPRを作成してください。

手順（必ずこの順序）:
1. 調査: skills/web-research-resolve の手順で、ここ最近に話題化した汎用概念を2〜3件特定する。
   （特定ライブラリ/SDK 固有のものは対象外。横断的に再利用できる概念のみ）
2. 重複チェック（必須）: 各概念について rg で user-rules/ と skills/ を検索し、
   既存とぶつかる場合は「新規追加」ではなく「既存ファイルへの追記」を選ぶ。
   - skill 化の判断は skills/skill-lifecycle/SKILL.md の lifecycle loop に従う。
   - ルール/lint/skill のどこに固定するかは skills/retrospective-codify/SKILL.md の分類表に従う。
3. 反映: 新規 skill は templates/project-skills/ の雛形から作成し、
   practice-registry が必要なら status: draft で登録する。user-rules への追記は最小差分にする。
4. 検証: bash scripts/install.sh の後に python3 temp/validate_new_skills.py を通す。
5. PR: cursor/ プレフィックスのブランチを切り、必ず draft PR で起票する。
   PR本文に「調査した概念・出典URL・重複チェック結果・採用理由」を明記する。

制約:
- 勝手に main へ push しない。必ず draft PR とし、人間レビューを前提にする。
- 1回の実行で追加する概念は最大2件まで。肥大化を避ける。
- 出典のない概念は採用しない。
```

---

## 注意事項

- Automations の作成・cron 設定・有効化は Cursor ダッシュボード側の操作で、リポジトリのコミットでは行わない。
  本ファイルはそのプロンプト雛形と運用方針を保管する場所。
- 自動PRは必ず **draft + 人間レビュー必須** とし、`skill-lifecycle` / `retrospective-codify` の
  「重複チェック」「承認 → 書き出し」方針を守る（無秩序な skill/ルールの肥大化を防ぐ）。
- CI を pre-commit/pre-push でも回したい場合は、`.github/workflows/ci.yml` の各コマンドを
  git フックに転記する（任意）。

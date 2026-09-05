---
name: cursor-session-doc
description: >-
  Builds a SESSION_DOC from local Cursor agent-transcript jsonl when ctx
  (ctxrs/ctx) cannot run, or when the user names a transcript/session ID to
  extract. Prefer `ctx search` / `ctx show` for history recall.
  Not for writing knowledge-base library notes (capture-external-intelligence).
---

# Cursor Session Doc

Prefer `ctx search` / `ctx show` ([ctxrs/ctx](https://github.com/ctxrs/ctx)) when `ctx` is on PATH. Use this skill only if ctx is missing or the user gave a transcript/session ID to extract from jsonl.

まず `scripts/extract_session_context.py` を実行し、出力を `OBSERVED` の根拠とする。`INFERRED` は、ログと現在のワークスペースを読んだあとにだけ書く。

## 前提（Cursor）

- ログ場所: `%USERPROFILE%\.cursor\projects\<workspace-slug>\agent-transcripts\<session-id>\<session-id>.jsonl`
- 親チャットの ID を渡す（例: `dd1da77b-f181-47e4-8f33-5cf7557b24cb`）。サブエージェント ID は `subagents/` 配下に別 jsonl がある場合あり。
- **Codex の SQLite ログは使わない**。Cursor 専用。

## ワークフロー

### 1. セッションコンテキストを抽出

```powershell
python skills/cursor-session-doc/scripts/extract_session_context.py `
  --session-id <SESSION_ID> `
  --format markdown
```

オプション:

- `--projects-root` … 既定は `%USERPROFILE%\.cursor\projects`
- `--workspace-slug` … 探索範囲を `projects\<slug>\` に限定（高速化）
- `--include-subagents` … `subagents/*.jsonl` も要約に含める
- `--format json` … 後続スクリプト向け

リポジトリ clone 後は、bokujuu_cursorsetup ルートから:

```powershell
python skills/cursor-session-doc/scripts/extract_session_context.py --session-id <ID> --format markdown
```

インストール先（`install.ps1` 後）:

```powershell
python $env:USERPROFILE\.codex\skills\cursor-session-doc\scripts\extract_session_context.py --session-id <ID> --format markdown
```

### 2. ワークスペースの残存状態を読む

- `git status --short`
- リポジトリの `AGENTS.md` / `README.md`（あれば）
- 抽出結果の `touched_files` / `next_read_targets` に列挙されたファイル

### 3. 事実と推測を分離

| 区分 | 内容 |
|------|------|
| `OBSERVED` | jsonl 上の tool 呼び出し、触ったパス、シェルコマンド種別、時刻窓 |
| `INFERRED` | 結論、意図、未コミット変更の意味 |
| `UNKNOWN` | ログに無いユーザー発話、最終回答の欠落、事後変更 |

### 4. 引き継ぎ文書を書く

- 逐語録は作らない。
- ユーザー意図はログまたは残存ファイルで裏付けできる場合のみ書く。
- 証拠が薄いときは `UNKNOWN` に明示。

## 出力フォーマット

```markdown
# SESSION_DOC

## OBSERVED
- session_id: ...
- transcript_path: ...
- workspace_slug: ...
- time_window: ...
- tool_summary: ...
- touched_files: ...
- shell_commands: ...

## INFERRED
- conclusion: ...
- implemented_changes: ...
- verification_result: ...
- residual_gaps: ...

## UNKNOWN
- missing_user_prompts: true|false
- missing_final_reply: true|false
- ambiguous_points: ...
```

簡潔さ優先。散文は最小限。

## 抽出ルール

- ローカル jsonl を最優先。記憶や推測で補わない。
- `Write` / `StrReplace` / `Read` の `path` を編集対象の根拠とする。
- `Shell` の `command` から検証・インストール・git 操作を分類する。
- `Task` はサブエージェント起動として記録し、詳細は `--include-subagents` 時のみ展開。
- セッション後に手で変えたファイルは「事後ドリフトあり」と明記。

## 失敗時

| 状況 | 対応 |
|------|------|
| ID の jsonl がこの PC に無い | このマシンからは復元不可と報告 |
| ログが薄い | `UNKNOWN` を厚めにした部分ドキュメント |
| 複数 workspace に同名 ID | `--workspace-slug` で絞るか、候補パスを列挙してユーザーに確認 |

## codex-session-doc からの移行

- 旧 `codex-session-doc` は Codex Desktop / CLI 用。Cursor では **本 skill を使う**。
- Codexの履歴は利用環境の履歴取得機能を使う。旧スキルの再インストールは不要。

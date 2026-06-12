---
name: repo-agent-bootstrap
description: >-
  リポジトリにエージェント基盤（AGENTS.md・repoローカル skill・practice-registry・検証コマンド）を
  初期構築またはメンテナンスする。「repoローカルのスキルやAGENTS.mdをセットアップして」
  「エージェントが効率的に動ける状態にして」「リポジトリの状況を見回して基盤を整備して」
  「AGENTS.md を最新化して」等の依頼で使う。新規リポジトリの立ち上げ直後や、
  しばらく運用したリポジトリの基盤ドリフト解消にも使う。
---

# repo-agent-bootstrap — エージェント基盤の初期構築とメンテナンス

リポジトリを「エージェントが迷わず動ける状態」にする。成果物は次の4点とその同期:

| 成果物 | 役割 |
|--------|------|
| `AGENTS.md`（repo 直下） | 目的・SoT の場所・主要コマンド・不変条件・未決事項 |
| `.cursor/skills/<slug>/`（または `.codex/skills/`） | 繰り返しタスクの標準手順 + ドメイン知識 + skill-memory |
| `.codex/practice-registry.json` | skill の登録簿（slug / triggers / verification_commands / status） |
| 検証コマンド | ルール・コード・出力の同期を機械チェックする手段 |

## モード判定

- repo 直下に `AGENTS.md` が **無い** → **初期構築モード**
- **有る** → **メンテナンスモード**（ドリフト解消・skill 追加）

---

## 初期構築モード

### 1. 調査（コードより先に文脈を読む）

詳細手順: [references/survey-guide.md](references/survey-guide.md)

1. `README.md`・`docs/`・`git log --oneline -10` で目的と進捗を把握
2. **過去セッションをマイニング**: `agent-transcripts/*.jsonl` からユーザー発言を抽出し、
   指示・方針転換・**手戻り（「誤りがある」等の訂正）** を拾う。手戻りは skill のドメイン知識の最有力候補
3. **並行セッションの検出**: 主要ファイルの `LastWriteTime` と作業開始時刻を比較。
   作業中も SoT ファイルの更新時刻変化に注意する（後述の落とし穴）

### 2. 設計（書く前に決める）

- リポジトリの **SoT はどのドキュメントか**（例: ルール定義 md、仕様書）
- **繰り返すタスクカテゴリ**は何か（1つに絞る。複数あっても初回は最頻のもの）
- **検証コマンド**は何か。無ければ作る価値があるか（§4）
- **不変条件**（壊してはいけない性質: 列数維持、エンコーディング、データ非転記など）

### 3. 作成

テンプレート: [assets/templates/](assets/templates/)

1. `AGENTS.md.template` → repo 直下へ。プレースホルダを埋める（日付は実時刻を取得）
2. `skill/` → `.cursor/skills/<slug>/` へ。手順・ドメイン知識・合格基準を具体化し、
   調査で拾った手戻りを `references/skill-memory.md` に初期知見として記録
3. `practice-registry.json` → `.codex/practice-registry.json`（`status: draft`）

### 4. 検証コマンドの恒久化（推奨）

過去セッションでアドホックに行われた検証（行数比較・整合チェック等）があれば、
スクリプト化して repo に残す。可能なら**二重検証**にする:

- **同期チェック**: 実装の出力 == 成果物（コード・成果物のずれ検出）
- **独立チェック**: ルール文書から直接再実装した検証（実装自体のバグ検出）

### 5. 検証と仕上げ

1. registry の `verification_commands` を**全て実行**し、通るまで完了と言わない
2. `README.md` に AGENTS.md / skill へのリンクと検証コマンドを追記（最小限）
3. lint・型チェック（プロジェクトに設定があれば）

---

## メンテナンスモード

チェックリスト: [references/maintenance-checklist.md](references/maintenance-checklist.md)

1. **ドリフト検出**: AGENTS.md・SKILL.md の記述と、SoT ドキュメント・コードの
   更新時刻 / 内容を突合（`git log --since`、`LastWriteTime`）
2. registry の `verification_commands` を再実行。失敗 = ドリフトの証拠
3. ずれた記述を修正し、`skill-memory.md` に1行追記
4. 安定運用できている draft skill は `approved` へ昇格
5. 新しい繰り返しタスクが生まれていれば skill を追加（`skill-lifecycle` の検索→作成順を守る）

---

## 落とし穴（実績ベース）

- **並行セッション**: 別チャットが SoT・コードを同時編集していることがある。
  作業前後でファイル更新時刻を確認し、自分が読んだ版が最新か疑う。
  検証コマンドの失敗が「並行セッションのルール進化」の検出器として機能した実績あり
- **transcript の文字化け**: PowerShell では `-Encoding UTF8` 指定 + `[Console]::OutputEncoding` 設定。
  構造は `{"role":..., "message":{"content":[{"type":"text","text":...}]}}`（survey-guide 参照）
- **AGENTS.md の肥大化**: 50–80行程度に抑える。詳細は docs / skill へリンクで逃がす
- **skill の汎用化しすぎ**: repo ローカル skill は具体的な列番号・コマンド・数値（期待件数等）を書く。
  汎用論はグローバル skill の仕事

## 報告テンプレート（ユーザー向け・日本語）

```markdown
## エージェント基盤セットアップ

- **モード**: 初期構築 / メンテナンス
- **調査**: …（目的・過去セッションからの知見・並行セッション有無）
- **作成/更新**: AGENTS.md / .cursor/skills/<slug>/ / practice-registry / 検証スクリプト
- **検証**: …（コマンド + OK/NG）
- **次**: …（DWH 等外部待ち / promote / 追加 skill 候補）
```

## Reference

- [references/survey-guide.md](references/survey-guide.md) — 調査・transcript マイニング詳細
- [references/maintenance-checklist.md](references/maintenance-checklist.md) — メンテナンス チェックリスト
- [assets/templates/](assets/templates/) — AGENTS.md / skill / registry 雛形
- 関連グローバル skill: `skill-lifecycle`（skill の検索→draft→registry→promote）、
  `cursor-session-doc`（過去セッションの本格的な掘り起こし）、`retrospective-codify`（失敗の知見化）

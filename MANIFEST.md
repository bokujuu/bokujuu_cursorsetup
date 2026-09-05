# 同梱マニフェスト

最終同期の想定元（ローカル）。`scripts/sync-from-local.ps1` で再取得できます（Windows・rulemaintenance 利用時）。

## user-rules/

| ファイル | 内容 |
|----------|------|
| `user-rule-cursor-communication.md` | コミュニケーション枠のみ（約 50 行）。技術手順は各リポへ委譲 |

**正の編集場所**: 本リポジトリを正とする場合は `user-rules/` を直接編集。

**廃止（user-rules から削除）**: `user-rule-cursor-integrated.md` および専門ルール 7 件（python/git/mcp 等）、`user-rule-agent-handoff-recovery.md`。旧 COM/VBA ルールは以前より `templates/project-rules/excel/` へ移行済み。

## skills/（グローバル・自作のみ）

| スキル | 備考 |
|--------|------|
| `cursor-session-doc` | Cursor `agent-transcripts/*.jsonl` 用（本 repo 内で管理） |
| `implement-with-practices` | 既存repo-local手順の再利用・更新。自動のスキル新設はしない |
| `agent-handoff-recovery` | 実際の指示ずれ・未統合・完了不一致からの復旧 |
| `japanese-doc-review` | 日本語文書の根拠ある指摘。通常は全観点、固定形式は指定時のみ |
| `japanese-technical-writing` | 技術説明・設計書・手順書。因果と再現性、任意の5種テンプレ |
| `natural-japanese` | 意味を保つ日本語改稿。lint・採点は必要時。MIT / coji由来の診断資産を保持 |
| `repo-agent-bootstrap` | repo固有の入口と手順の整備。スキル・registry新設は必要時のみ |
| `excel-deliverable-quality` | Excel/CSV 成果物の品質・レイアウト規約。常時: スクリプトで生成し `.xlsm` 手編集しない／数式エラーゼロ・数式優先・出典注記・納品前検証。場面依存（必須でない）: 人間が入力する成果物では役割を色で区別（カラーコードは固定しない）・配布帳票の印刷規律・内部データの very hidden 隔離。COM を第一・openpyxl+LibreOffice を代替とし、COM 手順は `templates/project-rules/excel/excel-com-automation.mdc` に委譲。設計源: ユーザー運用リポ [htmlPCAFmock](https://github.com/bokujuu/htmlPCAFmock) / [utf_ken_all](https://github.com/bokujuu/utf_ken_all) の一般化。着想元: [anthropics/skills `xlsx`](https://github.com/anthropics/skills)（Proprietary のため原則のみ参照・本文は独自実装） |
| `non-interactive-hang` | エージェントが verify を素早く回すための非対話ループ（人間 pause 維持・実測 timeout・秒単位 watchdog 自己検証）。考え方: [docs/fast-agent-test-loop.md](docs/fast-agent-test-loop.md)。雛形: `templates/project-ci/non-interactive-hang/` |
| `abstract-source-patterns` | 記事・repo から抽象パターンを抽出し global / template / knowledge-base への配置を判定。PR レビュー・ブックマーク評価と併用 |
| `capture-external-intelligence` | セッションで得た判断を knowledge-base（机／書庫）へ残す。AGENTS.md 肥大化を避ける。`ctx` で過去セッション検索。昇格は再現後のみ |
| `requirement-aligned-fixtures` | 要件・スキーマに沿ったダミーデータ設計。三軸バランス（決定性・変動・グループ）、volume tier、カバレッジ行列、Generation Spec・manifest。併用: 定番メソッド（static/seeded/factory）、factory_boy+Faker、lifelike-synthetic-data-generator（`references/companion-tools.md`）。表形式・PCAF 型は `references/tabular-excel.md`。帳票は `excel-deliverable-quality` |
| `cognitive-rhythm-writing` | 読み物の緩急。拍数・緊張台帳・必須併用を削除 |
| `slide-narration-video` | 全画面スライド＋TTS 解説動画（monologue／dialogue＝理解確認型の解説役＋聞き手）。Marp / ffmpeg 静止画結合（動きなし） / Remotion・Motion Canvas（モーションあり）、VOICEVOX 既定。JT はスライド論理、`dialogue-writing` は dialogue 台詞、cognitive-rhythm は monologue／場面接続を担当。配置 QA・TTS 読み正規化ゲートあり。設計: [docs/pr/015-slide-narration-video.md](docs/pr/015-slide-narration-video.md) / 追記: [docs/pr/017-slide-narration-ffmpeg-mermaid.md](docs/pr/017-slide-narration-ffmpeg-mermaid.md) |
| `voicevox-theater-video` | `slide-narration-video` の劇場拡張。全身立ち絵（胴体クロップなし）、ワイプ字幕（色縁→黒縁→白字）、実音波形同期口パク（+0.1s）、AviUtl「弾む」系の無音登場／Y回転＋弾む退場。プロファイル既定はひまり／つむぎ（ひまり優先版・つむぎ「さっぱり」版の取得元は `references/tachie-sources.md`）。`dialogue-writing` の発話可能性に加え、会話密度・前提・メタ分離を持つ。合成は Pillow＋ffmpeg pipe |
| `power-query-refactor` | Power Query M の編集方針（挙動保持・配置原則・notes・Table.Buffer）。帳票品質は `excel-deliverable-quality`、COM export/import は各リポへ委譲。設計源: [bokujuu/powerquery_refactor](https://github.com/bokujuu/powerquery_refactor)。設計: [docs/pr/016-power-query-refactor.md](docs/pr/016-power-query-refactor.md) |
| `md-html-visual-doc` | Agent→人間向けの視覚ドキュメント（Markdown + 選択的 HTML）。Companion HTML / 事前レンダ図 / `<details>` 等。スライドは `slide-narration-video`、transcript は `cursor-session-doc` に委譲。外部 VisualCave 等は丸導入せずパターンのみ。設計: [docs/pr/017-md-html-visual-doc.md](docs/pr/017-md-html-visual-doc.md) |
| `eli5` | 大きな絵と少ない言葉の HTML で、知らない人向けに説明する（`/eli5`）。本文は [anthropics/claude-plugins-community eli5](https://github.com/anthropics/claude-plugins-community/tree/main/eli5) の原文。設計: [docs/pr/019-eli5.md](docs/pr/019-eli5.md) |

## hooks/（任意・Windows）

| ファイル | 内容 |
|----------|------|
| `handoff-stop-check.py` | Cursor `stop` / `subagentStop` 用 |
| `knowledge-capture-nudge.py` | Cursor `sessionStart` / `stop`（未コミット Markdown 時） |
| `hooks.template.json` | `install.ps1` が `%USERPROFILE%\.cursor\hooks.json` に展開 |
| `README.md` | 手動マージ手順 |

## templates/project-rules/excel/

| ファイル | 内容 |
|----------|------|
| `README.md` | リポへの `.cursor/rules/` コピー手順 |
| `excel-com-automation.mdc` | win32com 共通（要 globs 調整） |
| `vba-coding-policy.mdc` | VBA 共通 |
| `pcaf-excel-agent.mdc.example` | SoT・検証・トークン効率の例 |

## templates/project-skills/

| ファイル | 内容 |
|----------|------|
| `README.md` | 対象リポの `.codex/skills/` 展開手順 |
| `practice-registry.json` | registry 雛形 |
| `skill/SKILL.md` | 汎用 repo-local skill 雛形 |
| `skill/references/skill-memory.md` | skill 単位の経験メモ |
| `qa-multi-perspective/` | 多ペルソナ固定のテスト観点 skill（new-feature / migration）。着想: [Zenn 7人の意地悪なQA](https://zenn.dev/nexta_/articles/be13a2395a5d2a) |

## templates/loop-orchestration/facets/

| ファイル | 内容 |
|----------|------|
| `README.md` | Faceted prompting のコピー手順・5 種 facet・implement/review 切替 |
| `persona-*.md.template` 等 | persona / policy / knowledge / instruction / output-contract |
| `PROMPT-faceted.md.template` | facet 組み立て版プロンプト |
| `references/sources.md` | 出典（[TAKT faceted prompting](https://github.com/nrslib/takt)） |

## templates/structure-viz/

| ファイル | 内容 |
|----------|------|
| `README.md` | Tier 1 / 3 のコピー手順 |
| `architecture.md` | Tier 1: Mermaid 置き場 |
| `site/index.html` | Tier 3: 単一 HTML + Mermaid CDN |

## templates/loop-orchestration/

| ファイル | 内容 |
|----------|------|
| `README.md` | コピー手順・Tier 1–5 スタック・Windows 注意 |
| `run-once.ps1` / `ralph.ps1` | Tier 1 CLI ループ |
| `ralph.mjs` | Tier 2 F — `@cursor/sdk` TypeScript |
| `ralph.sh` | Tier 4 WSL / Linux |
| `start-bridge.ps1` | Tier 3 手動 Bridge |
| `PROMPT.md.template` 等 | Ralph 状態ファイル雛形 |

## templates/project-ci/non-interactive-hang/

| ファイル | 内容 |
|----------|------|
| `README.md` | `scripts/ci/` へのコピー手順・検証順 |
| `run_with_watchdog.py` | pause 検知 + wall-clock timeout（exit 124） |
| `calibrate_timeout.py` | 実測 p95 → `timeouts.json` |
| `test_watchdog.py` | 秒単位自己検証（Excel 不要） |
| `fixtures/` | pause_probe / false_positive_log |
| `*.example` | presets / timeouts の雛形 |

## docs/（追加分）

| ファイル | 内容 |
|----------|------|
| `fast-agent-test-loop.md` | 素早くテストを回す考え方（非対話・実測 timeout・秒検証） |
| `loop-engineering.md` | 4 層スタック・SDK 安定優先（A–F）・Windows 回避 |

## scripts/（追加分）

| ファイル | 内容 |
|----------|------|
| `verify_loop_kit.py` | loop-orchestration テンプレ同梱検証 |
| `verify_non_interactive_hang_kit.py` | non-interactive-hang テンプレ同梱 + test_watchdog |
| `sdk-smoke.ps1` | CLI + TS SDK + Python async スモーク |


## docs/

| ファイル | 内容 |
|----------|------|
| `rule-index.md` | タスク別ルール参照 |
| `model-routing.md` | Astraの運用・内側ループ・旧キットとの区別 |
| `loop-engineering.md` | ループ 4 層・SDK 安定優先（A–F） |
| `user-rules-guide.md` | Settings への貼り方（1 ファイル運用） |
| `migration-from-legacy.md` | 旧 `.cursor/` からの移行 |
| `hooks-handoff-recovery.md` | handoff recovery 設計メモ |
| `pr/` | PR 設計メモ |
| `review/global-suitability-and-knowledge-capture.md` | PR レビュー: global suitability 判定と knowledge-base 知見化 |

## mcp/

| ファイル | 内容 |
|----------|------|
| `mcp.template.json` | Cursor 用の最小構成の雛形（filesystem / memory / blender / codex-sol・terra・luna）。context7 は非同梱 |
| `codex-mcp.template.toml` | Codex グローバル `config.toml` 用の管理対象（filesystem / memory / blender / codex-sol・terra・luna） |
| `mcp.optional.json` | excel / github / playwright / serena（任意） |
| `README.md` | Cursor / Codex への適用手順・グローバル vs プロジェクト配置・セキュリティ注意 |

## 意図的に含めないもの

| 対象 | 理由 |
|------|------|
| `%USERPROFILE%\.cursor\skills-cursor\` | Cursor 製品同梱。Cursor が自動同期 |
| `%USERPROFILE%\.codex\skills\.system\` | Codex 同梱 |
| 各プロジェクトの `.cursor/skills/` | リポジトリローカル |
| Obsidian Vault の commands | ワークスペース専用 |
| 旧 `.cursor/commands` / `mcp_enhanced.json` / `step_snapshot.py` | 廃止（移行表: `docs/migration-from-legacy.md`） |
| `codex-primary-runtime`（空ディレクトリ） | 中身なしのため同梱しない |


## Astra移行の配布境界

`scripts/retired-skills.json` の4件は `archive/pre-astra-20260905/` に保存し、配布しません。現行は18件。各判断は [docs/astra-skill-audit.md](docs/astra-skill-audit.md)。

`scripts/sync_skills.py` が管理対象を同期し、置換・退役した配置は `~/.codex/skill-archives/` に退避します。製品同梱・外部プラグインは管理対象外です。

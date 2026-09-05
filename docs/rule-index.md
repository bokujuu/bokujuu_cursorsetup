# ルールインデックス（タスク別参照）

技術手順・コーディング規約は **リポジトリ側**（`AGENTS.md`、`.cursor/rules/`、skills）を正とする。  
グローバル User Rules は [user-rule-cursor-communication.md](../user-rules/user-rule-cursor-communication.md) のコミュニケーション枠のみ。

適用の考え方は [user-rules-guide.md](user-rules-guide.md) を参照してください。

## タスク別の参照順

| タスク | 参照順 |
|--------|--------|
| **Python** | リポ `AGENTS.md` → `.cursor/rules/` |
| **COM/Excel（win32com）** | skill `excel-deliverable-quality` → 対象リポの `.cursor/rules/excel-com-automation.mdc`（雛形: `templates/project-rules/excel/`） |
| **エージェント検証の高速化（pause / timeout）** | [fast-agent-test-loop.md](fast-agent-test-loop.md) → skill `non-interactive-hang` → `templates/project-ci/non-interactive-hang/` |
| **Excel/CSV 成果物の品質・レイアウト** | skill `excel-deliverable-quality` |
| **Power Query / M の可読化・配置・Buffer** | skill `power-query-refactor` → ブック出し入れは各リポの workflow / AGENTS |
| **ダミーデータ・fixture・サンプル CSV/素データ** | skill `requirement-aligned-fixtures` → 帳票化は `excel-deliverable-quality` |
| **VBA** | 対象リポの `.cursor/rules/vba-coding-policy.mdc`（雛形: `templates/project-rules/excel/`） |
| **Git** | リポ `AGENTS.md` とプロジェクト Rules |
| **フロント/ブックマークレット** | リポ `AGENTS.md` とプロジェクト Rules |
| **ルール作成** | `templates/project-skills/` → 対象リポの `.codex/skills/` |
| **エージェント基盤** | skill `repo-agent-bootstrap` → `templates/project-skills/` |
| **指示ずれ・セッション折り返し** | skill `agent-handoff-recovery` |
| **Astra の運用・モデル選択** | [model-routing.md](model-routing.md) → ループ上書きは `templates/loop-orchestration/` |
| **Skill 化・進化（繰り返し手順）** | まず既存の global / repo-local skill と `templates/project-skills/` を検索し、ギャップがある場合のみ対象リポの `.codex/skills/` に作成。`verify` → `.codex/practice-registry.json` 登録（`verification_commands` 実行）の順。技術特化は `implement-with-practices` |
| **構造・依存の可視化** | `templates/structure-viz/` → 対象リポの `docs/` または静的サイト |
| **人間向けの視覚ドキュメント（MD + HTML）** | skill `md-html-visual-doc` → 文章の論理は `japanese-technical-writing`。スライド動画は `slide-narration-video`、transcript は `cursor-session-doc` |
| **超簡単な絵解説（ELI5）** | skill `eli5` → 大きな絵と少ない言葉の HTML。比較表・手順ギャラリーは `md-html-visual-doc`、スライド動画は `slide-narration-video` |
| **日本語技術文書（作成・改稿）** | skill `japanese-technical-writing` |
| **日本語の自然さ・AI臭さ（仕事文書・リライト）** | skill `natural-japanese` → 技術文書の型・常体は `japanese-technical-writing` を先に。読み物の緩急は `cognitive-rhythm-writing`。指摘のみは `japanese-doc-review` |
| **日本語の読み物・解説文の緩急（認知リズム）** | skill `cognitive-rhythm-writing` → 技術文書の土台は `japanese-technical-writing` |
| **全画面スライド解説動画（Marp＋TTS）** | skill `slide-narration-video` → JT はスライド構成、`dialogue-writing` は dialogue の各台詞、cognitive-rhythm は monologue と場面接続。理解確認が中心なら `dialogue`（解説役＋聞き手）、短い告知・手順は `monologue`。動きなしは ffmpeg 静止画結合、モーションありは Remotion／Motion Canvas。配置 QA（はみ出し・画像比）と TTS 読み正規化あり |
| **VOICEVOX 劇場レイアウト動画（立ち絵＋ワイプ字幕）** | skill `voicevox-theater-video` → 親 `slide-narration-video`（dialogue）。各台詞は `dialogue-writing`、劇場側は発話可能性の確認・会話密度・前提・メタ分離・全身立ち絵・口パク（実音＋0.1s遅れ）・弾む登場／退場・字幕3パス縁取りを担当。一人称は主語・目的語として使い、文頭の飾りにしない。プロファイル既定はひまり／つむぎ。立ち絵の取得元・SHA-256・取得手順は `references/tachie-sources.md`。 |
| **日本語文書レビュー（校正・指摘）** | skill `japanese-doc-review` |
| **bokujuu_cursorsetup の PR レビュー** | [review/global-suitability-and-knowledge-capture.md](review/global-suitability-and-knowledge-capture.md) → skill `abstract-source-patterns` |
| **セッション判断の書庫化（知見化）** | skill `capture-external-intelligence` → [bokujuu/knowledge-base](https://github.com/bokujuu/knowledge-base) の `docs/desk.md`。過去セッションは `ctx`（jsonl 直読みは `cursor-session-doc`） |
| **外部記事・repo の採用判断** | skill `abstract-source-patterns` → [global-suitability-and-knowledge-capture.md](review/global-suitability-and-knowledge-capture.md) |
| **QA テスト観点（7 ペルソナ）** | 雛形 `templates/project-skills/qa-multi-perspective/` |

日本語文書のスキルは、依頼に合うものだけを使います。通常のレビューは構成・文法・表記・誤字を対象とし、文体と形式はユーザー指定・既存文書を優先します。動画制作から文章スキルを一律には読み込みません。

## グローバル skill（install 後）

| skill | 用途 |
|-------|------|
| `agent-handoff-recovery` | 実際の指示ずれ・未統合・完了不一致からの復旧 |
| `cursor-session-doc` | ctx が使えないときの jsonl 要約。履歴検索の正は `ctx` |
| `md-html-visual-doc` | Agent→人間向け MD + 選択的 HTML（比較ビュー・ギャラリー・フロー画像） |
| `eli5` | 知らない人向けの大きな絵＋少ない言葉の HTML（`/eli5`）。upstream 原文 |
| `implement-with-practices` | 既存repo-local手順の再利用・更新。自動のスキル新設はしない |
| `repo-agent-bootstrap` | repo固有の入口と手順の整備。スキル・registry新設は必要時のみ |
| `japanese-doc-review` | 日本語文書の根拠ある指摘。通常は全観点、固定形式は指定時のみ |
| `japanese-technical-writing` | 技術説明・設計書・手順書。因果と再現性、任意の5種テンプレ |
| `natural-japanese` | 意味を保つ日本語改稿。lint・採点は必要時。MIT / coji由来の診断資産を保持 |
| `cognitive-rhythm-writing` | 読み物の緩急。拍数・緊張台帳・必須併用を削除 |
| `slide-narration-video` | 全画面スライド解説動画（Marp＋VOICEVOX＋ffmpeg／Remotion／Motion Canvas）。monologue／dialogue 切替、配置 QA・読み正規化ゲートあり。依存: JT（スライド論理） / `dialogue-writing`（dialogue 台詞） / cognitive rhythm（monologue・場面接続） |
| `voicevox-theater-video` | VOICEVOX 劇場拡張（全身立ち絵・ワイプ字幕・実音口パク+0.1s・弾む登場／退場）。`dialogue-writing` の発話可能性、ひまり／つむぎ既定・会話密度／前提／メタ分離あり。立ち絵取得元は `references/tachie-sources.md`。親: `slide-narration-video` |
| `excel-deliverable-quality` | Excel/CSV 成果物の品質・レイアウト規約・納品前検証 |
| `power-query-refactor` | Power Query M の編集方針（配置・notes・Table.Buffer）。COM export/import は各リポへ |
| `non-interactive-hang` | 非対話 verify・実測 timeout・watchdog 秒検証 |
| `abstract-source-patterns` | 外部ソースから抽象パターン抽出・配置判定（global / template / knowledge-base） |
| `capture-external-intelligence` | 仕事中の判断を knowledge-base へ残す（机は小さく、書庫へ再接続）。skill 昇格は再現後 |
| `requirement-aligned-fixtures` | 要件に沿ったダミーデータ設計（tier・三軸バランス・カバレッジ・manifest） |


## 旧構成からの移行

廃止した `.cursor/commands`、旧 user-rules（コーディング規約・MCP 方針等）、旧 MCP ドキュメントとの対応表: [migration-from-legacy.md](migration-from-legacy.md)


## 継続・退役スキル

通常の継続は利用環境の基本機能を使います。外側ループの手動構築のみ `templates/loop-orchestration/` を参照します。退役・軽量化の全件判断は [astra-skill-audit.md](astra-skill-audit.md)。

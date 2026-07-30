# ルールインデックス（タスク別参照）

技術手順・コーディング規約は **リポジトリ側**（`AGENTS.md`、`.cursor/rules/`、skills）を正とする。  
グローバル User Rules は [user-rule-cursor-communication.md](../user-rules/user-rule-cursor-communication.md) のコミュニケーション枠のみ。

適用の考え方は [user-rules-guide.md](user-rules-guide.md) を参照してください。

## タスク別の参照順

| タスク | 参照順 |
|--------|--------|
| **Python** | リポ `AGENTS.md` → `.cursor/rules/` → skill `implement-with-practices` |
| **COM/Excel（win32com）** | skill `excel-deliverable-quality` → 対象リポの `.cursor/rules/excel-com-automation.mdc`（雛形: `templates/project-rules/excel/`） |
| **エージェント検証の高速化（pause / timeout）** | [fast-agent-test-loop.md](fast-agent-test-loop.md) → skill `non-interactive-hang` → `templates/project-ci/non-interactive-hang/` |
| **Excel/CSV 成果物の品質・レイアウト** | skill `excel-deliverable-quality` |
| **Power Query / M の可読化・配置・Buffer** | skill `power-query-refactor` → ブック出し入れは各リポの workflow / AGENTS |
| **ダミーデータ・fixture・サンプル CSV/素データ** | skill `requirement-aligned-fixtures` → 帳票化は `excel-deliverable-quality` |
| **VBA** | 対象リポの `.cursor/rules/vba-coding-policy.mdc`（雛形: `templates/project-rules/excel/`） |
| **Git** | リポ `AGENTS.md` とプロジェクト Rules |
| **フロント/ブックマークレット** | リポ `AGENTS.md` とプロジェクト Rules |
| **ルール作成** | skill `skill-lifecycle` → `templates/project-skills/` |
| **ループ・無人収束（Ralph）** | skill `ralph-loop` → `templates/loop-orchestration/` → [loop-engineering.md](loop-engineering.md)。ローカル自律と承認境界は `anti-human-bottleneck` |
| **エージェント基盤** | skill `repo-agent-bootstrap` → `templates/project-skills/` |
| **指示ずれ・セッション折り返し** | skill `agent-handoff-recovery` |
| **非自明タスクの着手・観測優先の推論** | skill `fable-style-reasoning` → ずれ発生後は `agent-handoff-recovery` |
| **Grok / Composer の使い分け** | [model-routing.md](model-routing.md) → ループ上書きは `templates/loop-orchestration/` |
| **Skill 化・進化（繰り返し手順）** | skill `skill-lifecycle` → 雛形 `templates/project-skills/`。技術特化は `implement-with-practices` |
| **構造・依存の可視化** | skill `system-structure-viz` → 雛形 `templates/structure-viz/` |
| **人間向けの視覚ドキュメント（MD + HTML）** | skill `md-html-visual-doc` → 文章の論理は `japanese-technical-writing`。構造長期図は `system-structure-viz`、スライド動画は `slide-narration-video`、transcript は `cursor-session-doc` |
| **日本語技術文書（作成・改稿）** | skill `japanese-technical-writing` |
| **日本語の読み物・解説文の緩急（認知リズム）** | skill `cognitive-rhythm-writing` → 技術文書の土台は `japanese-technical-writing` |
| **全画面スライド解説動画（Marp＋TTS）** | skill `slide-narration-video` → 構成は `japanese-technical-writing`、原稿の緩急は `cognitive-rhythm-writing`。動きなしは ffmpeg 静止画結合、モーションありは Remotion／Motion Canvas。配置 QA（はみ出し・画像比）と TTS 読み正規化あり |
| **日本語文書レビュー（校正・指摘）** | skill `japanese-doc-review` |
| **bokujuu_cursorsetup の PR レビュー** | [review/global-suitability-and-knowledge-capture.md](review/global-suitability-and-knowledge-capture.md) → skill `abstract-source-patterns` |
| **外部記事・repo の採用判断** | skill `abstract-source-patterns` → [global-suitability-and-knowledge-capture.md](review/global-suitability-and-knowledge-capture.md) |
| **QA テスト観点（7 ペルソナ）** | 雛形 `templates/project-skills/qa-multi-perspective/` → `skill-lifecycle` |
| **ループ反復の Faceted prompting** | `templates/loop-orchestration/facets/` → [loop-engineering.md](loop-engineering.md) → `ralph-loop` |

日本語文書 skill の運用: 執筆は `japanese-technical-writing`、読み物として読ませたい章・記事・解説の緩急は `cognitive-rhythm-writing`、全画面スライド＋ナレーション解説動画は `slide-narration-video`（上記2 skill に依存）、指摘レビューは `japanese-doc-review`。「レビューして」単独は STRUCTURE のみ。全観点は `全部` / `総合` / `全観点` を指定する。

## グローバル skill（install 後）

| skill | 用途 |
|-------|------|
| `agent-handoff-recovery` | Plan/SoT/verify のずれを検知して状況整理 |
| `cursor-session-doc` | 過去 Cursor セッションの jsonl 要約 |
| `retrospective-codify` | タスク完了後の学びのルール化 |
| `skill-lifecycle` | タスクカテゴリ Skill の検索・作成・registry・改良 |
| `system-structure-viz` | アーキテクチャ・依存の可視化（Tier 1/2/3） |
| `md-html-visual-doc` | Agent→人間向け MD + 選択的 HTML（比較ビュー・ギャラリー・フロー画像） |
| `implement-with-practices` | ライブラリ/API 特化の repo-local practice（skill-lifecycle と併用） |
| `ralph-loop` | 外側ループ（Ralph）— `templates/loop-orchestration/` と併用 |
| `repo-agent-bootstrap` | AGENTS.md / registry / verify の初期構築 |
| `japanese-doc-review` | 日本語 prose のレビュー・校正指摘（固定出力形式・観点依存） |
| `japanese-technical-writing` | 日本語技術文書の作成・改稿（テンプレート方針・5種テンプレ） |
| `cognitive-rhythm-writing` | 説明文の認知リズム（緩急・緊張・駄文判別）。読み物向け生成／平坦文の診断 |
| `slide-narration-video` | 全画面スライド解説動画（Marp＋VOICEVOX＋ffmpeg／Remotion／Motion Canvas）。配置 QA・読み正規化ゲートあり。依存: JT writing / cognitive rhythm |
| `excel-deliverable-quality` | Excel/CSV 成果物の品質・レイアウト規約・納品前検証 |
| `power-query-refactor` | Power Query M の編集方針（配置・notes・Table.Buffer）。COM export/import は各リポへ |
| `non-interactive-hang` | 非対話 verify・実測 timeout・watchdog 秒検証 |
| `abstract-source-patterns` | 外部ソースから抽象パターン抽出・配置判定（global / template / knowledge-base） |
| `requirement-aligned-fixtures` | 要件に沿ったダミーデータ設計（tier・三軸バランス・カバレッジ・manifest） |
| `fable-style-reasoning` | Observation-first reasoning for Cursor agents（Grok / Composer; backbone: official excerpts / supplement: Phase 0–4; light/full） |

外部参照: [references/muse-autoskill.md](references/muse-autoskill.md)

## 旧構成からの移行

廃止した `.cursor/commands`、旧 user-rules（コーディング規約・MCP 方針等）、旧 MCP ドキュメントとの対応表: [migration-from-legacy.md](migration-from-legacy.md)

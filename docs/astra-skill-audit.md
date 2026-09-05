# Astra移行に伴うスキル監査

更新: 2026/09/06 00:02

自作スキル22件を確認し、4件を退役、17件を軽量化・境界修正、1件を維持しました。新スキルは追加していません。Cursor・Codexが対象です。Claudeはユーザーの追加指示により対象外です。

## 判断の根拠と限界

GPT-6 Astraの公式ガイドは、スキル内の曖昧・競合する指示、過剰な確認、過剰な検証の監査を推奨しています。本環境の基本指示にも、自律継続・承認の引継ぎ・必要な検証の規定があります。[OpenAI公式ガイド](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra)

共有資料の32枚目はハーネスの陳腐化、33枚目は素の状態の観察から始める順序を扱っています。今回、モデルの推論を細かく誘導する規則と、成果物の正しさを確かめる仕組みを分けて判断しました。[Speaker Deck](https://speakerdeck.com/kinopeee/hanesu-sekkei-nyuumon-kontekisuto-no-tsugi?slide=32)

最初に対象スキルを適用せず、Git同期と既存の機械検証を実行しました。その後、全22件のSKILL.mdと関係する参照資料・配布経路・フックを監査対象として読みました。公式情報の確認にはOpenAI Docsを参照しました。製品の基本指示や、この会話に既に載ったスキル一覧まで除いた「裸のモデル」ではありません。

実施したのは静的な指示監査と配布・整合性の検証です。同一課題をスキル有無で繰り返すモデル性能のA/B試験は実施していません。「性能が低下していた」「高速化した」とは断定しません。

## 全件の判断

| スキル | 判断 | 残す価値／削った指示 |
|---|---|---|
| fable-style-reasoning | 退役 | 他モデルのsystem prompt模倣、固定Phase 0–4、計画先頭の錨、再検証の重複。基本動作へ委ねる |
| anti-human-bottleneck | 退役 | 確認前の追加ロードと再承認の分岐を削除。自律性と承認引継ぎは短いUser Rulesへ |
| ralph-loop | 退役 | 長時間作業・PRDだけで外側ループが発火する入口を削除。旧キットは手動展開用に保持 |
| web-research-resolve | 退役 | 一般的な検索・比較・実装の手順は基本機能に重複。一次資料と必要な検証は維持 |
| agent-handoff-recovery | 軽量化 | 実際の不一致だけで起動。編集停止ゲート、固定報告、通常着手時の発火を削除 |
| implement-with-practices | 軽量化 | 再利用用スクリプトを保持。通常実装からの自動スキル増殖を削除 |
| repo-agent-bootstrap | 軽量化 | repo固有情報と雛形を保持。毎回の履歴採掘・registry新設・二重検証を削除 |
| japanese-doc-review | 軽量化 | 根拠のある指摘を保持。未指定時の構成限定、下流観点の抑止、通常回答の固定帳票を削除 |
| japanese-technical-writing | 軽量化 | 因果・前提・再現性と文書雛形を保持。固定順序・四項目の事前宣言を削除 |
| natural-japanese | 軽量化 | lint・採点・悪文例を保持。短文lint必須、固定人数レビュー、台帳と収束儀式を削除 |
| cognitive-rhythm-writing | 軽量化 | 読み物の緩急を保持。常時未回収の緊張、拍数、台帳、他スキルの必須ロードを削除 |
| abstract-source-patterns | 境界修正 | 外部資料の配置判断は独自価値あり。単純インストールの前提工程から外す |
| capture-external-intelligence | 境界修正 | 書庫の場所・記録形式を保持。通常作業から別repoへ自動的に書き始める発火を削除 |
| cursor-session-doc | 境界修正 | Cursorログの実抽出スクリプトを保持。退役したCodexログ用スキルの再導入案内を削除 |
| eli5 | 維持 | 10行の明示的な図解HTML依頼。特定成果物を選ぶ短い入口で、推論介入ではない |
| excel-deliverable-quality | 境界修正 | 数式・VBA保持・再計算・配色の実務条件を保持。CSVへのブック規約適用、xlsm読取禁止、未使用セルまでの走査を修正 |
| non-interactive-hang | 軽量化 | 実測timeout・watchdog・非対話入口はモデルで代替できない。毎回のwatchdog自己試験を削除 |
| power-query-refactor | 境界修正 | folding・結合キー・結果比較を保持。実行環境がないときも安全な静的整理を進める |
| requirement-aligned-fixtures | 軽量化 | 再現性・分布・参照整合を保持。小fixtureの別台帳や全tier、固定割合のサンプル監査を緩和 |
| slide-narration-video | 軽量化 | キュー・音声同期・配置と読みの検証を保持。文章スキルの一括読込と独立工程の待ち合わせを削除 |
| voicevox-theater-video | 境界修正 | 素材・字幕・口パク・実測済み既定値を保持。文章構成スキルは必要な場合だけ参照 |
| md-html-visual-doc | 境界修正 | 保存可能な比較HTML・安全な埋込みを保持。Cursor固有canvas固定と不要なMermaid画像生成を削除 |

SKILL.md本体の合計ファイルサイズは181,715→92,678 bytes（約49%減、改行を含むUTF-8実ファイル）。参照資料・アーカイブはこの集計に含めません。常時ロードされるトークン数や性能改善率ではありません。

製品同梱・プラグイン提供のスキルは、このrepoの配布原本ではないため変更していません。`ctx-agent-history-search`も別管理です。改稿では特定プラグインの存在を前提にせず、Cursor・Codex両方に残す価値のある手順を維持しました。

## ループと配布

通常は現在のエージェントの継続・ツール実行を使います。非同期処理は実際に利用可能なツールとIDで回収し、依存操作は結果を待ちます。再起動型の外側ループを構築する場合のみ、永続状態・上限・停止条件を用意します。[現行方針](model-routing.md)

旧スキルは [archive/pre-astra-20260905](../archive/pre-astra-20260905/README.md) に保存し、入口をSKILL.md.archivedへ変更しました。インストーラーはskills/だけを配布し、旧配置を検出範囲外の `~/.codex/skill-archives/` に退避します。同名の既存版も保存し、同一内容ならコピーを省きます。

本環境の共有配置は `~/.codex/skills/`。Cursorはこの互換ディレクトリを読み込みます。Cursor Cloudへのホーム配布は別途設定が必要であり、今回のローカル配置確認には含めません。[Cursor公式資料](https://prod.cursor.com/help/customization/skills)

終了フックは既定のインストールから外しました。配置済みスクリプトも、対象repoの `.cursor/handoff-recovery.local.md` または `.cursor/knowledge-capture.local.md` がある場合だけ通知します。権限管理や危険操作を止めるフックは変更していません。

## 同期・検証結果

- `git fetch origin` → `git merge --ff-only origin/main`: dcf3d6eへ同期。開始時は2コミット遅れ、同期後はHEADとorigin/mainの差0。
- 既存の追跡済みMCP関連変更はstash退避後に再適用。復元用stashは保持。未追跡の `.cursor/mcp.json` は変更していません。
- 変更前の `python scripts/verify_repo_setup.py --repo-only`: OK。
- `python scripts/test_sync_skills.py`: 4 tests OK（退役・バックアップ・失敗時復元・再実行・無関係スキルとClaudeの不変更）。
- `python scripts/test_optional_hooks.py`: 1 test OK（旧計画があっても既定で無通知、有効化時のみ通知）。
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/install.ps1`: OK。最初の実配置でWindowsのディレクトリrenameが一度失敗したため、検出範囲外のstagingと上限付きretryへ変更し再実行。失敗時の旧版復元も試験。
- `python scripts/verify_repo_setup.py`: OK（全配布ファイルのSHA-256一致、退役4件の不在を含む）。
- `python scripts/verify_loop_kit.py`: OK（旧手動キットの整合性）。
- 変更Pythonの `python -m py_compile`、Git Bashの `bash -n scripts/install.sh`、`git diff --check`: OK。

Codexのローカルmodel設定は既に `gpt-6-astra` でした。User Rules原本を短く調整し、CodexのAGENTS.mdへバックアップ付きで反映しました。配置済みCursorフックも更新済みです。既存のSol/Terra/Luna MCPは開始前の変更を維持しています。

残る手動反映は、Cursor SettingsのUser Rulesへの [原本](../user-rules/user-rule-cursor-communication.md) の貼り直しと、両製品の新しいタスクでの読込み確認です。既に進行中の会話から旧スキルの内容が消えるわけではありません。コミット・pushは未実施です。

## 今後の性能確認

同じモデル・推論設定・対象ファイルで、スキルなし／新版／旧版の代表課題を比較します。観測するのは、成果の正しさ、未完了箇所、不要な確認、無関係なファイル作成、ツール数と経過時間です。短い校正、全観点レビュー、小fixture、通常実装、実際の復旧、非同期結果回収を候補にし、各ケースを複数回測ります。旧版でしか防げない再現可能な失敗が出た部分だけ、最小の条件を戻します。

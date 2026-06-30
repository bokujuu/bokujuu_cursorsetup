---
name: requirement-aligned-fixtures
description: >-
  要件・スキーマ・検証目的に沿ってダミーデータ（fixture / サンプル CSV・Excel 素データ・
  JSON 等）を設計・生成する。行数が少なく実用性が低い、乱数だけ増やしてグループ性が崩れる、
  エラー境界のカバレッジが甘い、といった不満を避けるため、決定性・変動・グループの三軸バランス、
  ボリューム階層、カバレッジ行列、不変条件検証、manifest 付き再現性を定める。
  「ダミーデータを作って」「テスト用サンプルを増やして」「取込用 CSV の fixture を設計して」
  「htmlPCAFmock / PCAF 用の素データを作って」などで起動する。本番データの匿名化そのものや
  ライブラリ API の実装手順は対象外（それぞれ別 skill / implement-with-practices）。
---

# requirement-aligned-fixtures — 要件に沿ったダミーデータ設計・生成

テスト・開発・デモ用の**ダミーデータを「たくさんランダムに」ではなく、要件と検証目的から逆算して設計する** skill。
`htmlPCAFmock` 等の運用 Excel・取込 CSV で顕在化しやすい不満（行数不足、リピート性とランダム性と
グループ性のバランス不良、境界値カバレッジ不足）を、再現可能な手順で解消する。

## いつ使うか

- スキーマ・仕様・既存検証スクリプトがあり、**それに沿った** fixture を新規作成・拡張するとき
- 行数を増やしたいが、**意味のあるグループ**（部署・承認状態・日付バケット等）を保ちたいとき
- バリデーション・数式・参照整合・文字コード等、**壊れやすい境界**を意図的に含めたいとき
- 同じ seed で CI / ローカルが同じデータを再現できるようにしたいとき

使わない場面:

- **本番データのマスキング・匿名化**のみ（プライバシー工程は別途。合成データ生成は本 skill）
- **Excel 帳票のレイアウト・数式規約**そのもの → `excel-deliverable-quality`（本 skill は素データ設計）
- **win32com / openpyxl の API 手順** → 対象リポの `.cursor/rules/` または `implement-with-practices`
- 仕様・スキーマが無く推測だけで埋めるとき（先に一次情報を集める）

## 関連 skill（役割分担）

| skill | 役割 |
|-------|------|
| **本 skill** | 何件・どんな分布・どんな境界を入れるかの**設計と生成仕様** |
| `excel-deliverable-quality` | 生成したデータを Excel 成果物に載せるときの**品質・ビルド・検証** |
| `qa-multi-perspective` | **観点の抜け**を減らすレビュー（特に migration モードのデータ不変条件） |
| `implement-with-practices` | Faker / factory_boy 等の**ライブラリ別**実装パターンの repo-local 化 |

## 併用ツール・定番メソッド

設計（本 skill）のあと、**CSV / JSON 取込用の実ファイル**は環境に応じて次と併用する。
詳細・選定・接続パターン: [references/companion-tools.md](references/companion-tools.md)。

| 種別 | 代表 | 用途 |
|------|------|------|
| **定番メソッド** | Static fixture、Seeded generation、Factory/Builder、Negative 分離 | 取込ファイルの作り方の型。tier と対応づける |
| **factory_boy + Faker**（seed 固定） | [factory_boy](https://factoryboy.readthedocs.io/) + [Faker](https://faker.readthedocs.io/) | Python で CSV/JSON を書き出す。ドメイン固有列・FK・グループ内変動 |
| **lifelike-synthetic-data-generator** | https://github.com/jovd83/lifelike-synthetic-data-generator | スキーマ config + CLI で CSV/JSON 等を一括生成。seed・locale・分布 |

**原則**: 本 skill で Generation Spec と tier を先に決め、併用ツールは**実装層**に留める。
API 手順の深掘りは `implement-with-practices`、帳票への載せ方は `excel-deliverable-quality`。

## ワークフロー（この順を崩さない）

1. **要件取り込み** — 一次情報を列挙する（スキーマ、制約、既存 verify、利用シナリオ）。不足は `要確認` と明示し推測で埋めない。
2. **目的とボリューム階層** — [references/volume-tiers.md](references/volume-tiers.md) で tier を選ぶ（smoke / dev / stress / negative）。
3. **三軸バランスの設計** — [references/three-axis-balance.md](references/three-axis-balance.md) で決定性・変動・グループを割り当てる。
4. **カバレッジ行列** — [references/coverage-matrix.md](references/coverage-matrix.md) で境界・異常系・参照整合の行を計画する（正常系だけで完了しない）。
5. **生成仕様（Generation Spec）** — seed・グループ定義・分布・固定行（アンカー行）を [references/generation-spec.md](references/generation-spec.md) の形式で書く。
6. **実装** — [companion-tools.md](references/companion-tools.md) から併用ツールを選び CSV/JSON を生成。
   ハンドメイドの大量コピペは避ける（smoke アンカーのみ静的 fixture 可）。
7. **不変条件検証** — 件数・主キー・FK・集計・文字コード・ソート順を機械検証する（プロジェクトの verify があればそれを正とする）。
8. **manifest** — seed・生成器バージョン・checksum・tier を同梱し、再現手順を 1 コマンドで書く。
9. **サンプル監査** — 全体の 1〜5% を人間可読で spot check（ビジネス不整合が型検証をすり抜けないか）。

表形式（CSV / Excel 素データ）の追加注意: [references/tabular-excel.md](references/tabular-excel.md)。

## 三軸バランス（要約）

| 軸 | 役割 | 典型ミス |
|----|------|----------|
| **決定性（Repeatability）** | 同じ入力 → 同じ出力。CI 失敗の再現 | seed 未固定、日時・UUID を毎回変える |
| **変動（Variation）** | 同一パターンの繰り返しを避け、検証に効く幅 | 完全ランダムでグループが崩れる |
| **グループ性（Grouping）** | 集計・フィルタ・ワークフロー単位のまとまり | 一様乱数で「部署ごと」「状態ごと」の件数が偏らない |

**原則**: まずグループとアンカー行を固定し、グループ内の変動だけに seed 付き乱数を使う。
「全体をランダムにしてから件数を合わせる」のは禁止に近いアンチパターン。

## ボリューム階層（要約）

| Tier | 目安 | 用途 |
|------|------|------|
| `smoke` | 最小（境界 1 件ずつ + アンカー数行） | 高速回帰・スキーマ確認 |
| `dev` | 実用（例: 50〜500 行、ドメインによる） | 日常開発・手動確認 |
| `stress` | 大（要件の上限付近） | 性能・UI スクロール・集計 |
| `negative` | 小さく意図的に壊す | エラーハンドリング専用（正データと分離） |

詳細: [references/volume-tiers.md](references/volume-tiers.md)。

## カバレッジ（要約）

最低限、カバレッジ行列に次を検討して **意図的に行を割り当て**する:

- 空 / NULL / 空白のみ / 前後空白
- 境界値（長さ上限、0、負数、端の日付）
- 重複・衝突（意図的 duplicate と unique 違反は別 tier）
- 参照整合（孤児 FK、循環、削除済み親）
- 文字コード・全角半角・結合文字・機種依存文字
- ソート・表示順に依存するケース（明示ソートキー）

観点の抜けレビューには `qa-multi-perspective`（P4 データ整合・P5 移行）を併用してよい。
詳細: [references/coverage-matrix.md](references/coverage-matrix.md)。

## 生成仕様と manifest（要約）

生成前に **Generation Spec** を短い Markdown または YAML で残す（テンプレ:
[references/generation-spec.md](references/generation-spec.md)）。

manifest には最低限:

- `tier`, `seed`, `row_count`（テーブル別）
- 生成スクリプトパスとコミット SHA（またはバージョン）
- 出力ファイルの checksum
- 検証コマンド 1 行

## 完了の定義

- 要件で指定された tier の行数・グループ比率が満たされている
- カバレッジ行列の必須行がすべてデータ上で追跡可能（行 ID またはコメント列）
- 不変条件検証が exit 0
- manifest があり、README または skill-memory に再現手順がある
- `negative` データは正データとパス・ファイル名で混在しない

## メモ

運用で得た知見は [references/skill-memory.md](references/skill-memory.md) に 1 行ずつ追記する。

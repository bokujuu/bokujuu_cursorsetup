# 併用ツール・定番メソッド

本 skill は **設計層**（tier・三軸・カバレッジ・Generation Spec・manifest）を担う。
実装・出力は環境に応じて次の定番メソッド／ツールと**併用**する。取込用の **CSV / JSON**
が主成果物のとき、設計（本 skill）→ 生成（併用ツール）→ 検証（verify + manifest）の順を守る。

## 定番メソッド（パターン）

| メソッド | 向く場面 | CSV/JSON 取込との関係 | 本 skill との接続 |
|----------|----------|------------------------|-------------------|
| **Static fixture** | smoke・アンカー行・スナップショット回帰 | Git 管理の `.csv` / `.json` をそのまま取込 | `smoke` tier のアンカーを静的ファイルで固定し、dev はスクリプトで拡張 |
| **Seeded generation** | dev / stress・CI 再現 | 生成結果を CSV/JSON に書き出して取込 | Generation Spec の `master_seed`・`frozen_clock` と一致させる |
| **Factory / Builder** | リレーション・上書き可能な 1 行 | バッチ書き出しで CSV/JSON 化 | グループ配分は spec で決め、factory はグループ内の変動のみ |
| **Object Mother** | 説明しやすい代表シナリオ数件 | 小さな JSON を手元に置く | アンカー行・カバレッジ行列の「代表 1 件」と対応づける |
| **Negative fixture 分離** | バリデーション・エラー表示 | `_invalid.csv` / `negative/` を別パス | `negative` tier。正データとファイル名・ID 空間を分ける |

**使い分けの原則**

- 回帰ゲート（CI）→ 決定的（seed 固定 or 静的 fixture）
- 探索的 QA → ランダム可だが自動ゲートには入れない
- 取込パイプラインの入力は **常にファイルパス + manifest** で追跡可能にする

参照: [ArchMan — fixtures / factories / synthetic](https://archman.dev/docs/testing-strategy/test-automation/test-data-fixtures-synthetic-data)、
[Elysiate — deterministic CSV](https://www.elysiate.com/blog/deterministic-csv-for-tests-seeds-timestamps-and-ids)。

## 併用ツール 1 — factory_boy + Faker（seed 固定）

**いつ選ぶ**: Python 環境があり、スクリプトで CSV/JSON を生成する。ドメイン固有の列・FK・
状態ごとの上書きをコードで持ちたい。`htmlPCAFmock` / `utf_ken_all` 型の**自前 gen スクリプト**
と相性が良い。

| 項目 | 内容 |
|------|------|
| 公式 | [factory_boy](https://factoryboy.readthedocs.io/)、[Faker](https://faker.readthedocs.io/) |
| 出力 | `factory` で組んだオブジェクトを `csv.DictWriter` / `json.dump` で書き出し |
| 決定性 | `Faker.seed(master_seed)` と `random.seed(master_seed)` を spec と同値に固定 |
| 本 skill との役割分担 | **本 skill**: tier・グループ件数・アンカー ID・カバレッジタグ / **factory_boy**: 行の組み立て・SubFactory・Trait |
| 詳細 API | repo-local 化は `implement-with-practices`（グローバルには API 手順を重複しない） |

### 接続パターン（CSV/JSON 取込向け）

1. Generation Spec でグループ件数とアンカー行を確定する。
2. アンカーは `factory` の `Trait` または固定 dict で生成し、ID を不変にする。
3. 残り行は `factory.create_batch(n, status=...)` を **グループごと**に呼ぶ（一括乱数は使わない）。
4. 書き出し前に spec の `sort_by` でソート。`utf-8` / `utf-8-sig` / 改行は spec に明記。
5. manifest に `seed`・行数・checksum を記録する。

```python
import random
from faker import Faker
import factory

FAKE = Faker("ja_JP")
Faker.seed(42)
random.seed(42)

class RequestFactory(factory.Factory):
    class Meta:
        model = dict

    id = factory.Sequence(lambda n: f"AR-{n:05d}")
    status = "approved"
    title = factory.LazyAttribute(lambda o: FAKE.sentence(nb_words=4))

# グループ配分は spec から読む — 例: submitted 24 件
rows = [RequestFactory(status="submitted") for _ in range(24)]
```

**注意**

- `factory.Sequence` は並列 worker で衝突しうる。pytest-xdist 等では worker オフセットまたは UUID を検討。
- Faker の出力は **パッチバージョンで変わりうる**。期待値をハードコードするなら Faker 版を pin する。
- ビジネス不変条件（合計＝明細和など）は factory 生成後に assert する。

## 併用ツール 2 — lifelike-synthetic-data-generator

**いつ選ぶ**: スキーマ駆動で CSV/JSON/NDJSON/SQL を一括出力したい。locale・分布（population_model）・
カスタム regex 形式を **config JSON** で持ち、**コンテキスト内捏造ではなく CLI** で生成したいとき。

| 項目 | 内容 |
|------|------|
| リポジトリ | https://github.com/jovd83/lifelike-synthetic-data-generator |
| 実行 | `python scripts/generate_data.py --config path/to/config.json` |
| 検証のみ | `--validate-only` で config を先に検証 |
| 決定性 | config に `"seed"` を必須（無いと非決定的とみなす） |
| 本 skill との役割分担 | **本 skill**: tier・カバレッジ行列・manifest / **lifelike**: フィールド型・locale・分布・ファイル出力 |

### 接続パターン

1. 本 skill の Generation Spec を書く（tier・グループ・invariants）。
2. lifelike の [schema-config](https://github.com/jovd83/lifelike-synthetic-data-generator/blob/main/references/schema-config.schema.json)
   に合わせて config を起こす。`row_count`・`seed`・出力形式は spec と一致させる。
3. `--validate-only` → 生成 → stdout の JSON summary と manifest を突合。
4. 分布が「population-representative」のときだけ lifelike の `population_model` を使う。
   それ以外は本 skill のグループ配分を優先し、過剰な統計主張をしない。
5. ドメイン固有（承認状態・PCAF 列名）は config / custom_formats の**拡張**として repo-local に置く。

**注意**

- 大規模データをモデルコンテキストに載せない（skill 側 guardrail と同趣旨）。
- 日本語 locale・業務キーはプロジェクトで config をメンテする。global skill には同梱しない。

## 選定の目安

| 条件 | 第一候補 |
|------|----------|
| 既存 Python gen スクリプト・COM ビルド前処理 | factory_boy + Faker |
| スキーマ JSON から素早く CSV/JSON 大量出力 | lifelike-synthetic-data-generator |
| smoke のみ・数行 | Static fixture（手書き CSV/JSON） |
| 壊した取込例 | Static negative または専用 factory Trait |
| ライブラリ API の深い手順 | `implement-with-practices` で repo-local skill |

## 環境制約

| 制約 | 対処 |
|------|------|
| Python / pip 不可 | Static fixture + スプレッドシート export。設計（本 skill）は同じ |
| オフライン | lifelike はバンドル script。Faker はローカル install 済み前提 |
| Windows COM ビルドのみ | 生成は Python、取込は CSV 経由 — `excel-deliverable-quality` と併用 |
| Cursor Cloud（COM なし） | openpyxl 経路でも **入力 CSV/JSON の設計手順は同一** |

## 完了時チェック（併用時）

- [ ] 採用ツール名とバージョン（または commit）を manifest に記載した
- [ ] 出力が取込側の期待パス・encoding・列順と一致する
- [ ] spec の tier・seed・行数と実ファイルが一致する
- [ ] 本 skill の不変条件 verify を通した

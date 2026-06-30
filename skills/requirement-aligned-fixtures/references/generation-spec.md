# Generation Spec と manifest

生成コードを書く**前**に、人間が読める短い spec を残す。repo によって
`fixtures/specs/<name>.md` や `docs/fixtures/<name>.yaml` 等に置く。

## Generation Spec テンプレート

```yaml
# fixture: approval_requests_dev
version: 1
tier: dev
purpose: 日常開発用。smoke のアンカーを含み、承認済みが多数。

master_seed: 42
frozen_clock: "2026-06-01T09:00:00+09:00"

outputs:
  - path: fixtures/data/approval_requests_dev.csv
    format: csv
    encoding: utf-8
    newline: lf
    sort_by: [id]

tables:
  - name: approval_requests
    row_count: 120
    includes_smoke_anchors: true
    groups:
      - key: status=draft
        count: 12
      - key: status=submitted
        count: 24
      - key: status=returned
        count: 12
      - key: status=approved
        count: 72
    anchors:
      - id: AR-ANCHOR-DRAFT
        tags: [smoke, status_draft]
      - id: AR-ANCHOR-MAXTITLE
        tags: [smoke, str_max_length]
    variation:
      pool: fixtures/pools/person_names.txt
      fields:
        amount: { type: int, min: 1000, max: 500000, per: group }

invariants:
  - unique: [id]
  - fk: { child: requester_id, parent: fixtures/data/users_smoke.csv#id }
  - rule: "amount >= 0 for tier != negative"

verification:
  - python scripts/verify_fixtures.py --tier dev
```

## manifest テンプレート（生成後）

`fixtures/manifest.json` または spec 末尾に追記:

```json
{
  "fixture": "approval_requests_dev",
  "tier": "dev",
  "seed": 42,
  "generated_at": "2026-06-30T12:00:00Z",
  "generator": "scripts/gen_approval_fixtures.py",
  "git_sha": "optional",
  "files": [
    {
      "path": "fixtures/data/approval_requests_dev.csv",
      "sha256": "...",
      "row_count": 120
    }
  ],
  "verify_command": "python3 scripts/verify_fixtures.py --tier dev"
}
```

## 実装の原則

1. **Spec が SoT** — ハードコードされた件数は spec から読むか、spec と同期する定数ブロックにまとめる。
2. **アンカーはコード内の明示リスト** — コメント `ANCHOR: reason` を付ける。
3. **ビジネスルールは二重チェック** — 生成時 assert + verify スクリプト。
4. **LLM 生成を使う場合** — スキーマ検証（Pydantic 等）と不変条件検証の両方を通す。失敗時はリトライか破棄。

## 決定性のための実装スニペット（Python）

```python
import hashlib
import random

def derive_seed(master: int, *parts: str) -> int:
    h = hashlib.sha256(f"{master}|{'|'.join(parts)}".encode()).hexdigest()
    return int(h[:8], 16)

def rng_for_row(master: int, group: str, row_index: int) -> random.Random:
    return random.Random(derive_seed(master, group, str(row_index)))
```

日時は `frozen_clock` からのオフセット日のみ使い、`datetime.now()` を直接使わない。

## ソートと CSV

- 書き込み前に **明示 sort**（複数キーは仕様順）。
- `utf-8-sig` が必要かどうかを spec に書く（Excel 取込向け）。
- 数値コード列は `dtype=str` 前提なら生成時からゼロ埋め文字列にする（`utf_ken_all` 系）。

## 再生成手順（README 用 1 行）

```text
FIXTURE_SEED=42 python3 scripts/gen_approval_fixtures.py --tier dev && python3 scripts/verify_fixtures.py --tier dev
```

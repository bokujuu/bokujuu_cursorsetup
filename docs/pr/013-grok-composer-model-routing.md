# PR design note: Grok × Composer model routing

Updated: 2026/07/09 03:00

## Purpose

Grok 4.5 をメイン、Composer 2.5 を併用する前提で、本 repo の skill / ループ設計を
**モデル非依存のまま**保ちつつ、Composer 固定だった箇所だけ軽く直す。

## Verdict

- **大規模な skill 書き換えは不要**（手順・検証・SoT 委譲は共通）
- **追加**: `docs/model-routing.md`（使い分け SoT）
- **軽微**: loop 既定は Composer のまま、Grok 上書きを文書化・`ralph.ps1 -Model` 配線
- **軽微**: `fable-style-reasoning` の Composer 専用表記を Cursor 共通へ

## Related updates

- `docs/model-routing.md` / `docs/rule-index.md` / `docs/loop-engineering.md`
- `MANIFEST.md`
- `templates/loop-orchestration/`（README, run-once, ralph.ps1/sh/mjs）
- `skills/fable-style-reasoning/` + registry
- `skills/ralph-loop/references/operational-guide.md`
- `scripts/verify_loop_kit.py`

## Verification

```bash
bash scripts/install.sh
python3 scripts/verify_repo_setup.py
python3 scripts/verify_loop_kit.py
bash -n scripts/install.sh
python3 -m py_compile scripts/verify_loop_kit.py
```

## Deferred

- IDE ピッカーの正式 slug 一覧が製品 docs で安定したら表を追従
- Grok 固有の振る舞い差が実運用で固まったら skill-memory → model-routing へ昇格

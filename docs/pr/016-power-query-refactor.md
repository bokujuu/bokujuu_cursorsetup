# PR 設計: power-query-refactor

更新: 2026/07/27 10:14

## 目的

Power Query M の編集判断（挙動保持・配置・notes・Buffer）を global skill として配布する。  
特定リポの COM export/import や案件固有診断は含めない。

## 配置判断

| 候補 | 判定 |
|------|------|
| global `skills/power-query-refactor` | **採用** — 複数リポで再利用できる編集原則 |
| user-rules | 不適 — 常時適用の技術手順にしない |
| templates のみ | 不十分 — install でエージェントに載せたい |
| knowledge-base のみ | 不十分 — 起動可能な手順として配布したい |

## 三つの柱

1. 編集の基本方針（SKILL 本体）
2. notes（`references/notes.md`）
3. Buffer / フォールディング（`references/buffer-and-folding.md`）

## 非目標

- `powerquery_refactor` のスクリプト群の移植
- 絶対パス・作業痕跡の持ち込み
- Excel 帳票品質（`excel-deliverable-quality` と重複させない）
- Buffer をキャッシュ／高速化保証として教えること（誤用防止のため「第二手段＋検証必須」）

## 検証

```bat
.\scripts\install.ps1
python scripts\verify_repo_setup.py
python scripts\verify_loop_kit.py
```

レビュー反映（2026/07/27）: terra / sol 双方の P1（結果比較の必須化、Buffer の非キャッシュ明示、参照表マージのキー／結合仕様）と P2（description 境界、公開名、notes 言語規約、sources 整理、excel-deliverable-quality 併用、分割時のキャッシュ誤解防止）を本文へ取り込み。再レビュー: terra Approve with nits → nit 反映、sol Approve。
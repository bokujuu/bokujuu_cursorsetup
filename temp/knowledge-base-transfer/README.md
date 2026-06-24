# knowledge-base 転送用パッケージ

本ディレクトリは `bokujuu/knowledge-base` へ手動転送するための staging である。
`bokujuu_cursorsetup` 本体には取り込まない（global skill 非採用の知見化のみ）。

## 転送手順

1. `docs/research/taste-skill-global-suitability.md` を knowledge-base の同パスへコピー
2. 索引を更新（`index-updates.md` 参照）
3. 本 `temp/knowledge-base-transfer/` は転送完了後に削除してよい

## 背景

Cloud Agent が `leonxlnx/taste-skill` の global suitability を検討。
knowledge-base への直接 push は権限不足のため、本 repo 経由で転送する。

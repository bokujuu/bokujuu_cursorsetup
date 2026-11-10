# PR 020 — imozuru（原文取込）

更新: 2026/11/10 22:58

## 目的

[MaryCache/imozuru](https://github.com/MaryCache/imozuru) を、スキル本文は改変せずグローバル skill として同梱する。知らない分野を用語・人・媒体からたどり、原文を `~/research/<話題>/` に保存する。

## 採用判断

- **入れる**: `skills/imozuru/` の原文（`SKILL.md`、`scripts/`、`references/theory.md`、`assets/`）と MIT の `LICENSE`
- **入れない**: 本文の翻訳や Cursor 向けの書き換え。upstream の `tests/` と `examples/`。抜き書きの形は `SKILL.md` に既にある
- **検証側だけ**: `description: |` を `scripts/verify_repo_setup.py` が読めるようにする。本文は変えない

## 既存との境界

| 既存 | 境界 |
|------|------|
| `abstract-source-patterns` | 外部ソースをこのリポジトリへ入れるかの判定。imozuru は分野の原文を集める調査 |
| `japanese-technical-writing` | 技術文書を書く。imozuru は調べている間は要約せず、止めたあと `digest.html` を作る |
| `md-html-visual-doc` | 比較や手順の視覚ドキュメント。imozuru の HTML は抜き書きと調査の履歴 |
| `cursor-session-doc` | ローカルの会話履歴。imozuru は Web 上の原文 |

検索役のサブエージェントが使えないときは、upstream の手順どおり親が同じ検索を順に行う。

## 更新手順

本文の更新は `python scripts/update_imozuru.py` だけを使う。本家 `main` を shallow clone し、`skills/imozuru/` を置き換える。残す手元差分は upstream 直下の `LICENSE` と、取得コミットを書いた `references/sources.md` だけ。`tests/` と `examples/` は同梱しない。

取り直したあとは `.\scripts\install.ps1` と `python scripts\verify_repo_setup.py`。差分はこのリポジトリへ commit し、その commit が配布される写しになる。

## 検証

```bat
.\scripts\install.ps1
python scripts\verify_repo_setup.py
python scripts\verify_loop_kit.py
```

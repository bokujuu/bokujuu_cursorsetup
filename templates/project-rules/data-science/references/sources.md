# data-science template — 出典と抽象化

## 一次ソース

- [atsushi-green/ds-ai-coding-skills](https://github.com/atsushi-green/ds-ai-coding-skills)

## 取り込んだパターン

- 薄い `AGENTS.md` + タスク別 skill ルーター
- `docs/agent/` をプロジェクト知識の SoT
- raw / 機密の verify 3 本（コミット前ゲート）

## 除去した固有要素

- uv / polars / mypy / ruff の固定コマンド列
- Copilot `.github/skills` と Claude `.claude/skills` の二重ツリー全文
- 10 種 DS スキルの実装（各プロジェクトで `skill-lifecycle` / `implement-with-practices` から生成）

## 配置理由

DS はパッケージマネージャ・データレイアウト・指標定義がプロジェクトごとに異なる。**project-rules** にルーターと安全規約だけ置き、スキル本文は repo-local で育てる。

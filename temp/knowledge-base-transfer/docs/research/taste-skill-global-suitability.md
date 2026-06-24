---
title: taste-skill の global suitability 判定（bokujuu_cursorsetup 非採用）
tags:
  - research
  - ai
  - cursor
  - github
  - reference
created: 2026-06-24
updated: 2026-06-24
status: active
type: research
summary: leonxlnx/taste-skill を bokujuu_cursorsetup グローバル skill として採用しない判断。汎用人間工学ではなく Web フロント特化である根拠と、将来の配置指針。
source_repo: bokujuu/bokujuu_cursorsetup
source_context: Cloud Agent による検討セッション（2026-06-24）
---

# taste-skill の global suitability 判定（bokujuu_cursorsetup 非採用）

## Question

[leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) は、ビジュアル品質・人間工学・ユーザーの視線・動線といった**汎用デザイン概念**として `bokujuu_cursorsetup` のグローバル `skills/` に入れる価値があるか。  
それとも **Web フロントエンド固有の実装 skill** に留まるか。

## 背景

- `taste-skill` は AI が生成しがちな「スロップ」な UI を避け、LP・ポートフォリオ・リデザイン向けに高品質なフロントを実装させる Agent Skills のバンドル。
- `bokujuu_cursorsetup` は複数 repo で副作用の少ない**グローバル設定**のみを配布する。不適合でも配置判断に有用な知見は [knowledge-base](https://github.com/bokujuu/knowledge-base) へ記録する（[global-suitability-and-knowledge-capture](https://github.com/bokujuu/bokujuu_cursorsetup/blob/main/docs/review/global-suitability-and-knowledge-capture.md)）。
- 採用判断の最重要軸は「**媒体横断の人間工学・動線として抽象化されているか**」であり、単なる美的ルールや特定スタックの実装手順ではないこと。

## 判断

| 項目 | 結論 |
|------|------|
| `bokujuu_cursorsetup` グローバル `skills/` への採用 | **しない** |
| knowledge-base への知見化 | **する**（本ノート） |
| 将来フロント案件で使う場合 | upstream を `npx skills add` で直接入れる、または `templates/project-skills/` へ案件ローカル展開 |

## global に入れない理由

### 1. 汎用の人間工学・動線 skill ではない

`taste-skill` の主目的は **anti-slop の Web フロント美学と実装**である。次のような汎用 UX フレームワークとしては書かれていない。

- 視線誘導・スキャンパス（F/Z パターン等）の体系
- タスクフロー・ユーザージャーニー設計
- 媒体非依存の「次に何を見て何をするか」の抽象原則

メイン skill（`design-taste-frontend`）冒頭で適用範囲が明示されている。

- **対象**: landing page、portfolio、redesign、editorial
- **対象外**: dashboard、data table、multi-step product UI

Excel や帳票の「入力 → 集計 → 判定」の動線設計は想定外。

### 2. フロントエンド特定技術へのバイアスが強い

デフォルトスタックは **React / Next.js / Tailwind v4 / Motion（旧 Framer Motion）/ GSAP**。本文には Tailwind クラス名、`className`、`useState` 禁止、GSAP の **tsx コードスケルトン**が含まれる。

README では React / Vue / Svelte 対応を謳うが、実体は Web マーケページ向けの実装規約が中心。`redesign-skill` は既存 CSS フレームワークとの共存を述べるものの、監査項目は Web UI（nav、hero、hover、scroll）に寄る。

### 3. Excel 等への転用不可

`excel-deliverable-quality` は「どこを触る／触らないか」「入力 → 集計 → 判定 → メタの順」など**人間工学を媒体に落とした** skill である。  
`taste-skill` には表計算・帳票・入力順序・役割の色分け等の記述がなく、**同じ抽象化レベルにはない**。

### 4. グローバル install の副作用

`bokujuu_cursorsetup` の `install.sh` は `skills/` 配下を**全件** `~/.codex/skills/` にコピーする。フロント特化 skill を常駐させると、Excel / Python / インフラ作業でも UI ルールが誤発火しうる。

### 5. バンドル規模と保守

10 本以上の skill（実装系・画像生成系・スタイル variant）、英語のみ、メイン v2 は experimental。upstream の追従コストが `japanese-*` 取込みより高い。

## knowledge-base に残す理由

- 今後の **global / local / template / 直接 install** の配置判断の具体例になる。
- 「汎用デザイン skill に見えるが、実はドメイン特化である」という**誤採用の防止**に使える。
- ユーザーが重視する判定軸（視線・動線・人間工学の汎用性）を、外部 skill 評価のチェックリストとして再利用できる。

## 再利用できる観点

### 外部 skill を評価するときのチェックリスト

1. **抽象原則か、実装・媒体固有か** — SKILL 本文の過半数が何について書かれているか。
2. **動線・人間工学が主目的か** — タスク順序・視線・誤操作防止が体系化されているか、それとも美的 anti-pattern か。
3. **対象外の明示** — `description` と本文で適用外が書かれているか。
4. **グローバル install の副作用** — 非対象 repo で誤トリガーしないか。
5. **既存 skill との境界** — 例: 構造可視化は `system-structure-viz`、Excel 人間工学は `excel-deliverable-quality`。

### taste-skill の中で転用しうる断片（ただし skill としては不採用）

- visual hierarchy、WCAG コントラスト、フォーカス・キーボード
- loading / empty / error 状態
- アニメーションの目的付け（hierarchy / feedback / state transition）
- ブリーフ推論 → デザイン言語選択 → ダイヤル調整、という**メタ構造**（媒体を Web に限定すれば参考になる）

これらは **Excel 用の汎用原則 skill を自作する際の着想**にはなるが、`taste-skill` をそのまま転用する根拠にはならない。

### 将来フロント案件で使う場合の推奨配置

| 方針 | 内容 |
|------|------|
| A. 直接 install（推奨） | `npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"` |
| B. プロジェクトローカル | スタイル variant（minimalist / brutalist 等）を `templates/project-skills/` 相当へコピー |
| C. グローバル常駐 | **非推奨** |

## Findings（調査サマリ）

### リポジトリ概要

- **URL**: https://github.com/leonxlnx/taste-skill
- **ライセンス**: MIT
- **構成**: `skills/` 配下に複数 SKILL（実装系 + 画像生成系）

| 種類 | 例（install name） | 出力 |
|------|-------------------|------|
| 実装系 | `design-taste-frontend`, `redesign-existing-projects`, `minimalist-ui` | コード |
| 画像系 | `imagegen-frontend-web`, `imagegen-frontend-mobile`, `brandkit` | 参照画像 |
| 補助 | `image-to-code`, `full-output-enforcement` | ワークフロー |

### 汎用性の整理

| 領域 | 評価 |
|------|------|
| LP / ポートフォリオ / サイト UI 改善 | ◎ |
| React 等 Web フロント（マーケ寄り） | ○ |
| ダッシュボード・業務 UI・表形式 UI | ×（skill 自身が除外） |
| Excel / 帳票 / 資料 | × |
| 媒体横断の人間工学・動線 | ×（主目的ではない） |

## Evidence

- メイン skill 先頭: landing / portfolio / redesign が対象、dashboard / data table / multi-step product UI は対象外。
- Section 3 デフォルト: React or Next.js、Tailwind v4、Motion、GSAP コード例。
- `redesign-skill`: 「Works with any CSS framework or vanilla CSS」だが監査は Web サイト向け。
- `bokujuu_cursorsetup` の `excel-deliverable-quality`（`references/design-and-layout.md`）: 入力順・役割色・タッチ可否が中心 — 対照的に taste-skill は Web LP 構成と anti-slop が中心。

## Interpretation

`taste-skill` は **高品質な Web フロント（主にマーケ・ポートフォリオ）向けのドメイン skill** として優れているが、ユーザーが求める **「視線・動線・人間工学の汎用概念」skill ではない**。  
`bokujuu_cursorsetup` には入れず、必要時は upstream を直接使うかプロジェクトローカルに置くのが、global suitability 方針と整合する。

汎用の人間工学 skill が必要なら、Excel で既に実践している「役割・順序・誤入力防止」を抽象化した**自前 skill** の検討が筋が良い（本ノートはその判断材料）。

## Open Questions

- フロント案件の頻度が増えた場合、`templates/project-skills/` に taste-skill の**サブセット 1 本だけ**同梱する価値があるか。
- 媒体横断の「視線・動線・人間工学」skill を `bokujuu_cursorsetup` に新規作成する場合、`excel-deliverable-quality` と `system-structure-viz` の境界をどう切るか。

## 関連

- Source repo: [bokujuu/bokujuu_cursorsetup](https://github.com/bokujuu/bokujuu_cursorsetup)
- 判定手順: [global-suitability-and-knowledge-capture.md](https://github.com/bokujuu/bokujuu_cursorsetup/blob/main/docs/review/global-suitability-and-knowledge-capture.md)
- 役割分担: [bokujuu-cursorsetup-integration.md](https://github.com/bokujuu/knowledge-base/blob/main/docs/ai/bokujuu-cursorsetup-integration.md)
- 配置検討の先例: [agent-docs-verbalization-research.md](https://github.com/bokujuu/knowledge-base/blob/main/docs/research/agent-docs-verbalization-research.md)
- 対照的な skill（媒体特化・人間工学中心）: [excel-deliverable-quality SKILL.md](https://github.com/bokujuu/bokujuu_cursorsetup/blob/main/skills/excel-deliverable-quality/SKILL.md)
- 調査対象: [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill)

## References

- https://github.com/leonxlnx/taste-skill
- https://github.com/leonxlnx/taste-skill/blob/main/skills/taste-skill/SKILL.md
- https://github.com/leonxlnx/taste-skill/blob/main/skills/redesign-skill/SKILL.md

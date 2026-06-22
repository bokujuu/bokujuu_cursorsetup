# 出典

## 主たる設計源 — ユーザー運用リポジトリ

本スキルの配置・配色・ビルド・検証の規約は、ユーザー自身の運用リポジトリで実際に確立した方式を、
特定業務に依存しない形へ一般化したもの（文章は新規に書き起こし）。

- `htmlPCAFmock`（COM でビルドする運用 Excel・メール承認版）— https://github.com/bokujuu/htmlPCAFmock
  - 一般化して採用した方針:
    - **スクリプトで生成し `.xlsm` は手編集しない**／`.xlsm` を Read しない／座標・定数を集約
    - **セル役割の異色化**（人間が入力する成果物で重要）と**条件付き書式による状態表現**。具体の
      カラーコード（入力 `(255,255,204)`／数式 `(242,242,242)` など）は**既定例**で固定規定ではない
    - **印刷規律**（印刷配布時のみ・`PrintArea` 明示・`FitToPages=1`・向き/余白固定）は**ケース依存**
    - **very hidden で内部データ（素データ・正解値・ルーティング）を隔離**
    - **安全ビルド**（temp → COM 検証 → 成功時のみ置換）
    - **VBA は Core + Silent**（COM 経路にモーダル UI を出さない）・`*.bas` を UTF-8 で版管理し cp932 Import
    - **検証は全件完走・終了コードで集約失敗**・ログは `[SUMMARY]`/`[FAIL]` 優先
    - リボンは **imageMso のみ**
- `utf_ken_all`（取込用データ整形）— https://github.com/bokujuu/utf_ken_all
  - 一般化して採用した方針: **確定値でなく数式／ハードコード値の出典注記**（システム・日付・参照・URL）、
    取込用 CSV の文字コード・改行・ゼロ落ち対策（`dtype=str`）。
- `excel-addins`（`.xlam` 統合アドイン）— https://github.com/bokujuu/excel-addins
  - 一般化して採用した方針（[path-settings-xlam.md](path-settings-xlam.md)）:
    - **path-settings xlsx テーブル → ビルド時 `PathConfig` VBA 注入**（実行時に xlsx を読まない）
    - ListObject 外追記はビルドで無視される — テーブル範囲リサイズ必須
  - RibbonX 注入・OOXML 正規化は別トピック（knowledge-base [ribbonx-xlam-build](https://github.com/bokujuu/knowledge-base/blob/main/docs/technology/excel/ribbonx-xlam-build.md)）

## 着想元 — Anthropic `xlsx` スキル

- リポジトリ: https://github.com/anthropics/skills
- スキル: https://github.com/anthropics/skills/blob/main/skills/xlsx/SKILL.md（確認日 2026/06/16 JST）
- ライセンス上の扱い: upstream の `xlsx` は **Proprietary**（`LICENSE.txt` に全条件）。そのため本スキルは
  **本文を一切コピーしていない**。著作物でない一般的な実務規約（数式エラーゼロ、確定値でなく数式、
  数値・桁の表記、ハードコードの出典注記、納品前検証）という**考え方のみ**を参照した。
- upstream は pandas/openpyxl/LibreOffice 前提で、ユーザー運用（COM Automation 第一）には合わない。
  そこで実行系を **COM/win32com を第一**、openpyxl + LibreOffice をヘッドレス代替として再構成し、
  COM の API 手順は対象リポの `templates/project-rules/excel/excel-com-automation.mdc` に委譲した。

## himadajin 系スキルとの違い

himadajin 由来の日本語スキル（`japanese-doc-review` 等）は upstream 準拠の取込だが、本スキルは
**ユーザー運用リポの方式を一般化した独自実装**であり、upstream のコピーではない。

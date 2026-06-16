# 出典

- 着想元: Anthropic `skills` リポジトリの `xlsx` スキル
  - リポジトリ: https://github.com/anthropics/skills
  - スキル: https://github.com/anthropics/skills/blob/main/skills/xlsx/SKILL.md
  - 確認日: 2026/06/16（JST）
- ライセンス上の扱い: upstream の `xlsx` は **Proprietary**（`LICENSE.txt` に全条件）。
  そのため本スキルは**本文を一切コピーしていない**。著作物でない一般的な実務規約
  （数式エラーゼロ、確定値でなく数式を持つ、数値・桁・色の表記規約、ハードコードの出典注記、
  納品前検証）という**考え方のみ**を参照し、文章はすべて新規に書き起こした。
- 改変・再構成: ユーザー運用（COM Automation 第一）に合わせ、実行系を COM/win32com を第一、
  openpyxl + LibreOffice をヘッドレス代替として再構成した。COM の API 手順は
  `templates/project-rules/excel/excel-com-automation.mdc` を正とし重複させない。
- himadajin 由来の日本語スキル（`japanese-doc-review` 等）と異なり、本スキルは upstream 準拠の
  取込ではなく、原則のみを参照した独自実装である点に注意する。

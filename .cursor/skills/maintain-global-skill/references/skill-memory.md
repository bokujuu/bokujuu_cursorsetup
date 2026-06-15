# skill-memory — maintain-global-skill

- 2026/06/15 13:00: 初版。過去セッションでは skill-lifecycle / structure-viz / Japanese skills 追加時に「validation と PR」「global + ローカル配置」「sources に upstream URL」を繰り返し指示。PR 前の `verify_*` 実行を必須化した。
- 2026/06/15 13:50: PR レビュー指摘 — verify は install 後に実行。`verify_repo_setup.py` のパスは Path 正規化（Linux 対応）。registry は `python3` 表記。

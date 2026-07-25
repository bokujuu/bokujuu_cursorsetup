# PR design note: slide-narration-video

Updated: 2026/07/25 17:37

## Purpose

全画面スライド＋合成音声ナレーションの解説動画を設計・制作するグローバル skill。
Marp スライド、VOICEVOX（既定）／Irodori-TTS（任意）、Remotion と Motion Canvas の役割分担、発話と画面注釈の同期、スライド間の認知的な「間」を扱う。

本更新では次の配置・読み品質ゲートを規範として追加する（検査スクリプト実装は後続可）。

1. 文字はみ出し防止（工程 2.5）
2. 埋め込み画像のアスペクト比維持
3. VOICEVOX 向け英語・固有語の TTS 直前読み正規化（工程 4.5）

## Source

| Item | Value |
|------|-------|
| Origin | ローカル完成版 `%USERPROFILE%\.codex\skills\slide-narration-video\` |
| Local slug | `slide-narration-video` |
| Upstream | なし（自作。執筆規範は既存 skill に委譲） |
| Empiric check | `d:\Obsidian\temp\gigatoken-video-v2\`（更新 skill でクリーンエージェント再生成・親監査合格） |

## Design decisions

| Item | Decision |
|------|----------|
| Placement | `skills/`（複数 repo で再利用可能な制作フロー。global suitability OK） |
| Dependencies | 相対パスで `../japanese-technical-writing/SKILL.md` と `../cognitive-rhythm-writing/SKILL.md` を必須参照（install 後の並置を前提） |
| Stack default | Marp → Remotion（± Motion Canvas）→ VOICEVOX（冥鳴ひまり）。Irodori-TTS は代替。ffmpeg 結合も可 |
| Layout QA | `references/slide-layout-qa.md`。PNG 目視ゲート必須。`overflow:hidden` / 全面自動縮小は採らない |
| Image aspect | `max-width:100%; height:auto;`。両軸固定押しつぶし禁止。`object-fit:contain` は固定枠時のみ |
| TTS reading | `narration` は SoT。辞書（例: `pronunciation.yml`）で TTS 直前変換。未知英字の自動ローマ字推測はしない |
| Ops files | `agents/openai.yaml` / `references/*` / `references/skill-memory.md` |
| Out of scope | Premiere 等 GUI 編集前提、左右分割テンプレ常設、Pixi/Three デモ中心、機械検査スクリプト本体（別 PR） |

## Related updates

- `MANIFEST.md` / `docs/rule-index.md` / `INSTALL.md`
- `.codex/practice-registry.json`（draft）
- 新規: `references/slide-layout-qa.md`, `references/tts-pronunciation.md`

## Verification

```bash
.\scripts\install.ps1
python scripts\verify_repo_setup.py
python scripts\verify_loop_kit.py
```

実動画検証（任意・本 PR 外成果物）:

- 更新 skill を渡したクリーンエージェントで Gigatoken 解説を再生成
- フロー図（Mermaid 先レンダ）＋比較図を含め、端欠け・歪み・読み辞書を親が監査

## Deferred

- Remotion / Motion Canvas のプロジェクト雛形テンプレは本 skill に含めない（必要なら別 PR）
- PNG 画素／DOM 矩形の機械検査スクリプト、共通読み辞書パッケージは別 PR
- Irodori-TTS の詳細手順は `references/tts-and-stack.md` の範囲に留める
- VOICEVOX `/user_dict_word` 永続依存は採らない（都度投入は拡張可）

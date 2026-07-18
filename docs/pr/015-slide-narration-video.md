# PR design note: slide-narration-video

Updated: 2026/07/18 16:53

## Purpose

全画面スライド＋合成音声ナレーションの解説動画を設計・制作するグローバル skill。
Marp スライド、VOICEVOX（既定）／Irodori-TTS（任意）、Remotion と Motion Canvas の役割分担、発話と画面注釈の同期、スライド間の認知的な「間」を扱う。

## Source

| Item | Value |
|------|-------|
| Origin | ローカル完成版 `%USERPROFILE%\.codex\skills\slide-narration-video\` |
| Local slug | `slide-narration-video` |
| Upstream | なし（自作。執筆規範は既存 skill に委譲） |

## Design decisions

| Item | Decision |
|------|----------|
| Placement | `skills/`（複数 repo で再利用可能な制作フロー。global suitability OK） |
| Dependencies | 相対パスで `../japanese-technical-writing/SKILL.md` と `../cognitive-rhythm-writing/SKILL.md` を必須参照（install 後の並置を前提） |
| Stack default | Marp → Remotion（± Motion Canvas）→ VOICEVOX（冥鳴ひまり）。Irodori-TTS は代替 |
| Ops files | `agents/openai.yaml` / `references/*` / `references/skill-memory.md` |
| Out of scope | Premiere 等 GUI 編集前提、左右分割テンプレ常設、Pixi/Three デモ中心 |

## Related updates

- `MANIFEST.md` / `docs/rule-index.md` / `INSTALL.md`
- `.codex/practice-registry.json`（draft）

## Verification

```bash
.\scripts\install.ps1
python scripts\verify_repo_setup.py
python scripts\verify_loop_kit.py
```

## Deferred

- Remotion / Motion Canvas のプロジェクト雛形テンプレは本 skill に含めない（必要なら別 PR）
- Irodori-TTS の詳細手順は `references/tts-and-stack.md` の範囲に留める

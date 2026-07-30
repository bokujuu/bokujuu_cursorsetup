# PR 017 — slide-narration-video: Mermaid 改行と静止画高速書き出し

Updated: 2026/07/28 10:20

## Summary

- Mermaid ノード内改行は `\n` ではなく `<br/>`（リテラル `\n` が残る失敗を防止）
- 動きのないスライドショーは ffmpeg 静止画結合を優先し、fps 15 を候補に
- Remotion の concurrency／同時 render による mux 破損と、書き出し後の健全性チェックを明記

## Test plan

- [ ] `MANIFEST.md` と `docs/rule-index.md` を確認・更新（skill 説明の追従）してから skill references を変える
- [ ] `skills/slide-narration-video` の SKILL / figures-and-math / tts-and-stack / skill-memory を通読し、方針が矛盾していない
- [ ] （任意）小さな `.mmd` で `\n` vs `<br/>` を `mmdc` 比較し、`<br/>` 側だけ改行されることを確認
- [ ] `.\scripts\install.ps1` を実行する
- [ ] `python scripts\verify_repo_setup.py`（必要なら `python scripts\verify_loop_kit.py`）で検証する
- [ ] README / INSTALL を最終確認する（エントリと手順の齟齬がないこと）

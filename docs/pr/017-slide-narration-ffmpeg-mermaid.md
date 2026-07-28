# PR 017 — slide-narration-video: Mermaid 改行と静止画高速書き出し

## Summary

- Mermaid ノード内改行は `\n` ではなく `<br/>`（リテラル `\n` が残る失敗を防止）
- 動きのないスライドショーは ffmpeg 静止画結合を優先し、fps 15 を候補に
- Remotion の concurrency／同時 render による mux 破損と、書き出し後の健全性チェックを明記

## Test plan

- [ ] `skills/slide-narration-video` の該当 references を通読し、方針が矛盾していない
- [ ] （任意）小さな `.mmd` で `\n` vs `<br/>` を `mmdc` 比較し、`<br/>` 側だけ改行されることを確認
- [ ] `install.ps1` 後にグローバル skill へ反映されることを確認

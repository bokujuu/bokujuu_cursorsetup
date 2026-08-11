# Subtitle typography (display size & symbols)

Updated: 2026/08/11 15:15

字幕の**見た目サイズ**と**記号の書き方**を揃えるための不変条件。  
SoT は `utterances[].narration`。読みは `pronunciation.yml` → `tts_text`（画面に出さない）。

## フォントと光学サイズの原則

- 1080p の既定は解決済みの源真ゴシック P Heavy 48px とし、解像度に比例させる。通常文字、数字、Latin、Unicode 数学記号、MATH_MASK は同じ字幕フォントファイルを共有する。ASCII／数式だけを別フォントへ切り替えることを既定にしない。
- 分類ごとに `font_size * 0.72` のような固定倍率で別サイズのフォントをロードしない。さらに、`SU(2)` の括弧や `v1.2` の x-height を含む**単語全体の bbox をCJK高へ合わせる mask 拡縮も既定にしない**。識別子の長さは折り返し・行幅で処理し、基本ゴシックの native cap／x-height／数字比率を保つ。
- 差が目立つ単一 glyph だけ、同じフォントで一度ラスタライズした component のインク bbox を基準（`第`／`章`／`あ`）と比較し、必要時に glyph mask を等方補正する。補正を行った場合だけ補正後の実インク高／基準高を記録する。測定不能・インク高 1 以下は `scale=1` に戻す。
- `font_size` を span ごとに変えるのではなく、同一フォントの mask を supersample → 補正 → **共通 baseline** へ配置する。`baseline_offset` を保持し、bbox 下端合わせを baseline の代用にしない。通常 span は最終解像度±1px、MATH_MASK は±2px以内を目標とする。
- Matplotlib／LaTeX の既定 math font（DejaVu、Computer Modern 等）を最終字幕へ無調整で混在させない。対応可能なら字幕フォントを mathtext の custom font に設定し、対応できない場合は透明 mask として扱い、通常文字と同じ実インク高・baseline・縁取りへ正規化する。
- インク高は縁取り前の fill alpha mask に対して測定し、最終解像度で `alpha >= 16` の bbox を使う。基準グリフは `第`・`章`・`あ` の各高の中央値とし、外縁・blur・tight canvas の余白を測定値へ含めない。
- custom mathtext でも未収録グリフが DejaVu／Computer Modern へ暗黙 fallback し得るため、解決フォントを検出・記録する。検出不能または別 font なら、明示的 fallback と MATH_MASK の同一正規化経路へ送る。

## 実装契約（レンダラ側）

1. 字幕フォントを解決する処理は行単位で一度だけ実行し、解決した font file と基準サイズをログへ残す。通常 span は `mask, advance, baseline_offset` を返す同一フォントの supersample mask とする。
2. `baseline_offset` を使って行内の最大 ascent／descent から共通 baseline を組み、各 mask をそこへ貼る。mask の下端や tight bbox の下端を baseline の代用にしない。
3. 光学補正は、明示的に選んだ単一 glyph の `target_height / measured_component_height` から mask に対して計算する。通常の Latin 識別子には適用しない。`font_size` の再ロードや、Latin／数字だけに固定 `0.72` を掛ける処理は追加しない。補正した場合は最終解像度 fill alpha（`alpha >= 16`）を再測定し、比率を記録する。
4. 短い単純分数は、意味を保てる slash 表記（例: `\frac{J_1}{\hbar}` → `J1/ℏ`）へ flatten し、通常文字と同じ PLAIN_MASK で描けることを優先する。flatten 不能な `MATH_MASK` は同じ `mask, advance, baseline_offset` 契約に変換してから、通常 span と同じ supersample・縁取り・downsample 経路へ渡す。baseline は mathtext の ascent/depth 等から実測し、式全体を基準高へ押し込むだけにしない。最終 fill mask の上段・下段・stem・分数線を回帰し、内部が添字程度なら明示的な math style または安全な flatten へ切り替える。
5. 未収録 glyph や mathtext fallback を検出できない場合は、未測定のまま合格扱いにせず、明示的な fallback mask と検証ログへ送る。最低限 `font_file`、`resolved_font_file`、`fallback_detected`、`fallback_status`、`verification_basis`、`missing_candidates`、`unknown_commands` を残す。`fallback_status=verified` は、要求TTFへの解決、semantic glyph coverage、custom mathtext slotの一致をすべて記録できた場合だけ許可し、family解決だけでは個別 glyph の fallback 不在を証明しない。

## 分類（描画前）

`$...$` の flatten / mixed 分割を**先**に行い、残った通常テキストだけを span 分類する。  
未処理の `$` に対して全角化や光学補正をかけない。

**分類の優先順（固定）:**

1. raw `$...$` を除外（flatten 成功分は通常テキストへ、失敗分は MATH_MASK）  
2. latin 識別子一塊（`SU(2)`、`v1.2`）→ **同じ基準サイズ**。内部数字を別処理しない
3. 数字 run → 同じ基準サイズ。実インク高が不足する場合だけ mask を小幅補正
4. Greek / `ℏ` 等 → 同じ基準サイズ。実インク高が不足する場合だけ mask を小幅補正
5. 残り（和文・演算子・小数点）→ cjk 基準

| span | 例 | 描画 |
|------|----|------|
| CJK / 演算子 | 漢字・かな・句読点・`(` `/` `·` `×` | 基準サイズ |
| 数字 | `第3章` の `3`、`3.1` の数字、`図28` | 字幕フォントの基準サイズ。単語全体の高さ合わせには使わず、必要なら単一 glyph を測って補正 |
| 数学変数 | 単独 `J` / `i` / `ℏ` / `φ`（flatten 後） | 字幕フォントの基準サイズ。通常文字と同じ baseline／縁取りへ配置 |
| latin 識別子 | `SU(2)`、`API`、`v1.2` | 基準サイズで一塊。原則 scale=1。内部数字を再補正しない |
| MATH_MASK | flatten 不能な `$...$` | 同じ字幕フォントの custom mathtext、または透明 mask を実インク高・component・baseline 正規化 |

**禁止:** 全角数字・全角 Latin を「高さ合わせ」の手段にしない（横幅だけ増え、高さは足りない）。  
**フォールバック:** ink 高さ ≤1、測定失敗、font glyph 不在時は scale=1 と安全な fallback font／mask を使い、未測定の拡大・縮小をしない。fallback font を使った場合は検証ログへ記録する。

### 回帰例

| 入力 | 期待 |
|------|------|
| `第3章` | `3` は同じ基準フォント。必要時だけ mask 補正、第/章 cjk |
| `3.1` | `3`/`1` は同じ基準フォント、`.` cjk |
| `SU(2)` | 一塊を基準サイズ（中の `2` を再補正しない） |
| `v1.2` | 一塊を基準サイズ |
| 単独 `x` / `J` / `ℏ` | 同じ基準フォント、必要時だけ mask 補正 |
| `x×p` | `x`/`p` は同じ基準フォント、`×` cjk |
| `1-(i/ℏ)` | 数字・`i`・`ℏ` は同じ基準フォント、演算子 cjk |
| `\\frac{1}{2}` / `J_z` / `\\sqrt{x}` | raw TeX を先に補正せず、MATH_MASK 化後に実インク高・baseline・advance を正規化 |
| `API` / `Wigner–Eckart` | 一塊を基準サイズ、別 font の固定縮小をしない |
| 2行字幕 | 各行の補正後 advance で再計測し、共通 baseline と行間を保つ |
| `第3章 SU(2) J` | `J` を不要に拡大・縮小せず、`SU(2)` を旧36px相当へ縮小しない |
| `第3章 $\\frac{J_1}{\\hbar}$` | 短い既知分数は `J1/ℏ` へ安全に flatten。flatten不能な式だけ MATH_MASK の実インク高・baseline・縁取りを確認 |
| 未収録 math glyph | 暗黙 fallback を検出し、明示ログ＋安全な MATH_MASK 正規化へ進む |

## 記号・表記をいつ使うか

1. **節・章・図の番号** — 原稿 SoT は半角（`3.1`、`第3章`）。画面では同じ基本ゴシックの基準サイズで描く。単語全体の高さ合わせや小数点の個別拡大はしない
2. **数学の変数・式** — `$...$`。単純式は unicode flatten（半角のまま）。TTS カナを字幕に出さない  
3. **群名・定理名などのラテン固有表記** — 半角のまま一塊で基準サイズ。長ければ折り返す
4. **原稿 SoT の書き換え** — cues の半角を永続全角化しない（表示パイプラインのみ）

## flatten の境界

- 可: 単一変数、`x\times p`、`1-(i/\hbar)J·n dφ` のように記号置換で `\` と `_^{}` が消える式。短い分数は `J1/ℏ` のような slash 表記へ変換して意味と可読性を保てる場合に限り flatten
- 不可（MATH_MASK）: slash flatten で意味を保てない分数・根号・上下付き・大きな括弧伸長・行列など

## 縁取り

- 余白 `outer_w+8` 付きキャンバスで膨張する  
- 正方形 MaxFilter 単体は使わず、円形ダイレーション系で輪郭に沿わせる  
- 光学拡大後の advance で改行幅を再計算する（拡大を元幅に押し込まない）
- math mask も同じ supersample／dilate／downsample 経路へ通し、既定 math font の縁だけ別形状にしない

## 検証チェック

- [ ] `第3章` の `3` が別フォント風・別サイズ指定にならず、同じ font mask の native metrics／baseline で表示される
- [ ] `3.1` / `図28` の数字も同様  
- [ ] `$J$` / flatten 後の単独変数が同じ基本ゴシックで、単語bbox由来の巨大化・縮小がない
- [ ] `SU(2)` / `v1.2` が固定倍率で小さくならず、同じ字幕フォント感で表示される
- [ ] 通常の数字・Latin 識別子は基本ゴシックの native size／baseline で、単語全体の bbox 補正による倍率差がない。明示補正 glyph だけ実インク高と比率を記録する
- [ ] MATH_MASK が DejaVu／Computer Modern の無調整フォントに見えず、分子・分母の高さ、stem幅、分数線が潰れていない。fallback status が未検証なら合格にしない
- [ ] 字幕に TTS カナ（三点一、エイチバー）が出ていない  
- [ ] raw TeX を分類前に補正していない。MATH_MASK 化後は実インク高・baseline・advance・縁取りを正規化している

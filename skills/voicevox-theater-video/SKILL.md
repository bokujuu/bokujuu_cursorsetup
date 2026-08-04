---
name: voicevox-theater-video
description: >-
  VOICEVOX 劇場レイアウトの全画面スライド対話動画。立ち絵（胴体クロップなし）、ワイプ字幕、
  口パク（実音波形同期）、登場／退場（弾む歩き＋Y回転）、表情切替を Pillow＋ffmpeg で合成する。
  slide-narration-video の dialogue 拡張。Use when VOICEVOX劇場、立ち絵つき解説対話、
  theater profile、弾む登場・退場演出のとき。単純な Marp＋TTS のみ、
  Remotion 主軸、モノローグ専用は slide-narration-video に委譲。
---

# VOICEVOX 劇場動画（slide-narration 拡張）

Updated: 2026/08/05 00:55

`slide-narration-video` の **dialogue 劇場プロファイル**を、立ち絵・字幕・口パク・登場／退場演出まで含めて設計・実装する拡張 skill。
原稿・SoT・語り口は親 skill に従い、本 skill は **画面合成・レンダ規約・劇場プロファイル既定**を担う。
数値・話者・呼称の既定は Sakurai Ch3 系制作で収束した値（[references/theater-presets.md](references/theater-presets.md)）。呼称の出典は [ボイボ寮](https://voicevox.hiroshiba.jp/dormitory/)。

## 親 skill（必須）

着手前に読む:

1. [`../slide-narration-video/SKILL.md`](../slide-narration-video/SKILL.md) — 制作フロー・`narration_mode`・キュー SoT・**出典図の転載**
2. [`../slide-narration-video/references/dialogue-writing.md`](../slide-narration-video/references/dialogue-writing.md) — 対話原稿
3. [`../slide-narration-video/references/tts-pronunciation.md`](../slide-narration-video/references/tts-pronunciation.md) — 字幕＝`narration`、読み＝辞書→`tts_text`
4. [`../japanese-technical-writing/SKILL.md`](../japanese-technical-writing/SKILL.md) — スライドの論理
5. （monologue 接続のみ）[`../cognitive-rhythm-writing/SKILL.md`](../cognitive-rhythm-writing/SKILL.md)

本 skill を選ぶ条件: **立ち絵劇場レイアウト**が成果物の一部である。スライド＋音声だけの案件は親 skill のみでよい。

## 適用範囲

使う:

- 解説役（左）＋聞き手（右）の立ち絵 overlay
- 枠なしワイプ字幕（話者テーマ色縁取り）。字幕は **原文表記**（数字・ラテン・`$...$` 数式）
- VOICEVOX 発話 WAV に同期した口パク
- 動画先頭の無音登場（弾む歩きスライドイン＋フェード）
- 動画末尾の無音退場（Y 軸回転で外側向き → 弾む歩きスライドアウト＋フェード）
- 表情タグ（default / question / think / understand / surprise）

使わない:

- Remotion／Motion Canvas が主タイムラインの案件（親 skill）
- 立ち絵なしの ffmpeg 静止画結合のみ
- 会話劇そのものが目的で解説・理解確認がないコンテンツ

## プロファイル既定（明示上書きまで）

キューに `meta.speakers` / 素材指定が無いときの**本プロファイル既定**（ユーザーが別指定したらそちらを正とする）。詳細表: [references/theater-presets.md](references/theater-presets.md)。

| 役割 ID | 配置 | face_flip | 既定話者 | theme_rgb | 呼称／一人称（既定） |
|---------|------|-----------|----------|-----------|----------------------|
| `teacher` | 左下 | **true**（中央向き） | 冥鳴ひまり（id 14） | (155, 93, 229) | 相手=つむぎ先輩／私（[ボイボ寮](https://voicevox.hiroshiba.jp/dormitory/) 一致済み） |
| `listener` | 右下 | false（中央向き） | 春日部つむぎ（id 8） | (232, 168, 56) | 相手=ひまっち／あーし（同上） |

立ち絵素材の既定候補: とらっかぁ系 PSD 等の全身スプライト（胴体をクロップしない）。口は `closed`/`open`、表情は default/question/think/understand/surprise。ライセンス／クレジットは案件側で確認する。

口調・一人称・呼称は [ボイボ寮](https://voicevox.hiroshiba.jp/dormitory/)／[呼称表](https://voicevox.hiroshiba.jp/dormitory/call_names/) を正とする。**ひまり＋つむぎ既定のままなら**上表・`theater-presets.md` の `call_names` を再照会なしで使ってよい。別キャラに替えるときだけ寮を確認する。

キュー上は役割 ID を書き、話者名は `meta.speakers`（または上記既定）で解決する。

### 対話の既定（密度・前提・メタ分離）

劇場 dialogue では [references/dialogue-density.md](references/dialogue-density.md) に従う。

- 既定密度: **medium**（おおよそ 4〜5 発話・話者交替 3。厚い内容は `high`＝7 発話＋理解確認／再解説）
- 理解確認: 質問→回答→相槌／訂正→確認→（必要なら）再解説
- 前提説明: 知らないと崩れる語を AI が先に短く説明する（ユーザー指定を優先し不足を補う）
- **メタ指示禁止**: reasoning effort・校正・内部作業語（例: `extrahigh`）を動画本文・読み辞書へ入れない

## 既定スタック（劇場）

| 層 | 既定 | 備考 |
|----|------|------|
| スライド | 白テーマ PNG（Marp または Pillow 直描き） | ClearType 対策として Pillow＋源真ゴシックを**推奨**（必須固定ではない）。出典図は親 skill |
| 立ち絵 | 全身スプライト（上記プロファイル既定の素材候補） | 画面下へはみ出させて連続感。胴体クロップ禁止 |
| 合成 | Pillow（RGBA）→ ffmpeg rawvideo pipe | フレーム PNG を残さない |
| TTS | VOICEVOX（役割は `meta.speakers` またはプロファイル既定） | 発話ごと WAV。読みは辞書、字幕は `narration` |
| 字幕数式 | `$...$` を flatten／MATH_MASK | カタカナ読みを字幕に出さない。[subtitle-typography.md](references/subtitle-typography.md) |
| fps | **30（CFR）** | 本編15＋CFR再エンコードは同一ターゲットで総時間が改善しなかった（実測） |
| エンコード | libx264 | 短尺多数の NVENC はオーバーヘッドで不利になり得る |
| 字幕マスク | OpenCV 楕円 dilate（任意） | `cv2` 可なら `MORPH_ELLIPSE`。無ければ既存の Pillow perimeter dilate。速度目的で依存追加しない |
| フォント（字幕） | 源真ゴシック P Heavy（推奨） | 失敗時: MS UI Gothic → メイリオ → default |
| フォント（スライド） | 源真ゴシック P Medium/Bold（推奨） | 同上 |

詳細: [references/theater-presets.md](references/theater-presets.md) / [references/theater-layout.md](references/theater-layout.md) / [references/theater-render.md](references/theater-render.md) / [references/dialogue-density.md](references/dialogue-density.md) / [references/subtitle-typography.md](references/subtitle-typography.md) / [references/intro-entrance.md](references/intro-entrance.md) / [references/outro-exit.md](references/outro-exit.md)

## 制作フロー（劇場追加分）

親 skill の Task Progress に、劇場案件では次を足す。

```text
Theater extras:
- [ ] T0. profile: voicevox-theater（presets / layout / speakers / face_flip / call_names）
- [ ] T0b. 依頼文を題材／制作条件／メタ指示に分類。メタ語を本文候補から除外
- [ ] T0c. 参照タスク指定時は設定サマリー提示 → 不足のみ確認
- [ ] T0d. スライド密度（light/medium/high）と前提語彙を決める
- [ ] T1. 立ち絵エクスポート（固定キャンバス・表情・口開閉・レイヤ完全一致）
- [ ] T2. スライド書き出し（フリンジ対策・出典図・先頭出典行）
- [ ] T3. 導入: 無音弾む歩きスライドイン（左右同位相）
- [ ] T4. 本編: 発話クリップ（口パク＝実音区間＋0.1s 遅れ）
- [ ] T5. 字幕: narration 原文＋$LaTeX$／全行 色縁→黒縁→白文字
- [ ] T6. 退場: Y回転→弾む歩きアウト＋フェード（導入と同パラメータ）
- [ ] T7. concat → mp4 検証（導入／退場無音・口閉じ・縁・字幕記号）
- [ ] T8. 原稿検証: 発話数／交替／理解確認／メタ語混入なし／前提漏れなし
```

## 不変条件（短縮）

1. **対面**: 左=`teacher`（既定ひまり・`face_flip: true`）、右=`listener`（既定つむぎ）。中央向き
2. **口パク**: 無音では閉じる。実音開始から **0.1s 後**に開き始め（音声が先）。SoT は 0.1s（0.2s と書かない）。PSD 口レイヤは完全一致
3. **字幕レイヤ**: `narration`（SoT）を描画。TTS 用カナは出さない。表示区間は発話 cue の実測区間のみ（`pause_between_turns_ms` を含めない）。光学サイズは [subtitle-typography.md](references/subtitle-typography.md)。全行まとめて ①色縁 ②黒縁 ③白文字
4. **立ち絵**: 胴体を切り捨てない。入らない部分は画面外へ
5. **一時ファイル**: フレーム PNG を成果物として残さない
6. **導入**: 音なしで登場完了してから最初の発話。左右バウンスは同位相
7. **退場**: 本編後に音なしで外側向き回転→歩き去り→フェード
8. **対話**: 密度に応じた往復と理解確認。メタ指示を本文へ入れない。前提語を先に短く説明する

## 参照実装の置き場

global skill の SoT は本ディレクトリの Markdown 規約である。実装コードは案件 repo または `templates/project-skills/` へ置く。  
gitignored の `temp/` 試作は配布 SoT にしない（ローカル検証の一例にすぎない）。

## 検証

- 導入クリップが無音で、両キャラが外側から弾みながら定位置へ入る
- 退場クリップが無音で、Y 回転のあと外側へ歩きフェードする
- 最初の発話前に口が無音で動いていない
- 字幕に「三点二」「エイチバー」など TTS 用表記が出ておらず、`3.2` / `$\\hbar$` 等が原文どおり
- `第3章` の数字・`$J$` 等が和文と視覚高が揃う（[subtitle-typography.md](references/subtitle-typography.md)）

## メモリ

運用知見: [references/skill-memory.md](references/skill-memory.md)

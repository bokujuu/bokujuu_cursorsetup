# 劇場プロファイル既定（Sakurai Ch3 系）

Updated: 2026/08/05 00:55

明示上書きが無いときの **voicevox-theater プロファイル既定**。  
実測収束した Sakurai 第3章劇場制作の値を正とする。案件で変えてよいが、変えるときは生成前に差分を一言残す。

## 話者メタデータ（既定）

| フィールド | `teacher` | `listener` |
|------------|-----------|------------|
| side | left | right |
| face_flip | **true**（素材が右向きのため左右反転して中央向き） | false |
| engine | voicevox | voicevox |
| speaker | 冥鳴ひまり | 春日部つむぎ |
| style | ノーマル | ノーマル |
| speaker_id | 14 | 8 |
| sprite slug | `himari` | `tsumugi` |
| theme_rgb | (155, 93, 229) | (232, 168, 56) |
| 素材候補 | とらっかぁ系 全身 PSD／PNG | 同左 |

## 口調・一人称・呼称（ボイボ寮）

口調・一人称・相手の呼び方の SoT は **[ボイボ寮](https://voicevox.hiroshiba.jp/dormitory/)**（[呼称表](https://voicevox.hiroshiba.jp/dormitory/call_names/)）。世界観は必須遵守ではないが、VOICEVOX キャラを使う劇場案件ではこちらを正とする。

**ひまり＋つむぎのプロファイル既定を使う限り**、下表をそのまま使ってよく、制作のたびに寮ページを開き直す必要はない（寮と一致済み）。

| 項目 | 既定値 | ボイボ寮 |
|------|--------|----------|
| teacher 一人称 | 私 | ひまり |
| listener 一人称 | あーし | つむぎ |
| teacher → listener | つむぎ先輩 | ひまり→つむぎ |
| listener → teacher | ひまっち | つむぎ→ひまり |

別キャラ／別ペアに差し替えるとき、またはユーザーが寮と違う呼称を明示したときは、寮の該当キャラページ／呼称表を確認してから `call_names` を上書きする。未確認の推測で補完しない。

キュー例（`meta`）:

```yaml
meta:
  fps: 30
  narration_mode: dialogue
  profile: voicevox-theater
  layout:
    teacher_anchor: bottom_left
    listener_anchor: bottom_right
    subtitle_anchor: center_bottom_wipe
    slide_theme: light
    tachie: tracker-fullbody
  speakers:
    teacher:
      engine: voicevox
      speaker: 冥鳴ひまり
      style: ノーマル
      speaker_id: 14
      sprite: himari
      theme_rgb: [155, 93, 229]
      face_flip: true
    listener:
      engine: voicevox
      speaker: 春日部つむぎ
      style: ノーマル
      speaker_id: 8
      sprite: tsumugi
      theme_rgb: [232, 168, 56]
      face_flip: false
  call_names:
    teacher_to_listener: つむぎ先輩
    listener_to_teacher: ひまっち
    teacher_first_person: 私
    listener_first_person: あーし
  default_pause_between_turns_ms: 220
  default_pause_after_ms: 700
```

## 配置・スケール（1920×1080）

| 名前 | 既定値 | 意図 / 注意 |
|------|--------|-------------|
| `FACE_GAP` | `int(W * 0.42)`（顔重心 ≈ 中央±42%幅） | 左右対称。表情切替で `face_x` を再計算しない |
| `BODY_ON_SCREEN_H` | 962 | 全身 on-screen 高さ。胴体クロップ禁止 |
| `SPRITE_PAD_TOP` | 220 | エクスポート時の上余白と一致させる |
| `BUST_TOP_Y` | `H - int(600 * 0.88)`（≈552） | 頭上端の固定。拡縮は上揃え |
| `SUB_MAX_W` | 1350 | 字幕最大幅 |
| `SUB_BOX_BOTTOM` / `SUB_BOX_HEIGHT` | `H-56` / 150 | 下段ワイプ領域 |

案件上書き例（プロファイル既定ではない）: 画面幅の数 % だけ横シフト、頭上端 Y の個別指定などは `meta.layout` で明示する。

## 口パク

| 名前 | 既定 | 許容 / 注意 |
|------|------|-------------|
| `MOUTH_DELAY_MS` | **100**（0.1s） | SoT。0.2s と書かない |
| `MOUTH_MS` | 150 | 開閉交互の半周期 |
| `SPEECH_GAP_MERGE_MS` | 180 | 短い無音は発話連続扱い |
| `SPEECH_PAD_MS` | 40 | 区間パディング |
| `SPEECH_RMS_RATIO` | 0.05 | 相対閾値 |
| `SPEECH_RMS_FLOOR` | 180.0 | 絶対床 |

口状態ファイル名（ランタイム）: `{sprite}_{expression}_{closed|open}.png`  
非発話側・pause・intro／outro は常に `closed`。

## PSD／口レイヤー安全規則

1. **完全一致を優先**する（部分一致を既定にしない）
2. 開口は想定レイヤ名（例: `*あ`）と完全一致。`*あばー` 等への誤マッチは縦線ノイズの原因
3. 見つからないときは黙って別レイヤを選ばず、**警告またはエラー**で止める
4. 表情タグ不足時は `default` へフォールバックし、ログに残す

## 表情タグ

| tag | 用途 | 表示の目安 |
|-----|------|------------|
| `default` | 平常・説明の基調 | 発話の大半 |
| `question` | 疑問・食い付き | 聞き手の噛みつきに多い |
| `think` | 考え込み | 途中の迷い・整理 |
| `understand` | 納得・回収 | チェックポイント末・理解確認の着地 |
| `surprise` | 驚き | 予想外の事実の入口 |

キューの `utterances[].expression` が SoT。非話者側は `default`＋口閉じ。

## 登場／退場プリセット

詳細は [intro-entrance.md](intro-entrance.md) / [outro-exit.md](outro-exit.md)。要約:

| 項目 | 既定 |
|------|------|
| 弾む速さ | ≈6.7（`BOUNCE_SPEED = 20/3`） |
| 弾む高さ | 8（≈32px） |
| X 移動 | `SLIDE_IN_DIST ≈ 520` |
| 導入歩き / ホールド | 2400ms / 350ms |
| 退場回転 / 歩き / ホールド | 700ms / 2400ms / 200ms |
| フェード | 歩きの 0〜40%（導入）／最後 40%（退場） |
| 左右バウンス位相 | **同位相**（逆位相にしない） |

## 制作前サマリー（参照タスク引き継ぎ）

参照タスク ID／既存成果物が指定されたときは、生成前に次を抽出し短く提示する:

- speakers / call_names / theme_rgb / face_flip
- layout（アンカー・スケール・スライドテーマ）
- intro／outro／口パク数値
- 字幕・フォント方針

不足がある項目だけユーザー確認し、埋まっている項目は再質問しない。

## QA チェックリスト（抜粋）

- [ ] 左=ひまり（flip 済で中央向き）、右=つむぎ（中央向き）
- [ ] 登場バウンスが左右で同位相
- [ ] 口レイヤが完全一致／開口ノイズなし
- [ ] 無音区間で口が動いていない（遅れ 0.1s）
- [ ] 呼称・一人称が `call_names` と一致

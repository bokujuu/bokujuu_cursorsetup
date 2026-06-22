# path-settings xlsx — xlam アドインのビルド時設定

`.xlam` 統合アドインでパス・メール別名・ファイルアクセスを VBA ハードコードせず運用するパターン。
RibbonX 注入とは別トピック（RibbonX は [knowledge-base: ribbonx-xlam-build](https://github.com/bokujuu/knowledge-base/blob/main/docs/technology/excel/ribbonx-xlam-build.md) を参照。skill `excel-xlam-ribbon-build` は未マージ）。

## 方針

- 人間が編集するのは **`path-settings.local.xlsx`**（雛形は `path-settings.example.xlsx`）
- ビルド時に openpyxl で読み込み、**`PathConfig` VBA モジュールを生成して xlam に注入**
- 実行時に xlsx を読まない

## シート（すべて Excel テーブル / ListObject）

| シート | テーブル名 | 用途 |
|--------|------------|------|
| `Paths` | `PathSettingsTable` | パス・CC・UI ラベル（key/value） |
| `FileAccess` | `FileAccessTable` | リボン「ファイルアクセス」一覧 |
| `EmailMap` | `EmailMapTable` | 姓 → メール（`ConfigMailAlias`） |

**テーブル外に行を書かない。** `ws.append` でテーブル下に追記するとビルド時に無視される。
行追加後はテーブル範囲をリサイズする（実装例: `sync_config_tables` in `path_config.py`）。

## 読み取り

- ListObject があるシート → **テーブル内データ行のみ**
- テーブル無し（単体テスト用 xlsx）→ 2 行目以降にフォールバック

## ビルド入口（Windows）

```bat
scripts\build_excel_toolkit.bat
```

## 参照

- knowledge-base: [path-settings-xlam-config.md](https://github.com/bokujuu/knowledge-base/pull/12)（[PR #12](https://github.com/bokujuu/knowledge-base/pull/12) マージ待ち）
- excel-addins: https://github.com/bokujuu/excel-addins — `scripts/path_config.py`, `docs/excel-toolkit.md`

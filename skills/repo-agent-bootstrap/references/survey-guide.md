# 調査ガイド — リポジトリ文脈と過去セッションのマイニング

初期構築モードの手順1の詳細。**コードを読む前に文脈を読む**。

## 1. リポジトリ本体

| 確認対象 | 見るもの |
|----------|----------|
| `README.md` / `docs/*.md` | 目的・SoT ドキュメント・進捗（STATUS 系があれば最優先） |
| `git log --oneline -10` | 直近の作業内容・コミット粒度の慣習 |
| `git status --short` | 未コミットの並行作業の有無 |
| `pyproject.toml` 等 | lint / 型チェック設定（= 検証コマンド候補） |
| ディレクトリ構成 | 入力/出力データ、`.gitignore` 対象（= データ取り扱いルール候補） |

## 2. 過去セッション（agent-transcripts）

Cursor のプロジェクトフォルダ（`%USERPROFILE%\.cursor\projects\<repo-slug>\agent-transcripts\`）に
`<uuid>/<uuid>.jsonl` がある。**ユーザー発言だけ抽出**すれば短時間で文脈が掴める。

### jsonl の構造

```json
{"role":"user","message":{"content":[{"type":"text","text":"<user_query>...</user_query>"}]}}
{"role":"assistant","message":{"content":[{"type":"text","text":"..."},{"type":"tool_use",...}]}}
```

### PowerShell での抽出（文字化け対策込み）

```powershell
$OutputEncoding = [Console]::OutputEncoding = [Text.Encoding]::UTF8
Get-Content -Encoding UTF8 <transcript.jsonl> | ForEach-Object {
    $j = $_ | ConvertFrom-Json
    if ($j.role -eq 'user') {
        $txt = ($j.message.content | Where-Object { $_.type -eq 'text' } |
            ForEach-Object { $_.text }) -join "`n"
        if ($txt -and $txt -notmatch '^<system') {
            if ($txt.Length -gt 800) { $txt = $txt.Substring(0, 800) + ' ...' }
            '=== USER ==='; $txt
        }
    }
} | Out-File -Encoding UTF8 temp\transcript_users.txt
```

注意:

- コンソール直接出力は cp932 で文字化けしやすい。**temp ファイルに UTF-8 で書いて Read する**
- `$j.content` ではなく `$j.message.content`（ネストに注意）
- 本格的な掘り起こしが必要なら グローバル skill `cursor-session-doc` を使う

### 抽出結果から拾うもの

| 拾うもの | 行き先 |
|----------|--------|
| リポジトリの目的・ゴールの言明 | AGENTS.md「目的」 |
| ルール・仕様の指示 | SoT ドキュメントとの整合確認 |
| **訂正・手戻り**（「誤りがある」「〜も同様」等） | skill の「落とし穴」+ `skill-memory.md` 初期知見 |
| 繰り返された依頼パターン | repo ローカル skill のタスクカテゴリ |

## 3. 並行セッションの検出

複数チャットが同一 repo を編集していることがある。

```powershell
# 主要ファイルの更新時刻を作業開始時刻と比較
Get-ChildItem -Recurse src,docs -File | Sort-Object LastWriteTime -Descending |
    Select-Object -First 10 LastWriteTime, FullName
```

- 作業開始**直前〜直後**の更新があれば並行セッションを疑う
- 作業中に Read 済みファイルへ StrReplace が失敗したり検証が不可解に落ちたら、
  **ファイルを Read し直す**（自分の読んだ版が古い可能性）
- 並行セッションが SoT を編集中なら、docs の所有権を譲り自分は新規ファイル中心に作業する

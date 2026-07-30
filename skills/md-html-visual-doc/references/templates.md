# テンプレート断片

必要箇所だけコピーする。テーマ CSS やフレームワークは足さない。  
`{成果物ディレクトリ}` は対象リポの慣習またはユーザー指定で置換する。

## データ埋め込みの安全規約（必須）

Companion HTML に評価値・CSV・ログ・パスを入れるとき:

1. **DOM API 優先** — `textContent` / `createElement` / `appendChild` で入れる。
2. **文字列で HTML を組み立てる場合はエスケープ必須** — `& < > " '` をエンティティ化する（下の `escapeHtml` 例）。
3. **`href` / `src`** — 相対パス、または `https:` / `http:` / `file:`（ローカル閲覧時）のみ。`javascript:` 等は禁止。
4. **確認** — 入力に `<script>` や `<img onerror=...>` が含まれても、画面上は文字として見えること。

```javascript
function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}
```

## A. MD 索引（Companion 付き）

````markdown
# {題名}

{読者にしてほしいこと・1〜2文}

## 見る場所

- ブラウザで開く: [{短いラベル}]({相対/path/to/view.html})
- 生データ: `{相対/path/to/data}`

## 再生成

```bat
python {成果物ディレクトリ}/emit_view.py
```
````

## B. details で長い付録を隠す

````markdown
## 手順（要約）

1. …
2. …

<details>
<summary>詳細ログ・代替案</summary>

```text
（長い出力）
```

</details>
````

## C. figure でフロー画像

```markdown
<figure>
  <img src="assets/flow.svg" alt="{主経路の一文}" width="720" />
  <figcaption>{主経路の一文}（生成: assets/flow.mmd）</figcaption>
</figure>
```

または:

```markdown
![主経路の一文](assets/flow.svg)

*図: 主経路の一文。ソース `assets/flow.mmd`。*
```

## D. Companion HTML 骨格（比較ビュー）

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{題名}</title>
  <style>
    :root { color-scheme: light dark; }
    body { font-family: system-ui, sans-serif; margin: 1rem 1.25rem; line-height: 1.45; }
    h1 { font-size: 1.25rem; margin: 0 0 0.5rem; }
    .hint { opacity: 0.8; margin-bottom: 1rem; }
    label { margin-right: 0.75rem; }
    table { border-collapse: collapse; width: 100%; font-size: 0.9rem; }
    th, td { border: 1px solid #8884; padding: 0.4rem 0.5rem; vertical-align: top; }
    th { text-align: left; }
    /* fallback 先、対応ブラウザ向けに color-mix */
    .in { background: #e8f1fa; background: color-mix(in srgb, canvas 92%, #4a90d9); }
    .out { background: #e8f6ee; background: color-mix(in srgb, canvas 92%, #3d9a5f); }
    .ref { background: #f7f0e0; background: color-mix(in srgb, canvas 92%, #b0892e); }
    .hide { display: none; }
  </style>
</head>
<body>
  <h1>{題名}</h1>
  <p class="hint">{目的1行}。列は 入力 → 出力 → 参照。</p>
  <p>
    <label>フィルタ <input id="q" type="search" placeholder="id / 文言" /></label>
  </p>
  <table>
    <thead>
      <tr><th>id</th><th class="in">入力</th><th class="out">出力</th><th class="ref">参照</th></tr>
    </thead>
    <tbody id="rows"></tbody>
  </table>
  <script>
    function escapeHtml(s) {
      return String(s)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }
    // rowsData は生成スクリプトが埋め込む。値は必ず escapeHtml してから挿入する。
    const rowsData = []; // [{ id, input, output, ref }, ...]
    const tbody = document.getElementById('rows');
    for (const r of rowsData) {
      const tr = document.createElement('tr');
      tr.innerHTML =
        '<td>' + escapeHtml(r.id) + '</td>' +
        '<td>' + escapeHtml(r.input) + '</td>' +
        '<td>' + escapeHtml(r.output) + '</td>' +
        '<td>' + escapeHtml(r.ref) + '</td>';
      tbody.appendChild(tr);
    }
    const q = document.getElementById('q');
    const rows = [...document.querySelectorAll('#rows tr')];
    q.addEventListener('input', () => {
      const s = q.value.trim().toLowerCase();
      for (const tr of rows) {
        tr.classList.toggle('hide', s && !tr.innerText.toLowerCase().includes(s));
      }
    });
  </script>
</body>
</html>
```

データ行が多い場合は Python 等でこの骨格へ埋め込み、手書きしない。埋め込み時も上の安全規約に従う。

## E. ギャラリー MD（薄い）

```markdown
# {題名} ギャラリー

ブラウザ: [{name}.html]({name}.html)

## パス一覧

- `images/a.png`
- `images/b.png`
```

HTML 側でグリッド表示。MD に全画像を埋め込まない。

# モデルルーティング（Grok 4.5 × Composer 2.5）

更新: 2026/07/17 02:26

## 結論（先に）

主利用モデルは当面 **Grok 4.5** を想定する。変えるべきなのは「**どのモデルをいつ使うか**」の運用と、現状 **Composer 固定**になっているループラッパー／表記、および skill 分類ごとの扱いである。

skill は一括で「大半はそのままでよい」とせず、次の分類で判断する。

| 層 | 変更要否 | 理由 |
|----|----------|------|
| `user-rules/` | 不要 | 口調・最小変更のみ。モデル名を書かない |
| Domain / constraint skills | 原則維持 | 業務知識・不変条件・検証はモデル非依存 |
| Deliverable / workflow skills | 維持＋軽量化 | 成果物要件は残し、固定件数・不要順序は削る |
| Reasoning intervention skills | 軽量化または明示起動 | 上位モデルでは思考手順の固定が競合しやすい |
| Autonomy / loop-control skills | 安全境界との整合を最優先 | 人間確認・外部操作の境界はモデル非依存ではない |
| `templates/loop-orchestration/` | 軽微 | 既定は Composer、上書きで Grok |
| `docs/`（本ファイル） | SoT | ルーティングと skill 分類 |

## Skill 分類

### 1. Domain / constraint skills

業務知識、不変条件、環境固有情報、検証条件。  
原則モデル非依存で維持する。Grok / Composer どちらでも同じ Done / Verify を使う。

### 2. Deliverable / workflow skills

成果物形式、再現可能な手順。  
明示性（何を出すか・どう検証するか）は維持し、固定件数・不要な順序・依頼外の Git 操作は削る。

### 3. Reasoning intervention skills

モデルの思考順序、phase、固定出力を規定するもの（例: `fable-style-reasoning`）。  
上位モデルでは競合しやすいため、軽量化または明示起動を検討する。本ファイル時点では既存 skill の大規模改稿はしない。

### 4. Autonomy / loop-control skills

人間確認、反復、外部操作の境界（例: `anti-human-bottleneck`, `ralph-loop`）。  
モデル非依存ではなく、User Rules および承認境界との整合を最優先する。ローカル可逆な自律と、commit / push / deploy 等の外部・不可逆操作を混同しない。

## Grok 4.5 向け

- 探索・設計の裁量を残す。手順を過剰に固定しない。
- ドメイン制約・Done 条件・Verify 方法は具体的に与える。
- 説明や探索が厚くなりやすいため、固定テンプレートでさらに増幅しない。
- Skill 間の矛盾はモデル能力で吸収させず、設定側で解消する。

## 公式の位置づけ（要約）

[Introducing Grok 4.5](https://cursor.com/blog/grok-4-5) より:

- **Composer 2.5** — coding specialist（ソフトウェア実装に特化）
- **Grok 4.5** — より広い訓練ミックス（STEM・研究・知識作業）。ソフトウェア以外も含む難しい長時間タスク向け
- 両者は **別 weight class**。Composer は継続提供

価格帯の目安（同ブログ）: Grok は Composer より高い。ループの反復回数が多いほどコスト差が効く。

## 推奨ルーティング

| 用途 | 推奨モデル | slug 例 | 理由 |
|------|------------|---------|------|
| 対話のメイン・設計・調査・曖昧な要件 | **Grok** | `grok-4.5-xhigh` | 広い推論・ツール創造的利用 |
| 明確な実装・機械的編集・差分収束 | **Composer** | `composer-2.5` | 実装特化・コスト効率 |
| Ralph / CLI 外側ループ（多数反復） | **Composer（既定）** | `composer-2.5` | 反復コスト。難所だけ Grok 上書き |
| レイテンシ最優先の下書き | fast 系 | `*-fast*` | 品質より速度。本番ループの既定にしない |

### 使い分けの判断基準

1. **完了条件が観測可能で、変更範囲が狭い** → Composer
2. **仮説が複数・ドメイン横断・設計トレードオフ** → Grok
3. **ループの「内側1反復」が単純な verify 収束** → Composer
4. **ループの特定イテレーションだけ行き詰まった** → その回だけ `CURSOR_MODEL` / `-Model` で Grok

IDE のモデルピッカーと CLI `--model` の slug は製品側の表記に合わせる。本 repo は **品質系を既定**とし、account default の fast 上書きを避ける（従来方針の一般化）。

## skill 設計への含意

- skill 本文に特定モデル名を**必須条件として書かない**（「Cursor エージェント」または「Grok / Composer」）
- モデル差で振る舞いが分かれる知見は、まず `references/skill-memory.md` に1行追記し、安定したら本ファイルへ昇格
- 新規 skill は [global-suitability](review/global-suitability-and-knowledge-capture.md) どおりモデル非依存を優先
- 上記 4 分類で、維持・軽量化・安全境界のどれが主かを意識する

### 観測されやすい差（運用メモ）

確定ベンチではなく、併用時の注意点:

| 傾向 | 対応 |
|------|------|
| Grok は説明・探索が厚くなりやすい | User Rules の簡潔さ・最小変更を維持。`fable-style-reasoning` の出力テンプレは start/transition/done のみ |
| Composer は小さなタスクでも複数ファイルを触りやすい | light モードのゲートは「ファイル数」ではなく「観測可能な verify」 |
| Grok はコストが高い | ループ既定は Composer。対話メインだけ Grok |

## ループキットでの上書き

既定値は **`composer-2.5`**（多数反復向け）。Grok を使う例:

```powershell
# PowerShell（1 反復）
.\run-once.ps1 -Model grok-4.5-xhigh

# bash
MODEL=grok-4.5-xhigh ./ralph.sh

# TypeScript SDK ラッパー
CURSOR_MODEL=grok-4.5-xhigh node ./ralph.mjs
```

`ralph.ps1` は `-Model` を `run-once.ps1` に渡す。

## やらないこと

- User Rules にモデル名やルーティング表を載せない（技術手順の肥大化）
- 全 skill を Grok 専用に書き換えない
- ループ既定を無条件で Grok にしない（コスト）
- slug を製品ドキュメントより先に「推測で固定」しすぎない（ピッカー表記の変更に追従）

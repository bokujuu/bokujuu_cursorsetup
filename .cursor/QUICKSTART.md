# MCP サーバー クイックスタートガイド

## 🚀 3分で始める MCP セットアップ

### **ステップ 1: 自動インストール実行**

PowerShell を**管理者権限**で開き、以下を実行：

```powershell
# プロジェクトディレクトリに移動
cd C:\CursorPJs\onlychat

# 実行ポリシーの変更（一時的）
Set-ExecutionPolicy Bypass -Scope Process

# 自動インストール実行
.\install_mcp_servers.ps1
```

### **ステップ 2: Cursor 再起動**

1. Cursor を完全に終了
2. Cursor を再起動
3. 設定が読み込まれるまで約10秒待機

### **ステップ 3: 動作確認**

Cursor のチャットで以下をテスト：

```
@filesystem このディレクトリの内容を表示してください
```

## 📋 利用可能な MCP サーバー

| サーバー名 | 用途 | テストコマンド |
|------------|------|----------------|
| **context7** | ライブラリドキュメント | `@context7 React フックの使い方を教えて` |
| **excel** | Excel操作 | `@excel test_workbook.xlsx の内容を確認` |
| **playwright** | ブラウザ自動化 | `@playwright Google のタイトルを取得` |
| **filesystem** | ファイル操作 | `@filesystem temp フォルダの内容を表示` |
| **memory** | データ保持 | `@memory 今日の作業を記録` |

## 🛠 手動インストール（問題が発生した場合）

### **必須コマンド**
```powershell
# Node.js パッケージ
npm install -g @playwright/mcp@latest
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-memory

# Python パッケージ（Excel用）
pip install uv
pip install excel-mcp-server

# ブラウザエンジン
npx playwright install
```

### **設定ファイル適用**
```powershell
copy .cursor\mcp_enhanced.json "$env:USERPROFILE\.cursor\mcp.json"
```

## 🆘 トラブルシューティング

### **よくある問題**

#### **❌ MCP サーバーが認識されない**
```powershell
# Cursor の完全再起動
# PowerShell で設定確認
Get-Content "$env:USERPROFILE\.cursor\mcp.json"
```

#### **❌ NPM インストールエラー**
```powershell
npm cache clean --force
npm install -g npm@latest
```

#### **❌ Python/UV エラー**
```powershell
python --version  # 3.8+ 必須
pip install --upgrade uv
```

#### **❌ 権限エラー**
```powershell
# PowerShell を管理者権限で実行
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **エラーチェック手順**

1. **前提条件確認**
   ```powershell
   node --version    # 18.0.0+
   npm --version
   python --version  # 3.8+
   git --version
   ```

2. **設定ファイル検証**
   ```powershell
   # JSON形式チェック
   Get-Content "$env:USERPROFILE\.cursor\mcp.json" | ConvertFrom-Json
   ```

3. **パッケージ確認**
   ```powershell
   npm list -g | Select-String "mcp\|playwright"
   pip list | Select-String "excel-mcp"
   ```

## 💡 実用例

### **Excel ファイル分析**
```
@excel test_workbook.xlsx の全シートを確認し、データの概要を教えてください
```

### **プロジェクト管理**
```
@filesystem プロジェクト内の Python ファイルを一覧表示
@memory 今日実装した機能を記録: [機能名]
```

### **Web 自動化**
```
@playwright https://example.com にアクセスしてページタイトルを取得
```

### **メモ保存**
```
@memory 今日の議事録を保存してください
```

（追加ツールは必要時に導入）

## 🔧 カスタマイズ

### **独自 MCP サーバーの追加**
`mcp_enhanced.json` に新しいサーバーを追加：

```json
{
  "mcpServers": {
    "custom-server": {
      "command": "npx",
      "args": ["-y", "your-mcp-server"]
    }
  }
}
```

### **設定の無効化**
使用しないサーバーは設定から削除：

```json
{
  "mcpServers": {
    // "shell": { ... },  // コメントアウトで無効化
  }
}
```

## 📚 参考リンク

- [Cursor 公式ドキュメント](https://docs.cursor.com/)
- [MCP 公式リポジトリ](https://github.com/modelcontextprotocol)
- [Playwright ドキュメント](https://playwright.dev/)

---

**🎯 目標**: 3分以内にすべてのMCPサーバーを稼働させる  
**🚨 困った時**: `INSTALL_GUIDE.md` の詳細情報を参照

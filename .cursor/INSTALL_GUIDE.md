# MCP サーバー インストールガイド

## 前提条件の確認

### **1. Node.js のインストール確認**
```powershell
# バージョン確認（18.0.0 以上推奨）
node --version
npm --version

# インストールされていない場合
# https://nodejs.org/ から最新版をダウンロード・インストール
```

### **2. Python のインストール確認**
```powershell
# バージョン確認（3.8 以上推奨）
python --version

# uvx が必要（Python パッケージマネージャー）
pip install uv
```

### **3. Git のインストール確認**
```powershell
# バージョン確認
git --version

# インストールされていない場合
# https://git-scm.com/ から最新版をダウンロード・インストール
```

## MCP サーバーのインストール

### **一括インストールスクリプト**

以下のコマンドを PowerShell で実行してください：

```powershell
# 作業ディレクトリに移動
cd C:\CursorPJs\onlychat

# NPM キャッシュをクリア
npm cache clean --force

# 各MCPサーバーのプリインストール（オプション）
Write-Host "=== MCP サーバー プリインストール開始 ===" -ForegroundColor Green

# Excel MCP Server (uvx経由)
Write-Host "Excel MCP Server をインストール中..." -ForegroundColor Yellow
pip install excel-mcp-server

# Playwright MCP Server
Write-Host "Playwright MCP Server をインストール中..." -ForegroundColor Yellow
npm install -g @playwright/mcp@latest
playwright install

# 基本 MCP サーバーをインストール中...
Write-Host "基本 MCP サーバーをインストール中..." -ForegroundColor Yellow
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-memory

Write-Host "=== インストール完了 ===" -ForegroundColor Green
```

### **個別インストールコマンド**

#### **Excel MCP Server**
```powershell
# UV パッケージマネージャー経由
pip install uv
pip install excel-mcp-server

# または直接
uvx excel-mcp-server --help
```

#### **Playwright MCP Server**
```powershell
# NPM 経由でインストール
npm install -g @playwright/mcp@latest

# ブラウザエンジンのインストール
npx playwright install

# 確認
npx @playwright/mcp@latest --help
```

#### **基本 MCP Servers**
```powershell
# Filesystem Server
npm install -g @modelcontextprotocol/server-filesystem

# Memory Server  
npm install -g @modelcontextprotocol/server-memory
```

### **設定ファイルの適用**

```powershell
# 現在の設定をバックアップ
Copy-Item "$env:USERPROFILE\.cursor\mcp.json" "$env:USERPROFILE\.cursor\mcp.json.backup" -ErrorAction SilentlyContinue

# 新しい設定を適用
Copy-Item ".cursor\mcp_enhanced.json" "$env:USERPROFILE\.cursor\mcp.json"

# 設定確認
Get-Content "$env:USERPROFILE\.cursor\mcp.json"
```

## 動作確認

### **1. Cursor の再起動**
設定を反映するため Cursor を完全に再起動してください。

### **2. 各サーバーの動作確認**

#### **Context7 サーバー**
```
@context7 React の最新バージョン情報を教えてください
```

#### **Excel MCP サーバー**
```
@excel プロジェクト内の Excel ファイルを確認してください
```

#### **Playwright サーバー**
```
@playwright Google のホームページのタイトルを取得してください
```

#### **Filesystem サーバー**
```
@filesystem 現在のディレクトリの内容を表示してください
```

#### **Memory サーバー**
```
@memory 今日の作業内容を記録してください
```

## トラブルシューティング

### **よくある問題と解決法**

#### **NPM インストールエラー**
```powershell
# NPM キャッシュをクリア
npm cache clean --force

# Node.js を最新版に更新
npm install -g npm@latest

# 権限エラーの場合
npm config set prefix %APPDATA%\npm
```

#### **Python/UV インストールエラー**
```powershell
# UV を最新版に更新
pip install --upgrade uv

# パッケージ再インストール
uvx pip install --force-reinstall excel-mcp-server
```

#### **Playwright インストールエラー**
```powershell
# ブラウザエンジンの手動インストール
npx playwright install chromium
npx playwright install firefox
npx playwright install webkit
```

#### **権限エラー（Windows）**
```powershell
# PowerShell を管理者権限で実行
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# または
Set-ExecutionPolicy Bypass -Scope Process
```

#### **パッケージが見つからない場合**
```powershell
# レジストリ確認
npm search @modelcontextprotocol

# 代替パッケージの検索
npm search mcp-server
```

### **設定ファイルのデバッグ**
```powershell
# JSON 形式の検証
Get-Content "$env:USERPROFILE\.cursor\mcp.json" | ConvertFrom-Json

# エラーログの確認
Get-EventLog -LogName Application -Source "Cursor" -Newest 10
```

## 定期メンテナンス

### **月次更新スクリプト**
```powershell
# MCP サーバーの更新
Write-Host "=== MCP サーバー更新開始 ===" -ForegroundColor Green

# NPM パッケージ更新
npm update -g @playwright/mcp
npm update -g @modelcontextprotocol/server-filesystem
npm update -g @modelcontextprotocol/server-memory

# Python パッケージ更新
pip install --upgrade excel-mcp-server

Write-Host "=== 更新完了 ===" -ForegroundColor Green
```

## 使用上の注意

### **セキュリティ**
- Shell MCP は強力な機能のため、信頼できるコマンドのみ実行
- Git MCP は機密情報を含むリポジトリでは注意が必要
- Filesystem MCP はアクセス権限の範囲を適切に設定

### **パフォーマンス**
- 使用しない MCP サーバーは設定から除外
- SQLite データベースは定期的な最適化を推奨
- Memory MCP のデータは定期的にクリアを推奨

### **互換性**
- Cursor のバージョン更新時は設定の再確認が必要
- MCP サーバーのバージョン互換性に注意
- Windows、macOS、Linux での動作差異を考慮

---
**作成日**: 2024年  
**更新**: 必要に応じて最新版に更新してください

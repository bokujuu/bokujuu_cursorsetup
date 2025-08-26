# MCP サーバー 自動インストールスクリプト
# PowerShell で実行してください: .\install_mcp_servers.ps1

param(
    [switch]$SkipPrereq,
    [switch]$Quiet
)

function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    if (-not $Quiet) {
        Write-Host $Message -ForegroundColor $Color
    }
}

function Test-Command {
    param([string]$Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

Write-ColorOutput "=== MCP サーバー自動インストール開始 ===" "Green"
Write-ColorOutput "作業ディレクトリ: $(Get-Location)" "Cyan"

# 前提条件の確認
if (-not $SkipPrereq) {
    Write-ColorOutput "`n--- 前提条件の確認 ---" "Yellow"
    
    # Node.js の確認
    if (Test-Command "node") {
        $nodeVersion = node --version
        Write-ColorOutput "✓ Node.js: $nodeVersion" "Green"
    } else {
        Write-ColorOutput "✗ Node.js が見つかりません" "Red"
        Write-ColorOutput "https://nodejs.org/ からインストールしてください" "Yellow"
        exit 1
    }
    
    # NPM の確認
    if (Test-Command "npm") {
        $npmVersion = npm --version
        Write-ColorOutput "✓ NPM: $npmVersion" "Green"
    } else {
        Write-ColorOutput "✗ NPM が見つかりません" "Red"
        exit 1
    }
    
    # Python の確認
    if (Test-Command "python") {
        $pythonVersion = python --version
        Write-ColorOutput "✓ Python: $pythonVersion" "Green"
    } else {
        Write-ColorOutput "⚠ Python が見つかりません（Excel MCP に必要）" "Yellow"
    }
    
    # Git の確認
    if (Test-Command "git") {
        $gitVersion = git --version
        Write-ColorOutput "✓ Git: $gitVersion" "Green"
    } else {
        Write-ColorOutput "⚠ Git が見つかりません（Git MCP に必要）" "Yellow"
    }
}

# NPM キャッシュクリア
Write-ColorOutput "`n--- NPM キャッシュクリア ---" "Yellow"
try {
    npm cache clean --force
    Write-ColorOutput "✓ NPM キャッシュクリア完了" "Green"
} catch {
    Write-ColorOutput "⚠ NPM キャッシュクリアに失敗しました" "Yellow"
}

# MCP サーバーのインストール
Write-ColorOutput "`n--- MCP サーバーインストール ---" "Yellow"

$mcpServers = @(
    @{Name = "Excel MCP Server"; Command = "pip install excel-mcp-server"; Type = "Python"},
    @{Name = "Playwright MCP Server"; Command = "npm install -g @playwright/mcp@latest"; Type = "NPM"},
    @{Name = "Playwright Browsers"; Command = "npx playwright install"; Type = "NPM"},
    @{Name = "Filesystem Server"; Command = "npm install -g @modelcontextprotocol/server-filesystem"; Type = "NPM"},
    @{Name = "Memory Server"; Command = "npm install -g @modelcontextprotocol/server-memory"; Type = "NPM"}
)

foreach ($server in $mcpServers) {
    Write-ColorOutput "`n$($server.Name) をインストール中..." "Cyan"
    try {
        if ($server.Type -eq "Python" -and -not (Test-Command "python")) {
            Write-ColorOutput "⚠ Python が見つからないため、スキップします" "Yellow"
            continue
        }
        
        Invoke-Expression $server.Command
        Write-ColorOutput "✓ $($server.Name) インストール完了" "Green"
        Start-Sleep -Seconds 1
    } catch {
        Write-ColorOutput "✗ $($server.Name) インストールに失敗: $($_.Exception.Message)" "Red"
    }
}

# UV のインストール（Excel MCP 用）
if (Test-Command "python") {
    Write-ColorOutput "`n--- UV パッケージマネージャーのインストール ---" "Yellow"
    try {
        python -m pip install uv
        Write-ColorOutput "✓ UV インストール完了" "Green"
    } catch {
        Write-ColorOutput "⚠ UV インストールに失敗しました" "Yellow"
    }
}

# 設定ファイルの適用
Write-ColorOutput "`n--- 設定ファイルの適用 ---" "Yellow"

$cursorConfigPath = "$env:USERPROFILE\.cursor\mcp.json"
$enhancedConfigPath = ".\mcp_enhanced.json"

if (Test-Path $enhancedConfigPath) {
    # 既存設定のバックアップ
    if (Test-Path $cursorConfigPath) {
        $backupPath = "$cursorConfigPath.backup.$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        Copy-Item $cursorConfigPath $backupPath -ErrorAction SilentlyContinue
        Write-ColorOutput "✓ 既存設定をバックアップしました: $backupPath" "Green"
    }
    
    # 新設定の適用
    try {
        # .cursor ディレクトリが存在しない場合は作成
        $cursorDir = Split-Path $cursorConfigPath
        if (-not (Test-Path $cursorDir)) {
            New-Item -ItemType Directory -Path $cursorDir -Force | Out-Null
        }
        
        Copy-Item $enhancedConfigPath $cursorConfigPath
        Write-ColorOutput "✓ 新しい MCP 設定を適用しました" "Green"
        
        # JSON 形式の検証
        try {
            Get-Content $cursorConfigPath | ConvertFrom-Json | Out-Null
            Write-ColorOutput "✓ 設定ファイルの JSON 形式は正常です" "Green"
        } catch {
            Write-ColorOutput "✗ 設定ファイルの JSON 形式に問題があります" "Red"
        }
    } catch {
        Write-ColorOutput "✗ 設定ファイルの適用に失敗しました: $($_.Exception.Message)" "Red"
    }
} else {
    Write-ColorOutput "⚠ mcp_enhanced.json が見つかりません" "Yellow"
}

# インストール結果の確認
Write-ColorOutput "`n--- インストール結果確認 ---" "Yellow"

$testCommands = @(
    @{Name = "Playwright MCP"; Command = "npx @playwright/mcp@latest --help"},
    @{Name = "Filesystem Server"; Command = "npx @modelcontextprotocol/server-filesystem --help"}
)

foreach ($test in $testCommands) {
    Write-ColorOutput "$($test.Name) の動作確認..." "Cyan"
    try {
        $null = Invoke-Expression "$($test.Command) 2>`$null"
        Write-ColorOutput "✓ $($test.Name) 正常動作" "Green"
    } catch {
        Write-ColorOutput "⚠ $($test.Name) の動作確認に失敗" "Yellow"
    }
}

# 完了メッセージ
Write-ColorOutput "`n=== インストール完了 ===" "Green"
Write-ColorOutput "`n次の手順:" "Yellow"
Write-ColorOutput "1. Cursor を完全に再起動してください" "White"
Write-ColorOutput "2. Cursor のチャットで各 MCP サーバーをテストしてください" "White"
Write-ColorOutput "`n例:" "Cyan"
Write-ColorOutput "  @excel プロジェクト内の Excel ファイルを確認" "Gray"
Write-ColorOutput "  @filesystem ディレクトリ内容を表示" "Gray"
Write-ColorOutput "  @playwright Google のタイトルを取得" "Gray"

Write-ColorOutput "`nトラブルシューティング情報は INSTALL_GUIDE.md を参照してください" "Yellow"

# エラーログの出力（オプション）
if (-not $Quiet) {
    Write-ColorOutput "`n実行ログは PowerShell の履歴に保存されています" "Gray"
    Write-ColorOutput "問題が発生した場合は、INSTALL_GUIDE.md の『トラブルシューティング』セクションを確認してください" "Gray"
}

Write-ColorOutput "`n🎉 MCP サーバーのセットアップが完了しました！" "Green"

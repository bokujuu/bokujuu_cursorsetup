#Requires -Version 5.1
<#
.SYNOPSIS
  bokujuu_cursorsetup の skills/ を %USERPROFILE%\.codex\skills\ へコピーする。
  hooks/ がある場合は %USERPROFILE%\.cursor\hooks\ と hooks.json も配置する。
#>
param(
    [switch]$WhatIf,
    [switch]$SkipHooks,
    # グローバル Cursor mcp.json が無いときだけ mcp.template.json を配置する（既存動作）
    [switch]$InstallMcp,
    # Codex の config.toml と AGENTS.md だけを更新する。Cursor 側は変更しない。
    [switch]$InstallCodex
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Src = Join-Path $Root "skills"
$Dst = Join-Path $env:USERPROFILE ".codex\skills"

if (-not (Test-Path $Src)) {
    Write-Error "skills folder not found: $Src"
}

New-Item -ItemType Directory -Force -Path $Dst | Out-Null

$ManagedState = Join-Path $Dst ".bokujuu-cursorsetup-managed.txt"
$HasManagedState = Test-Path -LiteralPath $ManagedState
$LegacyManagedNames = @(
    # One-time migration for names managed before the ownership marker existed.
    "codex-session-doc",
    "empirical-prompt-tuning",
    "retrospective-codify",
    "skill-lifecycle",
    "system-structure-viz"
)
$CurrentSkillDirs = @(Get-ChildItem -LiteralPath $Src -Directory | Sort-Object Name)
$CurrentSkillNames = @($CurrentSkillDirs | Select-Object -ExpandProperty Name)
$PreviousManagedNames = @()

if ($HasManagedState) {
    $PreviousManagedNames = @(
        Get-Content -LiteralPath $ManagedState -ErrorAction Stop |
            ForEach-Object { $_.Trim() } |
            Where-Object { $_ }
    )
}

$KnownManagedNames = @($PreviousManagedNames)
if (-not $HasManagedState) {
    $KnownManagedNames += $LegacyManagedNames
}
$StaleManagedNames = @(
    $KnownManagedNames |
        Sort-Object -Unique |
        Where-Object {
            $_ -match '^[A-Za-z0-9_-]+$' -and $_ -notin $CurrentSkillNames
        }
)

foreach ($name in $StaleManagedNames) {
    $target = Join-Path $Dst $name
    if (Test-Path -LiteralPath $target) {
        Write-Host "[REMOVE] retired skill -> $target"
        if (-not $WhatIf) {
            Remove-Item -LiteralPath $target -Recurse -Force
        }
    }
}

$CurrentSkillDirs | ForEach-Object {
    $target = Join-Path $Dst $_.Name
    Write-Host "[COPY] $($_.Name) -> $target"
    if ($WhatIf) {
        return
    }
    if (Test-Path $target) {
        Remove-Item $target -Recurse -Force
    }
    Copy-Item $_.FullName $target -Recurse -Force
}

if (-not $WhatIf) {
    $CurrentSkillNames | Set-Content -LiteralPath $ManagedState -Encoding UTF8
}

Write-Host "[OK] Global skills installed under $Dst"

if ($InstallCodex) {
    $CodexDir = Join-Path $env:USERPROFILE ".codex"
    $CodexConfigPath = Join-Path $CodexDir "config.toml"
    $CodexAgentsPath = Join-Path $CodexDir "AGENTS.md"
    $CodexMcpTemplatePath = Join-Path $Root "mcp\codex-mcp.template.toml"
    $UserRulesSourcePath = Join-Path $Root "user-rules\user-rule-cursor-communication.md"
    $ManagedBegin = "# BEGIN bokujuu-cursorsetup managed Codex MCP"
    $ManagedEnd = "# END bokujuu-cursorsetup managed Codex MCP"

    foreach ($required in @($CodexMcpTemplatePath, $UserRulesSourcePath)) {
        if (-not (Test-Path -LiteralPath $required)) {
            Write-Error "Codex source file not found: $required"
        }
    }

    Write-Host "[CODEX] Synchronize global AGENTS.md from Cursor User Rules"
    if (-not $WhatIf) {
        New-Item -ItemType Directory -Force -Path $CodexDir | Out-Null
    }

    $agentsDifferent = $true
    if (Test-Path -LiteralPath $CodexAgentsPath) {
        $agentsDifferent = ((Get-FileHash -Algorithm SHA256 -LiteralPath $CodexAgentsPath).Hash -ne
            (Get-FileHash -Algorithm SHA256 -LiteralPath $UserRulesSourcePath).Hash)
    }
    if (-not $agentsDifferent) {
        Write-Host "[OK] Codex AGENTS.md already matches $UserRulesSourcePath"
    }
    elseif ($WhatIf) {
        Write-Host "[WHATIF] Would back up and replace $CodexAgentsPath"
    }
    else {
        if (Test-Path -LiteralPath $CodexAgentsPath) {
            $backupStamp = Get-Date -Format "yyyyMMdd-HHmmss"
            $backupPath = "$CodexAgentsPath.bak-$backupStamp"
            Copy-Item -LiteralPath $CodexAgentsPath -Destination $backupPath -Force
            Write-Host "[BACKUP] $CodexAgentsPath -> $backupPath"
        }
        Copy-Item -LiteralPath $UserRulesSourcePath -Destination $CodexAgentsPath -Force
        Write-Host "[OK] Wrote $CodexAgentsPath"
    }

    Write-Host "[CODEX] Synchronize managed MCP blocks in $CodexConfigPath"
    $templateText = (Get-Content -LiteralPath $CodexMcpTemplatePath -Raw -Encoding UTF8).Trim()
    $configText = ""
    if (Test-Path -LiteralPath $CodexConfigPath) {
        $configText = Get-Content -LiteralPath $CodexConfigPath -Raw -Encoding UTF8
    }

    $managedPattern = "(?ms)^" + [regex]::Escape($ManagedBegin) + "\r?\n.*?^" +
        [regex]::Escape($ManagedEnd) + "\r?\n?"
    if ($configText -match [regex]::Escape($ManagedBegin)) {
        $newConfigText = [regex]::Replace($configText, $managedPattern, $templateText + "`r`n")
    }
    else {
        $managedNames = @("filesystem", "memory", "codex-sol", "codex-terra", "codex-luna")
        $existingManaged = @(
            $managedNames | Where-Object {
                $configText -match ("(?m)^\[mcp_servers\." + [regex]::Escape($_) + "\]\s*$")
            }
        )
        if ($existingManaged.Count -gt 0) {
            Write-Error ("Existing unmanaged Codex MCP sections found ({0}). " -f ($existingManaged -join ", ")) +
                "Refuse to overwrite; merge mcp\codex-mcp.template.toml manually."
        }
        elseif ([string]::IsNullOrWhiteSpace($configText)) {
            $newConfigText = $templateText + "`r`n"
        }
        else {
            $newConfigText = $configText.TrimEnd() + "`r`n`r`n" + $templateText + "`r`n"
        }
    }

    if ($WhatIf) {
        Write-Host "[WHATIF] Would write Codex MCP configuration"
    }
    else {
        $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
        [System.IO.File]::WriteAllText($CodexConfigPath, $newConfigText, $utf8NoBom)
        Write-Host "[OK] Codex MCP configured (restart Codex or start a new task)"
    }
}

$HooksSrc = Join-Path $Root "hooks"
$HookScript = Join-Path $HooksSrc "handoff-stop-check.py"
if (-not $SkipHooks -and (Test-Path $HookScript)) {
    $HookDstDir = Join-Path $env:USERPROFILE ".cursor\hooks"
    $HooksJsonPath = Join-Path $env:USERPROFILE ".cursor\hooks.json"
    $TemplatePath = Join-Path $HooksSrc "hooks.template.json"

    Write-Host "[COPY] hooks -> $HookDstDir"
    if (-not $WhatIf) {
        New-Item -ItemType Directory -Force -Path $HookDstDir | Out-Null
        Copy-Item $HookScript (Join-Path $HookDstDir "handoff-stop-check.py") -Force

        if (Test-Path $HooksJsonPath) {
            Write-Host "[WARN] hooks.json already exists: $HooksJsonPath"
            Write-Host "       Merge subagentStop/stop from hooks\hooks.template.json (see hooks\README.md)"
        }
        elseif (Test-Path $TemplatePath) {
            $hookDirEscaped = $HookDstDir -replace '\\', '/'
            $json = Get-Content $TemplatePath -Raw -Encoding UTF8
            $json = $json.Replace('{{HOOKS_DIR}}', $hookDirEscaped)
            Set-Content -Path $HooksJsonPath -Value $json -Encoding UTF8
            Write-Host "[OK] Wrote $HooksJsonPath"
        }
    }
}

if ($InstallMcp) {
    $McpTemplate = Join-Path $Root "mcp\mcp.template.json"
    $McpDst = Join-Path $env:USERPROFILE ".cursor\mcp.json"
    if (-not (Test-Path $McpTemplate)) {
        Write-Error "MCP template not found: $McpTemplate"
    }
    if (Test-Path $McpDst) {
        Write-Host "[WARN] mcp.json already exists: $McpDst"
        Write-Host "       Skip overwrite. Merge from mcp\mcp.template.json (see mcp\README.md)"
    }
    else {
        Write-Host "[COPY] mcp.template.json -> $McpDst"
        if (-not $WhatIf) {
            $cursorDir = Split-Path -Parent $McpDst
            New-Item -ItemType Directory -Force -Path $cursorDir | Out-Null
            Copy-Item $McpTemplate $McpDst -Force
            Write-Host "[OK] Wrote $McpDst (restart Cursor to load MCP)"
        }
    }
}

Write-Host "[NEXT] User Rules: see docs\user-rules-guide.md (user-rule-cursor-communication.md only)"
Write-Host "[NEXT] Handoff recovery (optional): skill agent-handoff-recovery"
Write-Host "[NEXT] MCP (optional): see mcp\README.md  or  .\scripts\install.ps1 -InstallMcp"
Write-Host "[NEXT] Codex global setup (no Cursor changes): .\scripts\install.ps1 -InstallCodex -SkipHooks"

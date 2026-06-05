#Requires -Version 5.1
<#
.SYNOPSIS
  bokujuu_cursorsetup の skills/ を %USERPROFILE%\.codex\skills\ へコピーする。
  hooks/ がある場合は %USERPROFILE%\.cursor\hooks\ と hooks.json も配置する。
#>
param(
    [switch]$WhatIf,
    [switch]$SkipHooks
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Src = Join-Path $Root "skills"
$Dst = Join-Path $env:USERPROFILE ".codex\skills"

if (-not (Test-Path $Src)) {
    Write-Error "skills folder not found: $Src"
}

New-Item -ItemType Directory -Force -Path $Dst | Out-Null

Get-ChildItem $Src -Directory | ForEach-Object {
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

Write-Host "[OK] Global skills installed under $Dst"

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

Write-Host "[NEXT] User Rules: see docs\user-rules-guide.md (core: user-rule-cursor-integrated.md only)"
Write-Host "[NEXT] Handoff recovery (optional): user-rule-agent-handoff-recovery.md + skill agent-handoff-recovery"
Write-Host "[NEXT] MCP (optional): see mcp\README.md"

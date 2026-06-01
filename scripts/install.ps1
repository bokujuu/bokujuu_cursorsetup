#Requires -Version 5.1
<#
.SYNOPSIS
  bokujuu_cursorsetup の skills/ を %USERPROFILE%\.codex\skills\ へコピーする。
#>
param(
    [switch]$WhatIf
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
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
Write-Host "[NEXT] User Rules: see docs\user-rules-guide.md (core: user-rule-cursor-integrated.md only)"
Write-Host "[NEXT] MCP (optional): see mcp\README.md"

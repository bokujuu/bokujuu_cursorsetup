#Requires -Version 5.1
<#
.SYNOPSIS
  ローカルの正（rulemaintenance + .codex/skills）から repo 内容を再生成する。
#>
param(
    [string]$RuleMaintenanceRoot = "C:\CursorPJs\rulemaintenance"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

$userRulesDst = Join-Path $Root "user-rules"
$skillsDst = Join-Path $Root "skills"
$docsDst = Join-Path $Root "docs"
$codexSkillsSrc = Join-Path $env:USERPROFILE ".codex\skills"

if (-not (Test-Path $RuleMaintenanceRoot)) {
    Write-Error "rulemaintenance not found: $RuleMaintenanceRoot"
}
if (-not (Test-Path $codexSkillsSrc)) {
    Write-Error "codex skills not found: $codexSkillsSrc"
}

Write-Host "[SYNC] user-rules from $RuleMaintenanceRoot"
Remove-Item "$userRulesDst\*" -Force -ErrorAction SilentlyContinue
Copy-Item (Join-Path $RuleMaintenanceRoot "user-rule-*.md") $userRulesDst

Write-Host "[SYNC] docs/rule-index.md"
New-Item -ItemType Directory -Force -Path $docsDst | Out-Null
Copy-Item (Join-Path $RuleMaintenanceRoot "docs\rule-index.md") $docsDst -Force

Write-Host "[SYNC] skills from $codexSkillsSrc (excluding .system)"
if (Test-Path $skillsDst) {
    Remove-Item $skillsDst -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $skillsDst | Out-Null
Get-ChildItem $codexSkillsSrc -Directory |
    Where-Object { $_.Name -ne ".system" } |
    ForEach-Object {
        Copy-Item $_.FullName (Join-Path $skillsDst $_.Name) -Recurse -Force
    }

Get-ChildItem $skillsDst -Recurse -Directory -Filter __pycache__ |
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "[OK] Sync complete. Review with: git status"

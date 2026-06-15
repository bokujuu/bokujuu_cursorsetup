#Requires -Version 5.1
<#
.SYNOPSIS
  Run one Ralph iteration via cursor-agent CLI (Tier 1 — workaround A).

.NOTES
  Windows: do NOT pipe PROMPT.md into cursor-agent -p (prompt is not received).
  Model: composer-2.5 (explicit; avoids account default composer-2.5-fast).
#>
[CmdletBinding()]
param(
    [string]$Workspace = (Get-Location).Path,
    [string]$PromptPath = (Join-Path $PSScriptRoot "PROMPT.md"),
    [string]$Model = "composer-2.5"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $PromptPath)) {
    throw "PROMPT not found: $PromptPath (copy PROMPT.md.template to PROMPT.md)"
}

$prompt = Get-Content -LiteralPath $PromptPath -Raw -Encoding UTF8
if ([string]::IsNullOrWhiteSpace($prompt)) {
    throw "PROMPT is empty: $PromptPath"
}

$agentArgs = @(
    "-p",
    "--force",
    "--trust",
    "--workspace", $Workspace,
    "--output-format", "text",
    "--model", $Model,
    $prompt
)

& cursor-agent @agentArgs
exit $LASTEXITCODE

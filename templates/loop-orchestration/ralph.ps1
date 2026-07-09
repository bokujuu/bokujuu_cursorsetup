#Requires -Version 5.1
<#
.SYNOPSIS
  Outer Ralph loop — fresh cursor-agent -p per iteration (Tier 1 — workaround A).

.PARAMETER MaxIterations
  Maximum number of agent invocations.

.PARAMETER StopOnComplete
  When set, stop early if agent outputs <promise>COMPLETE</promise>.
  Default: continue until MaxIterations (useful for loop verification).

.PARAMETER Model
  Passed to run-once.ps1. Default composer-2.5; use grok-4.5-xhigh (etc.) for hard iterations.

.EXAMPLE
  .\ralph.ps1 -MaxIterations 3
  .\ralph.ps1 -MaxIterations 5 -StopOnComplete
  .\ralph.ps1 -MaxIterations 3 -Model grok-4.5-xhigh
#>
[CmdletBinding()]
param(
    [int]$MaxIterations = 3,
    [switch]$StopOnComplete,
    [string]$Workspace = (Get-Location).Path,
    [string]$Model = "composer-2.5"
)

$ErrorActionPreference = "Stop"
$kitDir = $PSScriptRoot
$journal = Join-Path $kitDir "loop-journal.txt"
$iterationFile = Join-Path $kitDir "current-iteration.txt"
$runOnce = Join-Path $kitDir "run-once.ps1"

function Write-JournalLine([string]$Line) {
    $ts = Get-Date -Format "yyyy/MM/dd HH:mm"
    Add-Content -LiteralPath $journal -Encoding UTF8 -Value "$ts | $Line"
}

function Get-AgentPromise([string]$Output) {
    if ($Output -match '<promise>COMPLETE</promise>') { return "COMPLETE" }
    if ($Output -match '<promise>ITERATION_DONE</promise>') { return "ITERATION_DONE" }
    return "UNKNOWN"
}

if (-not (Test-Path -LiteralPath $runOnce)) {
    throw "run-once.ps1 not found in $kitDir"
}

Push-Location -LiteralPath $Workspace
try {
    for ($i = 1; $i -le $MaxIterations; $i++) {
        Set-Content -LiteralPath $iterationFile -Encoding UTF8 -Value "$i"
        Write-JournalLine "反復 $i/$MaxIterations 開始（オーケストレータ）"

        $output = & $runOnce -Workspace $Workspace -Model $Model 2>&1 | Out-String
        Write-Host $output

        $promise = Get-AgentPromise $output
        Write-JournalLine "反復 $i/$MaxIterations 終了 | agent: $promise"

        if ($StopOnComplete -and $promise -eq "COMPLETE") {
            break
        }
    }
}
finally {
    Pop-Location
}

exit 0

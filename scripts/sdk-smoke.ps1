#Requires -Version 5.1
<#
.SYNOPSIS
  Smoke-test stable SDK paths on Windows (Tier 2 F + optional Tier 2 B).

.NOTES
  Requires CURSOR_API_KEY. Does not use Python sync Client.launch_bridge.
#>
[CmdletBinding()]
param(
    [switch]$SkipPython,
    [switch]$SkipTypeScript
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$kitDir = Join-Path $repoRoot "templates\loop-orchestration"

if (-not $env:CURSOR_API_KEY) {
    throw "CURSOR_API_KEY is not set"
}

Write-Host "=== CLI smoke (Tier 1 reference) ==="
& cursor-agent -p --force --trust --workspace $repoRoot --output-format text --model composer-2.5 `
    "Reply with exactly: SDK_SMOKE_CLI_OK"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "[OK] CLI smoke"

if (-not $SkipTypeScript) {
    Write-Host "=== TypeScript @cursor/sdk smoke (Tier 2 F) ==="
    $smokeDir = Join-Path $repoRoot "temp\sdk-smoke-ts"
    if (-not (Test-Path (Join-Path $smokeDir "node_modules\@cursor\sdk"))) {
        New-Item -ItemType Directory -Force -Path $smokeDir | Out-Null
        Push-Location $smokeDir
        try {
            if (-not (Test-Path package.json)) {
                npm init -y | Out-Null
            }
            npm install @cursor/sdk 2>&1 | Out-Null
        }
        finally {
            Pop-Location
        }
    }
    $smokeScript = @'
import { Agent } from "@cursor/sdk";
const agent = await Agent.create({
  apiKey: process.env.CURSOR_API_KEY,
  model: { id: "composer-2.5" },
  local: { cwd: process.cwd() },
});
const run = await agent.send("Reply with exactly: SDK_SMOKE_TS_OK");
const result = await run.wait();
console.log(result.result?.trim());
if (typeof agent.dispose === "function") await agent.dispose();
'@
    $scriptPath = Join-Path $smokeDir "smoke.mjs"
    Set-Content -LiteralPath $scriptPath -Encoding UTF8 -Value $smokeScript
    Push-Location $repoRoot
    try {
        node $scriptPath
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }
    finally {
        Pop-Location
    }
    Write-Host "[OK] TypeScript SDK smoke"
}

if (-not $SkipPython) {
    Write-Host "=== Python AsyncClient smoke (Tier 2 B) ==="
    $py = @'
import asyncio
import os
from cursor_sdk import AsyncClient

async def main():
    async with await AsyncClient.launch_bridge(workspace=r"''' + $repoRoot.Replace('\', '\\') + '''") as client:
        agent = await client.agents.create(model="composer-2.5", api_key=os.environ["CURSOR_API_KEY"])
        run = await agent.send("Reply with exactly: SDK_SMOKE_PY_ASYNC_OK")
        result = await run.wait()
        print(result.result or result)

asyncio.run(main())
'@
    $pyPath = Join-Path $repoRoot "temp\sdk-smoke-async.py"
    New-Item -ItemType Directory -Force -Path (Split-Path $pyPath) | Out-Null
    Set-Content -LiteralPath $pyPath -Encoding UTF8 -Value $py
    python $pyPath
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "Python async smoke failed (cursor-sdk not installed?). Use -SkipPython to skip."
        exit $LASTEXITCODE
    }
    Write-Host "[OK] Python AsyncClient smoke"
}

Write-Host "sdk-smoke: all requested checks passed"

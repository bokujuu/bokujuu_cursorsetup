#Requires -Version 5.1
<#
.SYNOPSIS
  Start cursor-sdk-bridge manually and print env vars (Tier 3 — workaround C).

.DESCRIPTION
  Use when you need synchronous Python Client.connect() without launch_bridge.
  After running, set CURSOR_SDK_BRIDGE_URL and CURSOR_SDK_BRIDGE_AUTH_TOKEN in the session.
#>
[CmdletBinding()]
param(
    [string]$Workspace = (Get-Location).Path,
    [int]$TimeoutSeconds = 30
)

$ErrorActionPreference = "Stop"

$bridgeCmd = Get-Command cursor-sdk-bridge -ErrorAction SilentlyContinue
if (-not $bridgeCmd) {
    throw "cursor-sdk-bridge not on PATH. Install: pip install cursor-sdk"
}

$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $bridgeCmd.Source
$psi.Arguments = "--workspace `"$Workspace`""
$psi.RedirectStandardError = $true
$psi.UseShellExecute = $false
$psi.CreateNoWindow = $true

$proc = [System.Diagnostics.Process]::Start($psi)
$deadline = (Get-Date).AddSeconds($TimeoutSeconds)
$discovery = $null

while ((Get-Date) -lt $deadline) {
    if ($proc.StandardError.Peek() -ge 0) {
        $line = $proc.StandardError.ReadLine()
        if ($line -match 'cursor-sdk-bridge ready\s+(\{.*\})') {
            $discovery = $Matches[1] | ConvertFrom-Json
            break
        }
    }
    if ($proc.HasExited) { break }
    Start-Sleep -Milliseconds 100
}

if (-not $discovery) {
    throw "Timed out waiting for bridge discovery on stderr"
}

$url = $discovery.url
$tokenFile = $discovery.authTokenFile
if (-not $url -or -not $tokenFile) {
    throw "Discovery JSON missing url or authTokenFile"
}
$token = Get-Content -LiteralPath $tokenFile -Raw -Encoding UTF8

Write-Host "Bridge running (PID $($proc.Id)). Keep this window open."
Write-Host ""
Write-Host '$env:CURSOR_SDK_BRIDGE_URL = "' + $url + '"'
Write-Host '$env:CURSOR_SDK_BRIDGE_AUTH_TOKEN = "' + $token.Trim() + '"'
Write-Host ""
Write-Host "Python: from cursor_sdk import Client"
Write-Host 'with Client.connect(base_url=os.environ["CURSOR_SDK_BRIDGE_URL"], auth_token=...) as client: ...'

Wait-Process -Id $proc.Id

# Overflow dashboard launcher

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path $PSScriptRoot -Parent
$pythonSrc = Join-Path $repoRoot "python\src"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "python not found. Install Python first." -ForegroundColor Red
    exit 1
}

$env:PYTHONPATH = "$pythonSrc"

Write-Host "Starting Overflow gateway and opening dashboard..." -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the gateway." -ForegroundColor Yellow

Start-Sleep -Seconds 1
Start-Process "http://127.0.0.1:8080/dashboard"

python -m overflow.cli gateway --host 127.0.0.1 --port 8080

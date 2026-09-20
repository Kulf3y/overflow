# Install Overflow dependencies

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path $PSScriptRoot -Parent

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "python not found." -ForegroundColor Red
    exit 1
}

Write-Host "Installing Overflow dependencies..." -ForegroundColor Cyan
Set-Location $repoRoot
pip install -e python

if ($LASTEXITCODE -ne 0) {
    Write-Host "Install failed." -ForegroundColor Red
    exit 1
}

Write-Host "Dependencies installed." -ForegroundColor Green

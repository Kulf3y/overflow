# Overflow policy validation helper

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path $PSScriptRoot -Parent
$pythonSrc = Join-Path $repoRoot "python\src"
$defaultPolicy = Join-Path $repoRoot "policies\eu_default.json"
$strictPolicy = Join-Path $repoRoot "policies\eu_strict.json"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "python not found. Install Python first." -ForegroundColor Red
    Write-Host "You can install Python with:" -ForegroundColor Yellow
    Write-Host "winget install -e --id Python.Python.3.12" -ForegroundColor Cyan
    exit 1
}

$env:PYTHONPATH = "$pythonSrc"

Write-Host "Validating eu_default.json..." -ForegroundColor Cyan
python -m overflow.cli policy validate "$defaultPolicy"

if ($LASTEXITCODE -ne 0) {
    Write-Host "eu_default.json validation failed." -ForegroundColor Red
    exit 1
}

Write-Host "Validating eu_strict.json..." -ForegroundColor Cyan
python -m overflow.cli policy validate "$strictPolicy"

if ($LASTEXITCODE -ne 0) {
    Write-Host "eu_strict.json validation failed." -ForegroundColor Red
    exit 1
}

Write-Host "Policy validation passed." -ForegroundColor Green

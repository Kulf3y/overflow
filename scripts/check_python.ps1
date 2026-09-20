# Overflow Python test helper

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path $PSScriptRoot -Parent
$pythonSrc = Join-Path $repoRoot "python\src"
$testsPath = Join-Path $repoRoot "python\tests"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "python not found. Install Python first." -ForegroundColor Red
    Write-Host "You can install Python with:" -ForegroundColor Yellow
    Write-Host "winget install -e --id Python.Python.3.12" -ForegroundColor Cyan
    exit 1
}

Write-Host "Python version:" -ForegroundColor Cyan
python --version

Write-Host "Running Python tests..." -ForegroundColor Cyan

$env:PYTHONPATH = "$pythonSrc"
python -m unittest discover -s "$testsPath" -p "test_*.py"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Python tests failed." -ForegroundColor Red
    exit 1
}

Write-Host "Python tests passed." -ForegroundColor Green

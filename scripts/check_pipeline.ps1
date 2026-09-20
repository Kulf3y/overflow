# Overflow pipeline test helper

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

$env:PYTHONPATH = "$pythonSrc"

Write-Host "Running optimizer tests..." -ForegroundColor Cyan
python -m unittest discover -s "$testsPath" -p "test_optimizer.py"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Optimizer tests failed." -ForegroundColor Red
    exit 1
}

Write-Host "Running pipeline tests..." -ForegroundColor Cyan
python -m unittest discover -s "$testsPath" -p "test_pipeline.py"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Pipeline tests failed." -ForegroundColor Red
    exit 1
}

Write-Host "Pipeline tests passed." -ForegroundColor Green

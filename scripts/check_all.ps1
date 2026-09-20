# Overflow health check helper

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path $PSScriptRoot -Parent
$pythonSrc = Join-Path $repoRoot "python\src"
$testsPath = Join-Path $repoRoot "python\tests"
$rustManifest = Join-Path $repoRoot "rust\overflow-core\Cargo.toml"

$failed = $false

if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "Running Python tests..." -ForegroundColor Cyan
    $env:PYTHONPATH = "$pythonSrc"
    python -m unittest discover -s "$testsPath" -p "test_*.py"

    if ($LASTEXITCODE -ne 0) {
        Write-Host "Python tests failed." -ForegroundColor Red
        $failed = $true
    }
}
else {
    Write-Host "python not found. Skipping Python tests." -ForegroundColor Yellow
}

if (Get-Command cargo -ErrorAction SilentlyContinue) {
    Write-Host "Running Rust tests..." -ForegroundColor Cyan
    cargo test --manifest-path "$rustManifest"

    if ($LASTEXITCODE -ne 0) {
        Write-Host "Rust tests failed." -ForegroundColor Red
        $failed = $true
    }
}
else {
    Write-Host "cargo not found. Skipping Rust tests." -ForegroundColor Yellow
}

if ($failed) {
    Write-Host "Health check failed." -ForegroundColor Red
    exit 1
}

Write-Host "Health check passed." -ForegroundColor Green

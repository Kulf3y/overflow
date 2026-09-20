# Build the Rust to Python bridge (optional accelerator)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path $PSScriptRoot -Parent

if (-not (Get-Command cargo -ErrorAction SilentlyContinue)) {
    Write-Host "cargo not found. Install Rust from https://rustup.rs first." -ForegroundColor Yellow
    Write-Host "Overflow works fine without it (pure Python fallback)." -ForegroundColor Cyan
    exit 0
}

Write-Host "Installing maturin..." -ForegroundColor Cyan
pip install maturin

Write-Host "Building Rust bridge..." -ForegroundColor Cyan
maturin build --release -m (Join-Path $repoRoot "rust\overflow-py\Cargo.toml") -o (Join-Path $repoRoot "rust\dist")

if ($LASTEXITCODE -ne 0) {
    Write-Host "Rust bridge build failed. Python fallback remains active." -ForegroundColor Yellow
    exit 0
}

$wheel = Get-ChildItem (Join-Path $repoRoot "rust\dist") -Filter *.whl | Select-Object -First 1

if ($wheel) {
    Write-Host "Installing wheel: $($wheel.Name)" -ForegroundColor Cyan
    pip install $wheel.FullName --force-reinstall
    Write-Host "Rust bridge installed. Overflow will now use native speed." -ForegroundColor Green
} else {
    Write-Host "No wheel found." -ForegroundColor Yellow
}

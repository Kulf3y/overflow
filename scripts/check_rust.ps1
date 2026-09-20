# Overflow Rust test helper

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path $PSScriptRoot -Parent
$manifest = Join-Path $repoRoot "rust\overflow-core\Cargo.toml"

if (-not (Get-Command cargo -ErrorAction SilentlyContinue)) {
    Write-Host "cargo not found. Install Rust first." -ForegroundColor Red
    Write-Host "You can install Rust with:" -ForegroundColor Yellow
    Write-Host "winget install --id Rustlang.Rustup" -ForegroundColor Cyan
    exit 1
}

Write-Host "Running Rust tests..." -ForegroundColor Cyan
cargo test --manifest-path $manifest

if ($LASTEXITCODE -ne 0) {
    Write-Host "Rust tests failed." -ForegroundColor Red
    exit 1
}

Write-Host "Rust tests passed." -ForegroundColor Green

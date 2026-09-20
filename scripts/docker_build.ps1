# Overflow Docker build helper

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path $PSScriptRoot -Parent
$dockerfile = Join-Path $repoRoot "docker\Dockerfile"

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "docker not found. Install Docker first." -ForegroundColor Red
    exit 1
}

Write-Host "Building Overflow Docker image..." -ForegroundColor Cyan
docker build -f "$dockerfile" -t overflow:local "$repoRoot"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker build failed." -ForegroundColor Red
    exit 1
}

Write-Host "Docker image built: overflow:local" -ForegroundColor Green

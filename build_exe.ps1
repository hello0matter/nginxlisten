$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Entry = Join-Path $Root "nginx_trace_hunter.py"
$Dist = Join-Path $Root "dist"
$Build = Join-Path $Root "build"
$Spec = Join-Path $Root "nginx-trace-hunter.spec"

if (-not (Test-Path $Entry)) {
    throw "Entry script not found: $Entry"
}

Write-Host "Checking Python..."
python --version

Write-Host "Checking PyInstaller..."
python -m PyInstaller --version | Out-Host

Write-Host "Cleaning old build outputs..."
Remove-Item -Recurse -Force $Build -ErrorAction SilentlyContinue
Remove-Item -Force $Spec -ErrorAction SilentlyContinue

Write-Host "Building nginx-trace-hunter.exe..."
python -m PyInstaller `
    --noconfirm `
    --clean `
    --onefile `
    --console `
    --name nginx-trace-hunter `
    $Entry

$Exe = Join-Path $Dist "nginx-trace-hunter.exe"
if (-not (Test-Path $Exe)) {
    throw "Build failed, exe not found: $Exe"
}

Write-Host ""
Write-Host "Build complete:"
Write-Host $Exe
Write-Host ""
Write-Host "Quick usage:"
Write-Host "  .\dist\nginx-trace-hunter.exe --gui"
Write-Host "  .\dist\nginx-trace-hunter.exe D:\nginx\logs --once --output-dir D:\hunter-output"
Write-Host "  .\dist\nginx-trace-hunter.exe D:\nginx\logs --interval 30 --output-dir D:\hunter-output"

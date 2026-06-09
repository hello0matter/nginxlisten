$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Entry = Join-Path $Root "nginx_trace_hunter.py"
$Dist = Join-Path $Root "dist"
$Build = Join-Path $Root "build"
$Spec = Join-Path $Root "nginx-trace-hunter-server.spec"
$Package = Join-Path $Dist "nginx-trace-hunter-server-dir.zip"

if (-not (Test-Path $Entry)) {
    throw "Entry script not found: $Entry"
}

Write-Host "Checking Python..."
python --version

Write-Host "Checking PyInstaller..."
python -m PyInstaller --version | Out-Host

Write-Host "Cleaning old server build outputs..."
Remove-Item -Recurse -Force $Build -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force (Join-Path $Dist "nginx-trace-hunter-server") -ErrorAction SilentlyContinue
Remove-Item -Force $Spec -ErrorAction SilentlyContinue
Remove-Item -Force $Package -ErrorAction SilentlyContinue

Write-Host "Building onedir server package..."
python -m PyInstaller `
    --noconfirm `
    --clean `
    --onedir `
    --console `
    --name nginx-trace-hunter-server `
    $Entry

$Exe = Join-Path $Dist "nginx-trace-hunter-server\nginx-trace-hunter-server.exe"
if (-not (Test-Path $Exe)) {
    throw "Build failed, exe not found: $Exe"
}

$AppDir = Join-Path $Dist "nginx-trace-hunter-server"
Copy-Item (Join-Path $Root "config.example.windows.json") $AppDir -ErrorAction SilentlyContinue
Copy-Item (Join-Path $Root "install_windows_task.ps1") $AppDir -ErrorAction SilentlyContinue
Copy-Item (Join-Path $Root "README.md") $AppDir -ErrorAction SilentlyContinue

Write-Host "Creating zip package..."
tar -a -c -f $Package -C $Dist "nginx-trace-hunter-server"

Write-Host ""
Write-Host "Server build complete:"
Write-Host $Exe
Write-Host $Package
Write-Host ""
Write-Host "Quick usage after unzip:"
Write-Host "  .\nginx-trace-hunter-server\nginx-trace-hunter-server.exe --help"
Write-Host "  .\nginx-trace-hunter-server\nginx-trace-hunter-server.exe D:\nginx\logs --once --output-dir D:\hunter-output"
Write-Host "  .\nginx-trace-hunter-server\nginx-trace-hunter-server.exe D:\nginx\logs --interval 30 --output-dir D:\hunter-output"

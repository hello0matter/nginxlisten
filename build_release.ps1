$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Dist = Join-Path $Root "dist"

Write-Host "== Build Windows onefile =="
& powershell.exe -ExecutionPolicy Bypass -File (Join-Path $Root "build_exe.ps1")

Write-Host ""
Write-Host "== Build Windows server onedir =="
& powershell.exe -ExecutionPolicy Bypass -File (Join-Path $Root "build_server_dir.ps1")

Write-Host ""
Write-Host "== Package Linux/CentOS source builder =="
New-Item -ItemType Directory -Force $Dist | Out-Null
Remove-Item -Force (Join-Path $Dist "nginx-trace-hunter-linux-source.tar.gz") -ErrorAction SilentlyContinue
tar -czf (Join-Path $Dist "nginx-trace-hunter-linux-source.tar.gz") `
    nginx_trace_hunter.py `
    build_linux_centos.sh `
    build_linux_portable.ps1 `
    install_linux_service.sh `
    linux_setup.sh `
    config.example.linux.json `
    config.example.windows.json `
    README.md

Write-Host ""
Write-Host "== Package Linux portable runtime =="
& powershell.exe -ExecutionPolicy Bypass -File (Join-Path $Root "build_linux_portable.ps1")

Write-Host ""
Write-Host "== Package pure source zip =="
Remove-Item -Force (Join-Path $Dist "nginx-trace-hunter-source.zip") -ErrorAction SilentlyContinue
tar -a -c -f (Join-Path $Dist "nginx-trace-hunter-source.zip") `
    nginx_trace_hunter.py `
    build_exe.ps1 `
    build_server_dir.ps1 `
    build_linux_centos.sh `
    build_linux_portable.ps1 `
    install_linux_service.sh `
    install_windows_task.ps1 `
    linux_setup.sh `
    config.example.linux.json `
    config.example.windows.json `
    README.md

Write-Host ""
Write-Host "Release artifacts:"
Get-ChildItem $Dist -File | Sort-Object Name | Select-Object Name,Length | Format-Table -AutoSize

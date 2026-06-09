param(
    [string]$TaskName = "NginxTraceHunter",
    [string]$LogDir = "",
    [string]$OutputDir = "",
    [string]$Interval = "30",
    [switch]$NoStart,
    [switch]$Uninstall
)

$ErrorActionPreference = "Stop"

$AppDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Exe = Join-Path $AppDir "nginx-trace-hunter-server.exe"
$ConfigFile = Join-Path $AppDir "config.json"

function Ask-Value([string]$Prompt, [string]$Default) {
    $value = Read-Host "$Prompt [$Default]"
    if ([string]::IsNullOrWhiteSpace($value)) {
        return $Default
    }
    return $value
}

function Ask-YesNo([string]$Prompt, [string]$Default = "Y") {
    $value = Read-Host "$Prompt [$Default]"
    if ([string]::IsNullOrWhiteSpace($value)) {
        $value = $Default
    }
    return $value -match "^[Yy]"
}

if ($Uninstall) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "Scheduled task removed: $TaskName"
    exit 0
}

if (-not (Test-Path $Exe)) {
    throw "Executable not found: $Exe. Put this script in the same directory as nginx-trace-hunter-server.exe."
}

if ([string]::IsNullOrWhiteSpace($LogDir)) {
    $LogDir = Ask-Value -Prompt 'Nginx log directory' -Default 'D:\nginx\logs'
}
if ([string]::IsNullOrWhiteSpace($OutputDir)) {
    $OutputDir = Ask-Value -Prompt 'Output directory' -Default 'D:\nginx-trace-hunter\output'
}
if ([string]::IsNullOrWhiteSpace($Interval)) {
    $Interval = Ask-Value -Prompt 'Polling interval seconds' -Default '30'
}

$StateFile = Join-Path (Split-Path -Parent $OutputDir) "state.json"
New-Item -ItemType Directory -Force $OutputDir | Out-Null
New-Item -ItemType Directory -Force (Split-Path -Parent $StateFile) | Out-Null

$config = [ordered]@{
    inputs = @($LogDir)
    search_roots = @()
    output_dir = $OutputDir
    state_file = $StateFile
    top_n = 20
    from_date = ""
    to_date = ""
    archive_mode = "auto"
    mode = "resident"
    interval_sec = [int]$Interval
    bootstrap_bytes = 67108864
    discover_every = 12
    ai_enabled = $false
    ai_base_url = ""
    ai_model = ""
    ai_api_key = ""
    ai_prompt = ""
    alert_enabled = $false
    alert_min_score = 30.0
    ding_url = ""
    ding_kw = ""
    wx_url = ""
    fs_url = ""
}

$config | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 $ConfigFile
Write-Host "Config generated: $ConfigFile"

$InstallTask = Ask-YesNo -Prompt 'Install as startup background scheduled task' -Default 'Y'
if (-not $InstallTask) {
    Write-Host "Manual start command:"
    Write-Host "`"$Exe`" --cfg `"$ConfigFile`""
    $StartBackground = Ask-YesNo -Prompt 'Start once in background now' -Default 'Y'
    if ($StartBackground) {
        Start-Process -FilePath $Exe -ArgumentList @("--cfg", $ConfigFile) -WorkingDirectory $AppDir -WindowStyle Hidden
        Write-Host "Started in background. Log: $OutputDir\hunter.log"
    }
    exit 0
}

$action = New-ScheduledTaskAction -Execute $Exe -Argument "--cfg `"$ConfigFile`"" -WorkingDirectory $AppDir
$trigger = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)

$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if ($isAdmin) {
    $principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -RunLevel Highest
} else {
    $principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited
}

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force | Out-Null
Write-Host "Scheduled task created: $TaskName"

$StartTask = Ask-YesNo -Prompt 'Start task now' -Default 'Y'
if (-not $NoStart -and $StartTask) {
    Start-ScheduledTask -TaskName $TaskName
    Write-Host "Task started."
}

Write-Host "Status: Get-ScheduledTask -TaskName $TaskName"
Write-Host "Stop:   Stop-ScheduledTask -TaskName $TaskName"
Write-Host "Remove: .\install_windows_task.ps1 -Uninstall"
Write-Host "Log:    $OutputDir\hunter.log"

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonArchive = Join-Path $Root ".cache\cpython-linux-x86_64.tar.gz"
$OutPackage = Join-Path $Root "dist\nginx-trace-hunter-linux-portable.tar.gz"
$Image = "quay.io/pypa/manylinux2014_x86_64"
$DockerScript = Join-Path $Root ".cache\build_linux_portable.sh"

if (-not (Test-Path $PythonArchive)) {
    throw "Standalone Python archive not found: $PythonArchive"
}

New-Item -ItemType Directory -Force (Join-Path $Root ".cache") | Out-Null
New-Item -ItemType Directory -Force (Join-Path $Root "dist") | Out-Null

@'
set -euo pipefail
rm -rf /tmp/nthpkg /tmp/nthtest
mkdir -p /tmp/nthpkg/nginx-trace-hunter-linux-portable
tar -xzf /src/.cache/cpython-linux-x86_64.tar.gz -C /tmp/nthpkg/nginx-trace-hunter-linux-portable
cp /src/nginx_trace_hunter.py /tmp/nthpkg/nginx-trace-hunter-linux-portable/
cp /src/README.md /tmp/nthpkg/nginx-trace-hunter-linux-portable/ 2>/dev/null || true
cp /src/config.example.linux.json /tmp/nthpkg/nginx-trace-hunter-linux-portable/ 2>/dev/null || true
cp /src/linux_setup.sh /tmp/nthpkg/nginx-trace-hunter-linux-portable/ 2>/dev/null || true

cat > /tmp/nthpkg/nginx-trace-hunter-linux-portable/nginx-trace-hunter <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$APP_DIR/python/bin/python3" "$APP_DIR/nginx_trace_hunter.py" "$@"
EOF

cat > /tmp/nthpkg/nginx-trace-hunter-linux-portable/run-resident.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="${LOG_DIR:-/var/log/nginx}"
OUTPUT_DIR="${OUTPUT_DIR:-$APP_DIR/output}"
INTERVAL="${INTERVAL:-30}"
exec "$APP_DIR/nginx-trace-hunter" "$LOG_DIR" --interval "$INTERVAL" --output-dir "$OUTPUT_DIR"
EOF

chmod +x \
  /tmp/nthpkg/nginx-trace-hunter-linux-portable/nginx-trace-hunter \
  /tmp/nthpkg/nginx-trace-hunter-linux-portable/run-resident.sh \
  /tmp/nthpkg/nginx-trace-hunter-linux-portable/linux_setup.sh \
  /tmp/nthpkg/nginx-trace-hunter-linux-portable/python/bin/python*

tar -C /tmp/nthpkg -czf /src/dist/nginx-trace-hunter-linux-portable.tar.gz nginx-trace-hunter-linux-portable

mkdir -p /tmp/nthtest
tar -xzf /src/dist/nginx-trace-hunter-linux-portable.tar.gz -C /tmp/nthtest
/tmp/nthtest/nginx-trace-hunter-linux-portable/nginx-trace-hunter --help >/tmp/nth_help.txt
grep -q "Nginx" /tmp/nth_help.txt
'@ | Set-Content -Encoding ASCII $DockerScript

$DockerScriptText = Get-Content -Raw $DockerScript
$DockerScriptText = $DockerScriptText -replace "`r`n", "`n"
[System.IO.File]::WriteAllText($DockerScript, $DockerScriptText, [System.Text.Encoding]::ASCII)

docker run --rm `
    -v "${Root}:/src" `
    -w /src `
    $Image `
    /bin/bash /src/.cache/build_linux_portable.sh

if (-not (Test-Path $OutPackage)) {
    throw "Linux portable package not found: $OutPackage"
}

Get-Item $OutPackage | Select-Object FullName,Length | Format-Table -AutoSize

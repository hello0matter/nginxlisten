#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/nginx-trace-hunter}"
LOG_DIR="${LOG_DIR:-/var/log/nginx}"
OUTPUT_DIR="${OUTPUT_DIR:-$APP_DIR/output}"
INTERVAL="${INTERVAL:-30}"
SERVICE_NAME="${SERVICE_NAME:-nginx-trace-hunter}"
RUN_USER="${RUN_USER:-root}"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXE="$ROOT/nginx-trace-hunter-linux/nginx-trace-hunter-linux"

if [[ ! -x "$EXE" ]]; then
  echo "Executable not found: $EXE" >&2
  echo "Run this script from the extracted package parent directory, or set APP_DIR manually after copying files." >&2
  exit 1
fi

if [[ "$(id -u)" -ne 0 ]]; then
  echo "Please run as root." >&2
  exit 1
fi

mkdir -p "$APP_DIR" "$OUTPUT_DIR"
cp -a "$ROOT/nginx-trace-hunter-linux" "$APP_DIR/"

cat > "/etc/systemd/system/${SERVICE_NAME}.service" <<EOF
[Unit]
Description=Nginx Trace Hunter resident analyzer
After=network.target

[Service]
Type=simple
User=${RUN_USER}
WorkingDirectory=${APP_DIR}
ExecStart=${APP_DIR}/nginx-trace-hunter-linux/nginx-trace-hunter-linux ${LOG_DIR} --interval ${INTERVAL} --output-dir ${OUTPUT_DIR}
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable "$SERVICE_NAME"

echo "Installed systemd service: $SERVICE_NAME"
echo "Start:   systemctl start $SERVICE_NAME"
echo "Status:  systemctl status $SERVICE_NAME"
echo "Logs:    journalctl -u $SERVICE_NAME -f"
echo "Report:  $OUTPUT_DIR/hunter.log"

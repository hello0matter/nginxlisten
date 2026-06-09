#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="${SERVICE_NAME:-nginx-trace-hunter}"
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${CONFIG_FILE:-$APP_DIR/config.json}"

usage() {
  cat <<EOF
Usage: $0 <command>

Commands:
  status       Show systemd service status
  restart      Restart systemd service after config/software changes
  stop         Stop systemd service
  start        Start systemd service
  logs         Follow service journal logs
  app-log      Follow hunter.log from configured output_dir
  edit-config  Open config.json with vi
  show-config  Print config.json
  test-once    Run one analysis cycle with current config
  reset-state  Stop service and remove configured state_file

Environment:
  SERVICE_NAME=nginx-trace-hunter
  CONFIG_FILE=$APP_DIR/config.json
EOF
}

config_value() {
  local key="$1"
  "$APP_DIR/python/bin/python3" - "$CONFIG_FILE" "$key" <<'PY'
import json, sys
path, key = sys.argv[1], sys.argv[2]
with open(path, "r", encoding="utf-8-sig") as f:
    data = json.load(f)
print(data.get(key, ""))
PY
}

cmd="${1:-}"
case "$cmd" in
  status)
    systemctl status "$SERVICE_NAME"
    ;;
  restart)
    systemctl daemon-reload
    systemctl restart "$SERVICE_NAME"
    systemctl status "$SERVICE_NAME" --no-pager
    ;;
  stop)
    systemctl stop "$SERVICE_NAME"
    ;;
  start)
    systemctl start "$SERVICE_NAME"
    ;;
  logs)
    journalctl -u "$SERVICE_NAME" -f
    ;;
  app-log)
    output_dir="$(config_value output_dir)"
    tail -f "$output_dir/hunter.log"
    ;;
  edit-config)
    vi "$CONFIG_FILE"
    ;;
  show-config)
    cat "$CONFIG_FILE"
    ;;
  test-once)
    "$APP_DIR/nginx-trace-hunter" --cfg "$CONFIG_FILE" --once
    ;;
  reset-state)
    state_file="$(config_value state_file)"
    systemctl stop "$SERVICE_NAME" || true
    rm -f "$state_file"
    echo "Removed state file: $state_file"
    echo "Start again: systemctl start $SERVICE_NAME"
    ;;
  *)
    usage
    exit 1
    ;;
esac

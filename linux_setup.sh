#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXE="$APP_DIR/nginx-trace-hunter"
DEFAULT_CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/nginx_trace_hunter"
CONFIG_FILE="${CONFIG_FILE:-$DEFAULT_CONFIG_DIR/config.json}"

if [[ ! -x "$EXE" ]]; then
  echo "Executable not found: $EXE" >&2
  exit 1
fi

ask() {
  local prompt="$1"
  local default_value="$2"
  local value
  read -r -p "$prompt [$default_value]: " value || true
  echo "${value:-$default_value}"
}

ask_yes_no() {
  local prompt="$1"
  local default_value="$2"
  local value
  read -r -p "$prompt [$default_value]: " value || true
  value="${value:-$default_value}"
  [[ "$value" =~ ^[Yy] ]]
}

json_get() {
  local key="$1"
  "$APP_DIR/python/bin/python3" - "$CONFIG_FILE" "$key" <<'PY'
import json, sys
path, key = sys.argv[1], sys.argv[2]
try:
    with open(path, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}
print(data.get(key, ""))
PY
}

if [[ -f "$CONFIG_FILE" ]] && ask_yes_no "发现系统配置 $CONFIG_FILE，是否直接使用" "y"; then
  OUTPUT_DIR="$(json_get output_dir)"
  if [[ -z "$OUTPUT_DIR" ]]; then
    OUTPUT_DIR="$APP_DIR/output"
  fi
  echo "使用已有配置: $CONFIG_FILE"
else
  LOG_DIR="$(ask 'Nginx 日志目录' '/var/log/nginx')"
  OUTPUT_DIR="$(ask '输出目录' "$APP_DIR/output")"
  STATE_FILE="$(ask '状态文件' "$APP_DIR/state.json")"
  INTERVAL="$(ask '轮询间隔秒' '30')"
  ALERT_MIN="$(ask '告警阈值' '30')"

  mkdir -p "$(dirname "$CONFIG_FILE")" "$OUTPUT_DIR" "$(dirname "$STATE_FILE")"

  cat > "$CONFIG_FILE" <<EOF
{
  "inputs": [
    "$LOG_DIR"
  ],
  "search_roots": [],
  "output_dir": "$OUTPUT_DIR",
  "state_file": "$STATE_FILE",
  "top_n": 20,
  "from_date": "",
  "to_date": "",
  "archive_mode": "auto",
  "mode": "resident",
  "interval_sec": $INTERVAL,
  "bootstrap_bytes": 67108864,
  "discover_every": 12,
  "ai_enabled": false,
  "ai_base_url": "",
  "ai_model": "",
  "ai_api_key": "",
  "ai_prompt": "",
  "alert_enabled": false,
  "alert_min_score": $ALERT_MIN,
  "ding_url": "",
  "ding_kw": "",
  "wx_url": "",
  "fs_url": ""
}
EOF

  echo "配置已生成: $CONFIG_FILE"
fi

mkdir -p "$OUTPUT_DIR"

if ask_yes_no "是否安装为 systemd 服务" "y"; then
  if [[ "$(id -u)" -ne 0 ]]; then
    echo "安装 systemd 服务需要 root，请使用 sudo 重新运行。" >&2
    exit 1
  fi
  SERVICE_NAME="$(ask '服务名' 'nginx-trace-hunter')"
  cat > "/etc/systemd/system/${SERVICE_NAME}.service" <<EOF
[Unit]
Description=Nginx Trace Hunter resident analyzer
After=network.target

[Service]
Type=simple
WorkingDirectory=$APP_DIR
ExecStart=$EXE --cfg $CONFIG_FILE
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
  systemctl daemon-reload
  systemctl enable "$SERVICE_NAME"
  if ask_yes_no "是否立即启动服务" "y"; then
    systemctl restart "$SERVICE_NAME"
  fi
  echo "服务已安装: $SERVICE_NAME"
  echo "查看状态: systemctl status $SERVICE_NAME"
  echo "查看日志: journalctl -u $SERVICE_NAME -f"
  echo "报告日志: $OUTPUT_DIR/hunter.log"
else
  if ask_yes_no "是否使用 nohup 后台启动" "y"; then
    nohup "$EXE" --cfg "$CONFIG_FILE" > "$OUTPUT_DIR/console.log" 2>&1 &
    echo $! > "$OUTPUT_DIR/pid"
    echo "已后台启动，PID: $(cat "$OUTPUT_DIR/pid")"
    echo "查看日志: tail -f $OUTPUT_DIR/console.log"
    echo "停止命令: kill $(cat "$OUTPUT_DIR/pid")"
  else
    echo "手动启动命令:"
    echo "$EXE --cfg $CONFIG_FILE"
  fi
fi

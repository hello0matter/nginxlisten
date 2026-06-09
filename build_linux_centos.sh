#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENTRY="$ROOT/nginx_trace_hunter.py"
PYTHON_BIN="${PYTHON_BIN:-python3}"
APP_NAME="nginx-trace-hunter-linux"
DIST_DIR="$ROOT/dist"
BUILD_DIR="$ROOT/build"
PACKAGE="$DIST_DIR/${APP_NAME}-centos.tar.gz"

if [[ ! -f "$ENTRY" ]]; then
  echo "Entry script not found: $ENTRY" >&2
  exit 1
fi

echo "Checking Python..."
"$PYTHON_BIN" --version

echo "Checking PyInstaller..."
if ! "$PYTHON_BIN" -m PyInstaller --version >/dev/null 2>&1; then
  echo "PyInstaller not found, installing for current user..."
  "$PYTHON_BIN" -m pip install --user pyinstaller
fi
"$PYTHON_BIN" -m PyInstaller --version

echo "Cleaning old build outputs..."
rm -rf "$BUILD_DIR" "$DIST_DIR/$APP_NAME" "$PACKAGE" "$ROOT/${APP_NAME}.spec"
mkdir -p "$DIST_DIR"

echo "Building Linux onedir package..."
"$PYTHON_BIN" -m PyInstaller \
  --noconfirm \
  --clean \
  --onedir \
  --console \
  --name "$APP_NAME" \
  --exclude-module tkinter \
  --exclude-module _tkinter \
  "$ENTRY"

EXE="$DIST_DIR/$APP_NAME/$APP_NAME"
if [[ ! -x "$EXE" ]]; then
  echo "Build failed, executable not found: $EXE" >&2
  exit 1
fi

echo "Creating tar.gz package..."
tar -C "$DIST_DIR" -czf "$PACKAGE" "$APP_NAME"

echo
echo "Linux build complete:"
echo "  $EXE"
echo "  $PACKAGE"
echo
echo "Quick usage after extract:"
echo "  ./$APP_NAME/$APP_NAME --help"
echo "  ./$APP_NAME/$APP_NAME /var/log/nginx --once --output-dir /opt/nginx-trace-hunter/output"
echo "  ./$APP_NAME/$APP_NAME /var/log/nginx --interval 30 --output-dir /opt/nginx-trace-hunter/output"

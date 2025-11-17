#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT_DIR"

API_HOST=${API_HOST:-$(hostname -I | awk '{print $1}' || echo "localhost")}
BACKEND_PORT=${BACKEND_PORT:-8000}
FRONTEND_PORT=${FRONTEND_PORT:-5173}

if ! command -v pm2 >/dev/null 2>&1; then
  echo "[ERROR] pm2 is not installed. Run install_ubuntu.sh first." >&2
  exit 1
fi

if [[ ! -x "$ROOT_DIR/backend/venv/bin/uvicorn" ]]; then
  echo "[ERROR] Backend virtualenv missing at $ROOT_DIR/backend/venv. Run install_ubuntu.sh." >&2
  exit 1
fi

export PYTHONPATH="$ROOT_DIR/backend"
source "$ROOT_DIR/backend/venv/bin/activate"

# Clean up any stale PM2 processes to avoid duplicate instances
pm2 delete deepguard-backend >/dev/null 2>&1 || true
pm2 delete deepguard-frontend >/dev/null 2>&1 || true

BACKEND_CMD=(pm2 start "$ROOT_DIR/backend/venv/bin/uvicorn" --interpreter none --name deepguard-backend --cwd "$ROOT_DIR/backend" -- \
  app.main:app --host 0.0.0.0 --port "$BACKEND_PORT" --reload)
"${BACKEND_CMD[@]}"

pm2 start "npm run dev -- --host --port ${FRONTEND_PORT}" --name deepguard-frontend --cwd "$ROOT_DIR/frontend"

# Persist and report status
pm2 save >/dev/null 2>&1 || true
pm2 status deepguard-backend deepguard-frontend || true

echo "[INFO] Waiting for backend to respond on http://${API_HOST}:${BACKEND_PORT} ..."
for _ in {1..15}; do
  if curl -fsS "http://${API_HOST}:${BACKEND_PORT}" >/dev/null 2>&1; then
    echo "[INFO] Backend is reachable on http://${API_HOST}:${BACKEND_PORT}"
    exit 0
  fi
  sleep 1
done

echo "[ERROR] Backend is not responding on http://${API_HOST}:${BACKEND_PORT}. Showing recent PM2 logs:"
pm2 logs deepguard-backend --lines 80 || true
exit 1

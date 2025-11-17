#!/usr/bin/env bash
set -e
ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT_DIR"
export PYTHONPATH="$ROOT_DIR/backend"
source backend/venv/bin/activate
pm2 start backend/venv/bin/uvicorn --name deepguard-backend --cwd "$ROOT_DIR/backend" -- app.main:app --host 0.0.0.0 --port 8000 --reload || true
pm2 start "npm run dev -- --host" --name deepguard-frontend --cwd "$ROOT_DIR/frontend" || true

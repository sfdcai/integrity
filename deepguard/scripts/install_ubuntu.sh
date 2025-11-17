#!/usr/bin/env bash
set -euo pipefail
set -x

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT_DIR"

# Packages
apt-get update
apt-get install -y curl software-properties-common
if ! command -v python3.12 >/dev/null; then
  add-apt-repository -y ppa:deadsnakes/ppa
  apt-get update
  apt-get install -y python3.12 python3.12-venv python3-distutils
fi
if ! command -v node >/dev/null || [[ $(node -v) != v20* ]]; then
  curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
  apt-get install -y nodejs
fi
npm install -g pm2 pm2-logrotate

# Backend setup
export PYTHONPATH="$ROOT_DIR/backend"
python3.12 -m venv backend/venv
source backend/venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt
cd backend
python - <<PY
from app.database import init_db
init_db()
PY
python - <<PY
from app.database import SessionLocal
from app.services.seed import seed_admin, seed_sample_well
from app.database import init_db
init_db()
db = SessionLocal()
seed_admin(db)
seed_sample_well(db)
db.close()
PY
cd "$ROOT_DIR"

# Frontend setup
cd frontend
npm install
cd ..

# PM2 processes
pm2 start backend/venv/bin/uvicorn --interpreter none --name deepguard-backend --cwd "$ROOT_DIR/backend" -- app.main:app --host 0.0.0.0 --port 8000 --reload
pm2 start "npm run dev -- --host" --name deepguard-frontend --cwd "$ROOT_DIR/frontend"
pm2 save
pm2-logrotate
pm2 startup systemd -u $(whoami) --hp $(eval echo ~$(whoami))

# Quick health hints
pm2 status deepguard-backend deepguard-frontend || true
if command -v curl >/dev/null 2>&1; then
  API_HOST=${API_HOST:-$(hostname -I | awk '{print $1}')}
  curl -f "http://${API_HOST}:8000" >/dev/null 2>&1 && echo "[INFO] Backend reachable on http://${API_HOST}:8000" || echo "[WARN] Backend not yet responding on http://${API_HOST}:8000"
fi

printf "Backend API: http://$(hostname -I | awk '{print $1}'):8000/docs\n"
printf "Frontend UI: http://$(hostname -I | awk '{print $1}'):5173\n"

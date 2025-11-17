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

# PM2 processes (single instance each)
cd "$ROOT_DIR"
bash scripts/start.sh
pm2-logrotate
pm2 startup systemd -u $(whoami) --hp $(eval echo ~$(whoami))

# Post-start validation
bash scripts/healthcheck.sh || true

printf "Backend API: http://$(hostname -I | awk '{print $1}'):8000/docs\n"
printf "Frontend UI: http://$(hostname -I | awk '{print $1}'):5173\n"

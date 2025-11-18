#!/usr/bin/env bash
set -e

# Install system dependencies
sudo apt-get update
sudo apt-get install -y python3.12 python3.12-venv python3-pip sqlite3 curl

# Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Backend setup
cd "$(dirname "$0")/.."/deepguard/backend
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
npm run build

# PM2 install
sudo npm install -g pm2 pm2-logrotate

# Environment
cd ..
cat > .env <<EENV
SECRET_KEY=${SECRET_KEY:-super-secret-key}
DATABASE_URL=${DATABASE_URL:-sqlite:///./deepguard.db}
EENV

# Start backend with PM2
cd backend
pm2 start venv/bin/uvicorn --name deepguard-backend -- app.main:app --host 0.0.0.0 --port 8000

# Serve frontend
cd ../frontend
pm2 start npm --name deepguard-frontend -- run dev -- --host --port 5173

pm2 save
pm2 startup systemd -u $USER --hp $HOME

HOST_IP=$(hostname -I | awk '{print $1}')
printf "Backend API: http://${HOST_IP:-<server-ip>}:8000/docs\n"
printf "Frontend UI: http://${HOST_IP:-<server-ip>}:5173\n"

# Setup Guide

## Requirements
- Python 3.12
- Node.js 20
- SQLite

## Backend
```
cd deepguard/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Bind to all interfaces if accessed from another machine on the network
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Frontend
```
cd deepguard/frontend
npm install
# Expose Vite dev server to the network
npm run dev -- --host --port 5173
```

See `scripts/install_ubuntu.sh` for the automated installer that provisions PM2 processes and dependencies on Ubuntu.

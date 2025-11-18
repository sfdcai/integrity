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
uvicorn app.main:app --reload
```

## Frontend
```
cd deepguard/frontend
npm install
npm run dev
```

See `scripts/install_ubuntu.sh` for the automated installer that provisions PM2 processes and dependencies on Ubuntu.

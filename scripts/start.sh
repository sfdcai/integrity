#!/usr/bin/env bash

# Start (or restart) backend and frontend with network-accessible hosts
pm2 describe deepguard-backend >/dev/null 2>&1 || \
  pm2 start deepguard/backend/venv/bin/uvicorn --name deepguard-backend -- app.main:app --host 0.0.0.0 --port 8000

pm2 describe deepguard-frontend >/dev/null 2>&1 || \
  (cd deepguard/frontend && pm2 start npm --name deepguard-frontend -- run dev -- --host --port 5173)

pm2 save

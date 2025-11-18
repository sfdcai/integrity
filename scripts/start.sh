#!/usr/bin/env bash
pm2 start deepguard-backend || pm2 start deepguard/backend/venv/bin/uvicorn --name deepguard-backend -- app.main:app --host 0.0.0.0 --port 8000
pm2 start deepguard-frontend || (cd deepguard/frontend && pm2 start npm --name deepguard-frontend -- run dev -- --host --port 5173)
pm2 save

# Setup Guide

1. Run `sudo bash scripts/install_ubuntu.sh` inside the `deepguard` directory.
2. The script installs Python 3.12, Node 20, PM2, provisions the SQLite DB, seeds admin + sample well, and starts backend/frontend.
3. Default login: `admin@deepguard.io / admin`.
4. Control processes with `scripts/start.sh`, `scripts/stop.sh`, `scripts/restart.sh`.
5. Run `bash scripts/healthcheck.sh` to verify ports 8000/5173 are reachable; it will restart PM2 services and print recent logs if not.
6. Environment variables: `DEEPGUARD_DB_PATH` to override database location; `VITE_API_URL` to point frontend at remote API (e.g., `http://<server-ip>:8000`).

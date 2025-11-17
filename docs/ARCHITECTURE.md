# Architecture

- **Backend**: FastAPI + SQLAlchemy (SQLite). Modules: wells, annuli, critical points, measurements, barrier elements, tasks, integrity engine, JWT auth. Automatic table creation on startup.
- **Integrity Engine**: Implements MAASP per ISO/TS 16530-2 formula, classification bands, SAP trend check, and auto task generation.
- **Frontend**: React + Vite + Tailwind. Pages: login, dashboard, well detail with D3 schematic, charts, and tasks.
- **Process Management**: PM2 supervises uvicorn and Vite dev server; pm2-logrotate enabled.
- **Scripts**: `scripts/install_ubuntu.sh` for native provisioning; start/stop/restart helpers for PM2.

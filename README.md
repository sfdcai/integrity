# DeepGuard Well Integrity Application

A production-focused FastAPI + React solution delivering MAASP calculations, annulus integrity classification, barrier management, and interactive schematics for ISO/TS 16530-2 style workflows. This edition targets native Ubuntu installs (SQLite backend, Vite frontend) with PM2 process supervision.

## Project layout
```
deepguard/
  backend/      # FastAPI, SQLAlchemy, integrity engine, JWT auth
  frontend/     # React + Tailwind + D3 UI
  scripts/      # Ubuntu installer + PM2 helpers
  docs/         # Architecture, setup, schematic, logic, roadmap
```

## Quick start (Ubuntu)
1. `cd deepguard`
2. `sudo bash scripts/install_ubuntu.sh`
3. Browse API at `http://<server>:8000/docs` and UI at `http://<server>:5173`

Default credentials: `admin@deepguard.io / admin`.

## Development
- Backend: `cd backend && ../scripts/start.sh` (uvicorn via PM2)
- Frontend: `cd frontend && npm run dev`
- Tests: `cd backend && source venv/bin/activate && pytest`

See `docs/SETUP.md` for detailed guidance and `docs/INTEGRITY_LOGIC.md` for the MAASP algorithm.

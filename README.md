# DeepGuard Well Integrity Application

Production-oriented web application for well integrity management per ISO/TS 16530-2 concepts. Includes FastAPI backend, PostgreSQL, Alembic migrations, and React + Tailwind frontend with D3 schematic rendering.

## Architecture
- **Backend**: FastAPI, SQLAlchemy ORM, Alembic, PostgreSQL. Modules for wells, annuli, measurements, barrier elements, tasks, integrity engine (MAASP and status), and schematic DTOs.
- **Frontend**: React (Vite) + TailwindCSS, Axios data layer, D3 interactive well schematic, dashboard with traffic-light indicators and tasks.
- **Deployment**: Native Ubuntu services (PostgreSQL, FastAPI via uvicorn, Vite dev server). No Docker required.

## Native installation (Ubuntu headless)
Use the installer to download the latest tagged archive, install missing dependencies, provision PostgreSQL locally, install backend/frontend dependencies, and run Alembic migrations:

```bash
chmod +x installer.sh
./installer.sh --latest                # or omit --latest to pin tag v0.0.01
```

Flags:
- `--install-dir <path>`: where the project should be placed (default: `$(pwd)/integrity`).
- `--release-tag <tag>`: fetch a specific release tag instead of the latest.
- `DEBUG=1`: emit verbose shell tracing to diagnose install issues.

What the installer does:
- Installs prerequisites: curl, unzip, Python 3 + venv, build-essential, libpq-dev, PostgreSQL, Node.js + npm.
- Ensures PostgreSQL service is started, creates `deepguard` role/password and `deepguard` database.
- Sets up Python virtual environment in `deepguard-app/backend/.venv` and installs `requirements.txt`.
- Writes `.env` with `DATABASE_URL=postgresql+psycopg2://deepguard:deepguard@localhost:5432/deepguard`.
- Runs Alembic migrations.
- Installs frontend dependencies (Vite + Tailwind) and builds the client once.

## Starting services and health checks
Use the port guard to verify core ports (5432/8000/3000) and start services natively if any are inactive. The script starts PostgreSQL via `systemctl`, launches uvicorn for the backend, and runs the Vite dev server for the frontend with logs saved under `deepguard-app/logs/`.

```bash
chmod +x port_guard.sh
./port_guard.sh --project-root <install_dir>/deepguard-app
```

You can override watched ports with `--ports "5432 8000 3000"` and enable debug tracing via `DEBUG=1`.

Manual start commands (after the installer):

```bash
# Backend
cd <install_dir>/deepguard-app/backend
source .venv/bin/activate
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Frontend
cd <install_dir>/deepguard-app/frontend
npm run dev -- --host --port 3000
```

Backend OpenAPI docs: http://localhost:8000/docs
Frontend UI: http://localhost:3000

## Database
- Alembic migrations live in `backend/alembic`. The default connection is `postgresql://deepguard:deepguard@localhost:5432/deepguard`.
- On backend startup a seed inserts sample well `DG-1` with annuli, tubulars, barrier elements, measurements, and tasks auto-generated from the integrity engine rules.

## Integrity logic
- MAASP: `P_surface_allowed = limit_at_depth - (gradient_bar_per_m * TVD)` then `MAASP = min(P_surface_allowed) * safety_factor (0.9)` per annulus.
- Status: utilisation = measured / MAASP. <70% GREEN, 70–90% AMBER, 90–100% HIGH-AMBER, >100% RED.
- Task hooks: utilisation >=90% creates review (7 days); >=100% creates critical immediate task.

## Frontend highlights
- Dashboard: well list with traffic-light status and open tasks.
- Well Detail: annulus cards, measurement entry, D3-based schematic (`/wells/{id}/schematic` endpoint), critical points, and barrier elements.
- Data Entry: create wells and annuli.

## Future AI hooks
- The data model and API responses leave space for predictive or advisory fields without implementing AI/ML in this release.

# DeepGuard Well Integrity Application

Production-oriented web application for well integrity management per ISO/TS 16530-2 concepts. Includes FastAPI backend, PostgreSQL, Alembic migrations, and React + Tailwind frontend with D3 schematic rendering.

## Architecture
- **Backend**: FastAPI, SQLAlchemy ORM, Alembic, PostgreSQL. Modules for wells, annuli, measurements, barrier elements, tasks, integrity engine (MAASP and status), and schematic DTOs.
- **Frontend**: React (Vite) + TailwindCSS, Axios data layer, D3 interactive well schematic, dashboard with traffic-light indicators and tasks.
- **Deployment**: Docker Compose with database, backend, and frontend services.

## Running locally
1. Install Docker.
2. From `deepguard-app/` run:
   ```bash
   docker-compose up --build
   ```
3. Backend: http://localhost:8000 (OpenAPI at `/docs`).
4. Frontend: http://localhost:3000.

## Automated installation (Ubuntu headless)
Use the installer to download the latest tagged archive, install missing dependencies, and build the containers:

```bash
chmod +x installer.sh
./installer.sh --latest                # or omit --latest to pin tag v0.0.01
```

Flags:
- `--install-dir <path>`: where the project should be placed (default: `$(pwd)/integrity`).
- `--release-tag <tag>`: fetch a specific release tag instead of the latest.
- `--skip-compose`: download/unpack without building Docker images (useful for air-gapped hosts).
- `DEBUG=1`: emit verbose shell tracing to diagnose install issues.

After installation, start or verify the stack with the port guard script, which checks ports 5432/8000/3000 and starts Docker Compose if needed:

```bash
chmod +x port_guard.sh
./port_guard.sh --compose-root <install_dir>/deepguard-app
```

You can override the watched ports with `--ports "5432 8000 3000"` and enable debug tracing via `DEBUG=1`.

## Database
- Alembic migrations live in `backend/alembic`. The default connection is `postgresql://postgres:postgres@db:5432/deepguard`.
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

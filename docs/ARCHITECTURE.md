# Architecture

- **Backend**: FastAPI + SQLAlchemy + SQLite. JWT auth, MAASP computation, reminders.
- **Frontend**: React (Vite), Tailwind, D3 for schematics, Recharts for trends.
- **Process control**: PM2 managed via install scripts.

## Backend layers
- `models`: SQLAlchemy ORM entities
- `schemas`: Pydantic DTOs
- `api`: Routers (auth, wells)
- `integrity`: MAASP and classification logic
- `services`: reminder generation

## Frontend
- Vite + Tailwind, pages: Login, Dashboard, WellDetail
- Components: ShellLayout, WellSchematic, widgets

## Data Flow
1. User logs in via `/auth/login` to receive JWT.
2. React uses token to call `/wells` endpoints.
3. `/wells/{id}/schematic` returns DTO for D3 rendering and trend cards.
4. MAASP engine derives utilisation and classification for tasks.

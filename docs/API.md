6. API Client Layer

In src/api/client.ts:

Axios instance with baseURL, auth header, interceptors.

Example:

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1",
});


Each module (wells.ts, annuli.ts, etc.) wraps endpoints in typed functions.

7. State Management

authStore (Zustand):

token, user, login/logout functions.

Query data via React Query or simple SWR-style hooks:

useWell(id), useWells(), useAnnulusMeasurements(wellId) etc.

8. Thematic Components

StatusPill:

colour-coded pill based on status (green, amber, high_amber, red).

AnnulusSummaryCard:

Reusable card that pulls from /integrity/annuli-summary.

RiskMatrixChart:

5×5 grid, each cell is clickable to filter wells by risk.

9. Build & Runtime

Dev: npm run dev (Vite).

Prod:

npm run build → dist/ static files.

Serve with Node (using serve or a small Express wrapper) under pm2.


# DeepGuard API Design

Base URL (default):


http://<host>:8000/api/v1


Auth: JWT Bearer token in Authorization: Bearer <token> header for protected routes.

1. Authentication
POST /auth/login

Request:

{
  "email": "engineer@example.com",
  "password": "Secret123!"
}


Response:

{
  "access_token": "jwt-token-here",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "engineer@example.com",
    "role": "engineer"
  }
}

2. Wells
GET /wells

List wells with filters:

Query params:

status (optional)

field (optional)

search (optional, partial name)

limit, offset

Response (simplified):

[
  {
    "id": 1,
    "name": "A-15",
    "field": "Alpha",
    "status": "green",
    "type": "producer",
    "highest_risk": "medium",
    "open_tasks": 2
  }
]

POST /wells

Create well.

GET /wells/{well_id}

Returns master data and summary integrity snapshot.

3. Casing, Tubing, Cement
GET /wells/{well_id}/architecture

Returns:

{
  "casings": [...],
  "tubing": [...],
  "cement_intervals": [...]
}

POST /wells/{well_id}/casings
POST /wells/{well_id}/tubing
POST /wells/{well_id}/cement

CRUD endpoints for each.

4. Annuli & MAASP
GET /wells/{well_id}/annuli

List annuli A/B/C/D:

[
  {
    "id": 1,
    "name": "A",
    "fluid_type": "gas",
    "fluid_gradient_bar_per_m": 0.012,
    "safety_factor": 0.9
  }
]

POST /wells/{well_id}/annuli

Create annulus.

GET /annuli/{annulus_id}/critical-points

List critical points.

POST /annuli/{annulus_id}/critical-points

Create critical point.

GET /annuli/{annulus_id}/maasp

Computes and returns MAASP:

{
  "annulus_id": 1,
  "maasp_bar": 230.0,
  "limiting_point": {
    "id": 5,
    "label": "Weak formation",
    "tvd_m": 1200,
    "pressure_limit_bar": 245.0
  },
  "safety_factor": 0.9,
  "computed_at": "2025-11-18T10:00:00Z"
}

5. Measurements
GET /annuli/{annulus_id}/measurements

Query params:

from (ISO datetime)

to (ISO datetime)

limit, offset

POST /annuli/{annulus_id}/measurements

Add measurement:

{
  "timestamp": "2025-11-18T08:00:00Z",
  "pressure_bar": 180.5,
  "temperature_c": 35.0
}


On POST, backend:

Stores measurement.

Recomputes utilisation & status.

Triggers SAP detection.

Generates tasks if thresholds exceeded.

6. Integrity Summary
GET /wells/{well_id}/integrity-summary

Returns data used to drive the overview tab:

{
  "well_id": 1,
  "overall_status": "amber",
  "risk_score": 62,
  "risk_category": "medium",
  "sap_detected": true,
  "primary_status": "green",
  "secondary_status": "amber",
  "annuli": [
    {
      "id": 1,
      "name": "A",
      "pressure_bar": 190.0,
      "maasp_bar": 220.0,
      "utilisation": 0.86,
      "status": "amber"
    }
  ],
  "last_updated": "2025-11-18T08:00:00Z"
}

GET /wells/{well_id}/annuli-summary

More compact per-annulus cards.

7. Barrier Management
GET /wells/{well_id}/barriers

Returns:

{
  "primary": [
    { "id": 1, "name": "SSSV", "type": "sssv", "depth_md": 1600, "status": "ok", "last_test": "2025-10-01" },
    ...
  ],
  "secondary": [
    { "id": 5, "name": "Production casing", "type": "casing", "status": "degraded" },
    ...
  ]
}

POST /wells/{well_id}/barriers

Create barrier element.

POST /barriers/{barrier_id}/tests

Register test result.

8. Schematic DTO
GET /wells/{well_id}/schematic

Used exclusively by the D3 schematic:

{
  "well": { "id": 1, "name": "A-15", "md": 3200, "tvd": 2950 },
  "casings": [...],
  "tubing": [...],
  "cement": [...],
  "annuli": [...],
  "barriers": [...]
}


Frontend does not call low-level architecture endpoints for drawing; it consumes this pre-assembled DTO.

9. Tasks & Reminders
GET /tasks

Query params:

status, priority, well_id, overdue_only

Response:

[
  {
    "id": 12,
    "title": "Review A-annulus (86% MAASP)",
    "priority": "high",
    "status": "open",
    "due_date": "2025-11-25",
    "well": { "id": 1, "name": "A-15" },
    "annulus": { "id": 1, "name": "A" }
  }
]

PATCH /tasks/{task_id}

Update status, add comments.

10. Admin & Config
GET /config/risk-matrix

Returns current risk matrix.

GET /config/settings

System-wide settings (safety factor, SAP thresholds, etc.).

PATCH /config/settings

Admin-only update.

11. Error Handling & Conventions

Errors use standard FastAPI format with detail field.

Pagination: X-Total-Count header where applicable.

Dates in ISO 8601 with UTC (Z).

12. Versioning

All endpoints under /api/v1. Future breaking changes go under /api/v2.

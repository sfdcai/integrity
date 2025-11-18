# DeepGuard Backend Design

## 1. Goals

The backend provides a deterministic, auditable well integrity engine:

- Store and manage well architecture (casing, tubing, cement, annuli).
- Compute MAASP and annulus utilisation using ISO/TS 16530-aligned logic.
- Model barrier envelopes (primary / secondary) and barrier elements.
- Track integrity tests, surveillance data, and SAP conditions.
- Expose clean APIs for frontend/UI, integrations, and reporting.
- Run natively on headless Ubuntu with **Python + FastAPI + SQLite**.

No Docker. No AI/ML in this version (future extension).

---

## 2. Tech Stack

- Language: **Python 3.12**
- Web framework: **FastAPI**
- ORM: **SQLAlchemy 2.x**
- DB: **SQLite** (single file `deepguard.db`)
- Migrations: **Alembic** (optional but recommended)
- Auth: JWT (via `python-jose` or similar)
- Validation: Pydantic models
- Process manager: **pm2** (via `pm2 start backend` running `uvicorn`)

---

## 3. High-Level Architecture

```text
backend/
  app/
    main.py           # FastAPI app + router registration
    core/
      config.py       # settings (ENV, DB path, JWT secret, etc.)
      security.py     # auth helpers, JWT encode/decode
      dependencies.py # common DI/dependency logic
    db/
      session.py      # engine + sessionmaker
      init_db.py      # schema/migration bootstrap
    models/
      user.py
      well.py
      annulus.py
      barrier.py
      measurement.py
      task.py
      integrity.py    # snapshot / risk
    schemas/
      auth.py
      well.py
      annulus.py
      barrier.py
      measurement.py
      task.py
      integrity.py
    services/
      well_service.py
      annulus_service.py
      barrier_service.py
      measurement_service.py
      task_service.py
      integrity_service.py
    integrity/
      maasp_engine.py
      classification.py
      risk_model.py
      sap_detection.py
      schematic_builder.py
    api/
      v1/
        auth.py
        wells.py
        annuli.py
        barriers.py
        measurements.py
        integrity.py
        tasks.py
        schematic.py
    utils/
      pagination.py
      logging.py
      csv_import.py

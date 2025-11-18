Configuration

Config via environment variables, read in core/config.py:

DG_DB_PATH (default ./deepguard.db)

DG_JWT_SECRET

DG_JWT_EXPIRE_MINUTES

DG_LOG_LEVEL

9. Startup Flow

uvicorn app.main:app started under pm2.

On startup:

Create DB file if missing.

Run migrations / create tables.

Ensure default admin user created (optional).

Expose OpenAPI docs at /docs.

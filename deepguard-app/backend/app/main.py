from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import wells, tasks
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(wells.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "DeepGuard Well Integrity API"}

from app.core.database import SessionLocal
from app.services.seed import seed


@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    seed(db)
    db.close()

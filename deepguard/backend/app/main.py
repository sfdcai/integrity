from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db, SessionLocal
from app.api import wells, auth
from app.services.seed import seed_admin, seed_sample_well

app = FastAPI(title="DeepGuard Well Integrity API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(wells.router, prefix="/api")


@app.on_event("startup")
def startup():
    init_db()
    db = SessionLocal()
    seed_admin(db)
    seed_sample_well(db)
    db.close()


@app.get("/")
def health():
    return {"message": "DeepGuard API online"}

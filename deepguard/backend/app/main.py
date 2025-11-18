from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .models import User
from .utils.security import get_password_hash
from .api import wells, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DeepGuard Well Integrity API", version="1.0")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(wells.router)


@app.on_event("startup")
def seed_user():
    db = next(get_db())
    try:
        if not db.query(User).filter(User.email == "admin@deepguard.ai").first():
            db.add(User(email="admin@deepguard.ai", hashed_password=get_password_hash("admin"), full_name="Admin"))
            db.commit()
    finally:
        db.close()


@app.get("/")
def health():
    return {"status": "ok"}

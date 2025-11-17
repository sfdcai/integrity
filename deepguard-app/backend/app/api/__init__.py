from fastapi import APIRouter
from app.api import wells, tasks

api_router = APIRouter()
api_router.include_router(wells.router)
api_router.include_router(tasks.router)

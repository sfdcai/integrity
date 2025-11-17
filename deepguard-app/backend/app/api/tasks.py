from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db
from app.models.task import Task as TaskModel
from app.schemas.well import Task

router = APIRouter()


@router.get("/tasks", response_model=List[Task])
def list_tasks(db: Session = Depends(get_db)):
    records = db.query(TaskModel).order_by(TaskModel.due_date.asc()).all()
    return records

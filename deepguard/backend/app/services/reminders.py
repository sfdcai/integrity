from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..models import Task, PressureMeasurement, Annulus
from ..integrity.maasp import compute_maasp, utilisation, detect_trend


def ensure_tasks(db: Session, annulus: Annulus, maasp_value: float):
    measurements = [m.pressure for m in annulus.measurements]
    current_pressure = measurements[-1] if measurements else 0
    utilisation_pct = utilisation(current_pressure, maasp_value)

    if utilisation_pct >= 90:
        due = datetime.utcnow() + timedelta(days=7 if utilisation_pct < 100 else 0)
        title = "Integrity review" if utilisation_pct < 100 else "Urgent bleed-down"
        create_task_if_missing(db, annulus.well_id, title, due, "HIGH" if utilisation_pct >= 100 else "MEDIUM")

    if detect_trend(measurements) == "rising":
        create_task_if_missing(
            db,
            annulus.well_id,
            f"Rising pressure detected in {annulus.name}",
            datetime.utcnow() + timedelta(days=1),
            "HIGH",
        )


def create_task_if_missing(db: Session, well_id: int, title: str, due_date: datetime, priority: str):
    existing = (
        db.query(Task)
        .filter(Task.well_id == well_id, Task.title == title, Task.status == "OPEN")
        .first()
    )
    if existing:
        return existing
    task = Task(well_id=well_id, title=title, due_date=due_date, priority=priority)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

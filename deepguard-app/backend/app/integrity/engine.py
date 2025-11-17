from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from app.models.measurement import Measurement
from app.models.annulus import Annulus
from app.models.task import Task


class IntegrityStatus:
    GREEN = "GREEN"
    AMBER = "AMBER"
    HIGH_AMBER = "HIGH-AMBER"
    RED = "RED"


class IntegrityEngine:
    @staticmethod
    def maasp(annulus: Annulus, tvd: float) -> float:
        p_surface_allowed = annulus.limit_at_depth - (annulus.gradient_bar_per_m * tvd)
        return p_surface_allowed * annulus.safety_factor

    @staticmethod
    def classify(utilisation: float) -> str:
        if utilisation < 0.7:
            return IntegrityStatus.GREEN
        if utilisation < 0.9:
            return IntegrityStatus.AMBER
        if utilisation <= 1.0:
            return IntegrityStatus.HIGH_AMBER
        return IntegrityStatus.RED

    @staticmethod
    def process_measurement(db: Session, measurement: Measurement) -> Optional[Task]:
        annulus = measurement.annulus
        maasp_value = IntegrityEngine.maasp(annulus, measurement.tvd)
        utilisation = measurement.pressure / maasp_value if maasp_value else 0
        status = IntegrityEngine.classify(utilisation)

        # generate tasks based on utilisation
        task: Optional[Task] = None
        if utilisation >= 1.0:
            task = Task(
                well_id=annulus.well_id,
                title=f"Urgent annulus pressure breach ({annulus.name})",
                priority="critical",
                due_date=datetime.utcnow(),
                status="open",
            )
            db.add(task)
        elif utilisation >= 0.9:
            task = Task(
                well_id=annulus.well_id,
                title=f"Review annulus pressure ({annulus.name})",
                priority="high",
                due_date=datetime.utcnow() + timedelta(days=7),
                status="open",
            )
            db.add(task)
        db.commit()
        db.refresh(measurement)
        if task:
            db.refresh(task)
        return task

    @staticmethod
    def status_for_annulus(annulus: Annulus):
        if not annulus.measurements:
            return {"maasp": None, "utilisation": None, "status": IntegrityStatus.GREEN}
        latest = sorted(annulus.measurements, key=lambda m: m.recorded_at)[-1]
        maasp_val = IntegrityEngine.maasp(annulus, latest.tvd)
        utilisation = latest.pressure / maasp_val if maasp_val else 0
        status = IntegrityEngine.classify(utilisation)
        return {"maasp": maasp_val, "utilisation": utilisation, "status": status}

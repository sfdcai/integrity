from datetime import datetime, timedelta
from typing import List, Tuple
from app.models import Annulus, CriticalPoint, Measurement, Task, Well


STATUS_BANDS = [
    (0.7, "GREEN", "Stable integrity"),
    (0.9, "AMBER", "Monitor and plan review"),
    (1.0, "HIGH-AMBER", "Prepare mitigation"),
    (999, "RED", "Exceeding MAASP - act now"),
]


def calculate_maasp(annulus: Annulus, critical_points: List[CriticalPoint]) -> float:
    allowable = [
        cp.limit_at_depth - (annulus.fluid_gradient * cp.depth_m) for cp in critical_points
    ]
    return min(allowable) * annulus.safety_factor if allowable else 0.0


def classify_integrity(measured: float, maasp: float) -> Tuple[str, float, str]:
    if maasp <= 0:
        return "RED", 1.0, "No MAASP available"
    utilisation = measured / maasp
    for threshold, label, recommendation in STATUS_BANDS:
        if utilisation < threshold:
            return label, utilisation, recommendation
    return "RED", utilisation, "Check MAASP inputs"


def auto_tasks(well: Well, maasp: float, measurement: Measurement):
    utilisation = measurement.pressure_bar / maasp if maasp else 1
    due_date = None
    priority = "normal"
    title = None
    if utilisation >= 1.0:
        title = "Urgent bleed-down"
        priority = "critical"
        due_date = datetime.utcnow()
    elif utilisation >= 0.9:
        title = "Integrity review"
        priority = "high"
        due_date = datetime.utcnow() + timedelta(days=7)
    if title:
        well.tasks.append(
            Task(title=title, priority=priority, due_date=due_date, well_id=well.id)
        )


def sap_trend_alert(measurements: List[Measurement]) -> bool:
    if len(measurements) < 3:
        return False
    last = sorted(measurements, key=lambda m: m.recorded_at)[-3:]
    return last[0].pressure_bar < last[1].pressure_bar < last[2].pressure_bar

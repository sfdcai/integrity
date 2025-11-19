"""Glue logic triggered when new measurements arrive."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Iterable, List, Sequence

from .classification import assess_integrity
from .maasp_engine import MAASPResult, compute_maasp_for_annulus
from .sap_detection import SAPDetectionResult, detect_sap
from ..services.reminders import create_task_if_missing


@dataclass
class IntegritySnapshot:
    utilisation: float
    status: str
    sap_detected: bool
    maasp: MAASPResult


@dataclass
class TaskPlan:
    title: str
    due_date: datetime
    priority: str
    trigger_type: str


def evaluate_measurement(
    annulus: Any, measurements: Sequence[Any], critical_points: Sequence[Any], barrier_test_failed: bool = False
) -> IntegritySnapshot:
    """Compute MAASP, utilisation, status, and SAP detection for a measurement set."""

    if not measurements:
        raise ValueError("At least one measurement is required to evaluate integrity")

    maasp_result = compute_maasp_for_annulus(annulus, critical_points)
    latest_pressure = measurements[-1].get("pressure_bar") if isinstance(measurements[-1], dict) else getattr(measurements[-1], "pressure_bar", getattr(measurements[-1], "pressure", 0))
    util, status = assess_integrity(latest_pressure, maasp_result.maasp_bar)
    sap_result = detect_sap(measurements)

    return IntegritySnapshot(utilisation=util, status=status, sap_detected=sap_result.sap_detected or barrier_test_failed, maasp=maasp_result)


def plan_tasks(snapshot: IntegritySnapshot, barrier_test_failed: bool = False) -> List[TaskPlan]:
    """Translate snapshot outcomes into auto-generated task plans."""

    plans: List[TaskPlan] = []

    if snapshot.utilisation > 0.9 and snapshot.utilisation <= 1.0:
        plans.append(
            TaskPlan(
                title="Integrity review",
                due_date=datetime.utcnow() + timedelta(days=7),
                priority="HIGH",
                trigger_type="maasp_exceed",
            )
        )
    elif snapshot.utilisation > 1.0:
        plans.append(
            TaskPlan(
                title="Urgent bleed-down",
                due_date=datetime.utcnow(),
                priority="CRITICAL",
                trigger_type="maasp_exceed",
            )
        )

    if snapshot.sap_detected:
        plans.append(
            TaskPlan(
                title="Investigate sustained annulus pressure",
                due_date=datetime.utcnow() + timedelta(days=1),
                priority="HIGH",
                trigger_type="sap_detected",
            )
        )

    if barrier_test_failed:
        plans.append(
            TaskPlan(
                title="Barrier maintenance",
                due_date=datetime.utcnow() + timedelta(days=3),
                priority="HIGH",
                trigger_type="failed_test",
            )
        )

    return plans


def apply_task_plans(db: Any, annulus: Any, plans: Iterable[TaskPlan]) -> None:
    """Persist tasks using the shared reminder helper while avoiding duplicates."""

    for plan in plans:
        create_task_if_missing(
            db,
            annulus.well_id,
            plan.title,
            plan.due_date,
            plan.priority,
            auto_generated=True,
            trigger_type=plan.trigger_type,
        )


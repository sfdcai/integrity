"""SAP (sustained annulus pressure) detection utilities."""

from dataclasses import dataclass
from typing import Any, Iterable, List


@dataclass
class SAPDetectionResult:
    sap_detected: bool
    reasons: List[str]


def _pressure_value(measurement: Any) -> float:
    if isinstance(measurement, dict):
        return float(measurement.get("pressure_bar") or measurement.get("pressure") or 0)
    return float(getattr(measurement, "pressure_bar", getattr(measurement, "pressure", 0)))


def detect_sap(
    measurements: Iterable[Any],
    positive_pressure_threshold: float = 0.0,
    rebuild_threshold: float = 5.0,
    persistence_points: int = 3,
) -> SAPDetectionResult:
    """Detect SAP based on guidance in ``docs/Integrity Logic.md``.

    Two scenarios are flagged:
    * Persistent positive pressure: the last ``persistence_points`` values all exceed
      ``positive_pressure_threshold``.
    * Pressure rebuild after bleed: a sharp drop followed by a sustained rebuild of
      at least ``rebuild_threshold`` without falling back below the positive threshold.
    """

    pressures = [_pressure_value(m) for m in measurements]
    reasons: List[str] = []

    if len(pressures) >= persistence_points and all(p > positive_pressure_threshold for p in pressures[-persistence_points:]):
        reasons.append("persistent-positive-pressure")

    for idx in range(1, len(pressures)):
        drop = pressures[idx - 1] - pressures[idx]
        if drop >= rebuild_threshold:
            subsequent = pressures[idx:]
            if subsequent and (max(subsequent) - pressures[idx]) >= rebuild_threshold and min(subsequent) > positive_pressure_threshold:
                reasons.append("pressure-rebuild-after-bleed")
                break

    return SAPDetectionResult(sap_detected=bool(reasons), reasons=reasons)


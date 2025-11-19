"""Integrity calculations aligned with docs/INTEGRITY_LOGIC.md."""

from statistics import mean
from typing import Any, Iterable, List, Sequence, Tuple


def compute_maasp(
    gradients: List[float], limits: List[float], depths: List[float], safety_factor: float = 0.9
) -> float:
    """Calculate MAASP using the documented formula.

    For each critical point the allowed surface pressure is::

        P_surface_allowed_i = limit_at_depth_i - (gradient_bar_per_m * TVD_i)

    The minimum allowed pressure is multiplied by the provided safety factor. The
    lists must be of equal length so that each triple aligns.
    """

    if not (len(gradients) == len(limits) == len(depths)):
        raise ValueError("Gradient, limit, and depth lists must be same length")

    allowed = [limit - (gradient * depth) for gradient, limit, depth in zip(gradients, limits, depths)]
    return min(allowed) * safety_factor if allowed else 0.0


def compute_maasp_for_annulus(
    fluid_gradient_bar_per_m: float, critical_points: Sequence[Any], safety_factor: float = 0.9
) -> Tuple[float, Any]:
    """Return MAASP and the limiting point for an annulus.

    Each ``critical_point`` item can be either a mapping or object exposing
    ``tvd_m`` and ``pressure_limit_bar`` attributes. This keeps the logic
    reusable for ORM objects and plain dictionaries.
    """

    if not critical_points:
        raise ValueError("At least one critical point is required to compute MAASP")

    def extract(point: Any, key: str) -> float:
        if isinstance(point, dict):
            return float(point.get(key, 0))
        return float(getattr(point, key))

    allowed = []
    for point in critical_points:
        tvd = extract(point, "tvd_m")
        limit = extract(point, "pressure_limit_bar")
        allowed_surface = limit - (fluid_gradient_bar_per_m * tvd)
        allowed.append((allowed_surface, point))

    limiting_allowed, limiting_point = min(allowed, key=lambda item: item[0])
    return limiting_allowed * safety_factor, limiting_point


def utilisation(measured_pressure: float, maasp: float) -> float:
    if maasp <= 0:
        return 0.0
    return (measured_pressure / maasp) * 100


def classify_integrity(utilisation_pct: float) -> str:
    if utilisation_pct < 70:
        return "GREEN"
    if utilisation_pct < 90:
        return "AMBER"
    if utilisation_pct <= 100:
        return "HIGH AMBER"
    return "RED"


def recommendations(utilisation_pct: float) -> str:
    if utilisation_pct < 70:
        return "Normal monitoring; maintain standard surveillance cadence."
    if utilisation_pct < 90:
        return "Elevated observation; plan integrity review and validate trends."
    if utilisation_pct <= 100:
        return "High amber; schedule bleed-down preparedness and validate barriers."
    return "RED risk; initiate urgent bleed-down and perform root-cause analysis."


def detect_trend(measurements: Iterable[float]) -> str:
    measurements_list = list(measurements)
    if len(measurements_list) < 3:
        return "insufficient-data"

    slope = measurements_list[-1] - measurements_list[0]
    avg = mean(measurements_list)
    if avg == 0:
        return "stable"

    if slope > 0.05 * avg:
        return "rising"
    if slope < -0.05 * avg:
        return "falling"
    return "stable"

"""MAASP computation helpers following the integrity documentation.

The functions in this module mirror the steps described in
``docs/Integrity Logic.md`` so that MAASP values, limiting critical points,
and safety factors are all explicit and traceable.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Sequence


@dataclass
class MAASPResult:
    """Container for MAASP outputs."""

    maasp_bar: float
    limiting_point: Any
    safety_factor: float
    computed_at: datetime


def _extract(point: Any, key: str) -> float:
    if isinstance(point, dict):
        return float(point[key])
    return float(getattr(point, key))


def compute_maasp_for_annulus(
    annulus: Any, critical_points: Sequence[Any], safety_factor: float | None = None
) -> MAASPResult:
    """Return MAASP, limiting point, and the safety factor used.

    The documented formula is applied per critical point::

        P_surface_allowed_i = pressure_limit_bar - fluid_gradient_bar_per_m * tvd_m
        MAASP = min(P_surface_allowed_i_list) * safety_factor

    ``critical_points`` may be SQLAlchemy objects or dictionaries exposing
    ``tvd_m`` and ``pressure_limit_bar`` keys. ``annulus`` must expose a fluid
    gradient (``fluid_gradient`` or ``fluid_gradient_bar_per_m``) and may carry a
    ``safety_factor`` override.
    """

    if not critical_points:
        raise ValueError("At least one critical point is required to compute MAASP")

    gradient = None
    if isinstance(annulus, (int, float)):
        gradient = float(annulus)
    else:
        gradient = getattr(annulus, "fluid_gradient", None)
        if gradient is None:
            gradient = getattr(annulus, "fluid_gradient_bar_per_m", None)
    if gradient is None:
        raise ValueError("Annulus must provide a fluid gradient for MAASP computation")

    applied_safety_factor = safety_factor if safety_factor is not None else getattr(annulus, "safety_factor", 0.9)

    allowed_surface_pressures = []
    for point in critical_points:
        tvd = _extract(point, "tvd_m")
        limit = _extract(point, "pressure_limit_bar")
        allowed_surface_pressures.append((limit - (gradient * tvd), point))

    limiting_allowed, limiting_point = min(allowed_surface_pressures, key=lambda item: item[0])

    return MAASPResult(
        maasp_bar=limiting_allowed * applied_safety_factor,
        limiting_point=limiting_point,
        safety_factor=applied_safety_factor,
        computed_at=datetime.utcnow(),
    )


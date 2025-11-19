"""Utilisation and status helpers as documented in Integrity Logic."""

from typing import Tuple


def utilisation(measured_pressure: float, maasp_bar: float) -> float:
    """Return utilisation as a ratio (0–1).

    The documentation defines utilisation as measured pressure divided by MAASP
    (no implicit percentage scaling). Zero or negative MAASP values return 0 to
    avoid divide-by-zero surprises.
    """

    if maasp_bar <= 0:
        return 0.0
    return measured_pressure / maasp_bar


def classify_status(utilisation_ratio: float) -> str:
    """Classify utilisation into traffic-light style statuses."""

    if utilisation_ratio < 0.7:
        return "green"
    if utilisation_ratio < 0.9:
        return "amber"
    if utilisation_ratio <= 1.0:
        return "high_amber"
    return "red"


def assess_integrity(measured_pressure: float, maasp_bar: float) -> Tuple[float, str]:
    """Convenience wrapper returning both utilisation and status."""

    util = utilisation(measured_pressure, maasp_bar)
    return util, classify_status(util)


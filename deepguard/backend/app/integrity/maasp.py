from typing import List
from statistics import mean


def compute_maasp(gradients: List[float], limits: List[float], depths: List[float], safety_factor: float = 0.9) -> float:
    if not (len(gradients) == len(limits) == len(depths)):
        raise ValueError("Gradient, limit, and depth lists must be same length")
    allowed = []
    for gradient, limit, depth in zip(gradients, limits, depths):
        allowed_surface = limit - (gradient * depth)
        allowed.append(allowed_surface)
    return min(allowed) * safety_factor if allowed else 0.0


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


def detect_trend(measurements: List[float]) -> str:
    if len(measurements) < 3:
        return "insufficient-data"
    slope = measurements[-1] - measurements[0]
    avg = mean(measurements)
    if slope > 0.05 * avg:
        return "rising"
    if slope < -0.05 * avg:
        return "falling"
    return "stable"

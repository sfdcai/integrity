Integrity Logic
5.1 MAASP Engine

For each annulus:

Load all AnnulusCriticalPoint rows.

For each point:

P_surface_allowed_i = pressure_limit_bar - fluid_gradient_bar_per_m * tvd_m

MAASP = min(P_surface_allowed_i) * safety_factor.

Implement in integrity/maasp_engine.py:

def compute_maasp_for_annulus(annulus, critical_points) -> MAASPResult:
    # returns maasp value and limiting point

5.2 Utilisation & Status

For the latest measurement:

utilisation = measured_pressure / maasp
if utilisation < 0.7: status = "green"
elif utilisation < 0.9: status = "amber"
elif utilisation <= 1.0: status = "high_amber"
else: status = "red"

5.3 SAP Detection

In sap_detection.py:

Analyse time series of AnnulusMeasurement.

Detect cases where:

Pressure builds up after bleed without injection.

Persistent positive pressure over threshold (config).

Flag sap_detected = True in IntegritySnapshot.

5.4 Automatic Task Creation

Triggered in integrity_service.py after each new measurement:

If utilisation > 0.9 and ≤ 1.0 → create review task (7-day due date).

If utilisation > 1.0 → create urgent task (today’s date).

If SAP detected → create investigation task.

If barrier test failed → create maintenance task.

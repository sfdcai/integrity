# Integrity Logic

MAASP calculation follows:
`P_surface_allowed_i = limit_at_depth_i - (gradient_bar_per_m * TVD_i)`
`MAASP = min(P_surface_allowed_i_list) * safety_factor (0.9)`

Utilisation = measured_surface_pressure / MAASP * 100

Classification:
- <70% GREEN
- 70–90% AMBER
- 90–100% HIGH AMBER
- >100% RED

Reminders auto-generate when utilisation >=90% or trends show rising pressure.

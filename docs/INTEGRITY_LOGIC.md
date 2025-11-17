# Integrity Logic

MAASP: `P_surface_allowed_i = limit_at_depth_i - (gradient_bar_per_m * TVD_i)`; `MAASP = min(P_surface_allowed_i_list) * safety_factor(0.9)`.

Classification based on utilisation = measured / MAASP:
- <70% GREEN
- 70–90% AMBER
- 90–100% HIGH-AMBER
- >100% RED

Tasks: >=90% schedule review in 7 days; >=100% urgent bleed-down; SAP rising trend triggers recommendation note.

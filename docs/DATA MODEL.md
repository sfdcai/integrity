Data Model
4.1 Users

User

id (int, PK)

email (unique)

password_hash

role (viewer, engineer, admin)

is_active

Used for auth + RBAC.

4.2 Wells & Architecture

Well

id

name

field

country (optional)

type (producer/injector/testing/etc.)

status (active/shut-in/suspended/abandoned)

spud_date, completion_date (optional)

measured_depth

true_vertical_depth

CasingString

id

well_id

name (e.g. "Surface", "Intermediate", "Production")

outer_diameter_in

inner_diameter_in

grade

top_md, bottom_md

burst_limit_bar

collapse_limit_bar

CementInterval

id

well_id

casing_id

top_md, bottom_md

compressive_strength_mpa (optional)

quality_flag (OK/uncertain/poor)

TubingString

id

well_id

name (e.g. "Production tubing")

outer_diameter_in

inner_diameter_in

top_md, bottom_md

grade

4.3 Annuli & MAASP

Annulus

id

well_id

name ("A", "B", "C", "D")

inner_string (FK to CasingString or TubingString)

outer_string (FK to CasingString)

fluid_type (gas/brine/mud/other)

fluid_gradient_bar_per_m

safety_factor (default 0.9)

AnnulusCriticalPoint

id

annulus_id

label ("Shoe", "Top of cement", "Weak formation", etc.)

tvd_m

pressure_limit_bar # allowable at that depth

AnnulusMeasurement

id

annulus_id

timestamp

pressure_bar

temperature_c (optional)

source (manual/SCADA/bulk_import)

MAASPResult

id

annulus_id

computed_at

maasp_bar

limiting_point_id (FK to AnnulusCriticalPoint)

4.4 Barrier Envelopes

BarrierEnvelope

id

well_id

type (primary, secondary)

description

BarrierElement

id

well_id

envelope_id (primary / secondary)

name (e.g. "SSSV", "Production packer")

element_type (enum: sssv, packer, casing, cement, wellhead, tree_valve, etc.)

depth_md (if applicable)

status (ok, failed, degraded, unknown)

BarrierTest

id

barrier_element_id

test_type (pressure, inflow, leak-rate, functional)

test_date

result (pass, fail, inconclusive)

pressure_applied_bar

leak_rate_unit (optional)

comments

4.5 Integrity & Risk

IntegritySnapshot

id

well_id

created_at

overall_status (green, amber, red)

primary_status

secondary_status

highest_annulus_utilisation

sap_detected (bool)

risk_score (0–100)

risk_category (L/M/H)

RiskMatrixCell (configurable)

id

probability_level (1–5)

consequence_level (1–5)

category (low, medium, high, extreme)

4.6 Tasks & Reminders

Task

id

well_id (optional)

annulus_id (optional)

barrier_element_id (optional)

title

description

priority (low, normal, high, critical)

due_date

status (open, in_progress, done, cancelled)

auto_generated (bool)

trigger_type (maasp_exceed, sap_detected, failed_test, etc.)

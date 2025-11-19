from app.integrity.classification import assess_integrity, classify_status, utilisation
from app.integrity.maasp import compute_maasp, detect_trend
from app.integrity.maasp_engine import compute_maasp_for_annulus
from app.integrity.sap_detection import detect_sap
from app.integrity.integrity_service import IntegritySnapshot, plan_tasks


def test_compute_maasp_basic():
    maasp = compute_maasp([0.01, 0.012], [400, 380], [1000, 1200])
    assert round(maasp, 2) == round(min([400 - 0.01 * 1000, 380 - 0.012 * 1200]) * 0.9, 2)


def test_maasp_engine_returns_limiting_point():
    points = [
        {"tvd_m": 500, "pressure_limit_bar": 300, "label": "Shoe"},
        {"tvd_m": 800, "pressure_limit_bar": 270, "label": "Weak formation"},
    ]
    result = compute_maasp_for_annulus(0.012, points)

    expected_surface = min([300 - 0.012 * 500, 270 - 0.012 * 800]) * 0.9
    assert round(result.maasp_bar, 2) == round(expected_surface, 2)
    assert result.limiting_point["label"] == "Weak formation"


def test_utilisation_and_classification():
    maasp = 200
    util = utilisation(150, maasp)
    assert round(util, 3) == 0.75
    _, status = assess_integrity(150, maasp)
    assert status == "amber"


def test_detect_trend_matches_documentation():
    assert detect_trend([100, 110, 125]) == "rising"
    assert detect_trend([120, 110, 100]) == "falling"
    assert detect_trend([100, 101, 100]) == "stable"


def test_sap_detection_flags_persistent_and_rebuild():
    assert detect_sap([{"pressure_bar": 0.2}, {"pressure_bar": 1.0}, {"pressure_bar": 1.1}]).sap_detected

    rebuild_series = [
        {"pressure_bar": 15.0},
        {"pressure_bar": 2.0},
        {"pressure_bar": 4.0},
        {"pressure_bar": 10.0},
    ]
    result = detect_sap(rebuild_series)
    assert result.sap_detected
    assert "pressure-rebuild-after-bleed" in result.reasons


def test_task_planning_matches_integrity_logic():
    snapshot = IntegritySnapshot(utilisation=0.95, status="high_amber", sap_detected=False, maasp=None)
    plans = plan_tasks(snapshot)
    assert any(plan.title == "Integrity review" for plan in plans)

    snapshot = IntegritySnapshot(utilisation=1.05, status="red", sap_detected=True, maasp=None)
    plans = plan_tasks(snapshot)
    titles = {plan.title for plan in plans}
    assert "Urgent bleed-down" in titles
    assert "Investigate sustained annulus pressure" in titles

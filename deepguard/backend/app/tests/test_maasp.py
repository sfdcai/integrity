from app.integrity.maasp import compute_maasp, utilisation, classify_integrity


def test_compute_maasp_basic():
    maasp = compute_maasp([0.01, 0.012], [400, 380], [1000, 1200])
    assert round(maasp, 2) == round(min([400 - 0.01 * 1000, 380 - 0.012 * 1200]) * 0.9, 2)


def test_utilisation_and_classification():
    maasp = 200
    util = utilisation(150, maasp)
    assert round(util, 1) == 75.0
    assert classify_integrity(util) == "AMBER"

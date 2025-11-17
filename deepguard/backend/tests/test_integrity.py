from app.integrity.engine import calculate_maasp, classify_integrity
from app.models import Annulus, CriticalPoint


def test_calculate_maasp():
    annulus = Annulus(fluid_gradient=0.012, safety_factor=0.9)
    cps = [CriticalPoint(depth_m=1000, limit_at_depth=240)]
    maasp = calculate_maasp(annulus, cps)
    assert round(maasp, 2) == round((240 - 0.012 * 1000) * 0.9, 2)


def test_classification_bands():
    status, utilisation, _ = classify_integrity(measured=50, maasp=100)
    assert status == "GREEN"
    status, utilisation, _ = classify_integrity(measured=80, maasp=100)
    assert status == "AMBER"

from sqlalchemy.orm import Session
from app import models


def seed(db: Session):
    if db.query(models.well.Well).count() > 0:
        return
    well = models.well.Well(name="DG-1", field="DeepGuard", operator="OperatorX", tvd=2500)
    db.add(well)
    db.flush()

    annulus_a = models.annulus.Annulus(
        name="A-annulus", well_id=well.id, limit_at_depth=400, gradient_bar_per_m=0.012, safety_factor=0.9
    )
    annulus_b = models.annulus.Annulus(
        name="B-annulus", well_id=well.id, limit_at_depth=350, gradient_bar_per_m=0.011, safety_factor=0.9
    )
    db.add_all([annulus_a, annulus_b])
    db.flush()

    db.add_all(
        [
            models.measurement.Measurement(annulus_id=annulus_a.id, pressure=120, tvd=1500),
            models.measurement.Measurement(annulus_id=annulus_b.id, pressure=80, tvd=1000),
        ]
    )
    db.add_all(
        [
            models.tubular.Tubular(well_id=well.id, type="casing", top_md=0, bottom_md=2500, od_in=9.625),
            models.tubular.Tubular(well_id=well.id, type="tubing", top_md=0, bottom_md=2400, od_in=3.5),
        ]
    )
    db.add_all(
        [
            models.critical_point.CriticalPoint(
                well_id=well.id, name="Shoe", depth=2450, description="Production casing shoe"
            ),
            models.critical_point.CriticalPoint(
                well_id=well.id, name="Packer", depth=1800, description="Permanent packer"
            ),
        ]
    )
    db.add_all(
        [
            models.barrier.BarrierElement(well_id=well.id, name="SSSV", type="surface safety valve", md=100, status="tested"),
            models.barrier.BarrierElement(well_id=well.id, name="Packer", type="mechanical", md=1800, status="set"),
        ]
    )
    db.commit()

from sqlalchemy.orm import Session
from app import models
from app.utils.auth import get_password_hash


def seed_admin(db: Session):
    if not db.query(models.User).filter(models.User.email == "admin@deepguard.io").first():
        admin = models.User(email="admin@deepguard.io", hashed_password=get_password_hash("admin"))
        db.add(admin)
        db.commit()


def seed_sample_well(db: Session):
    if db.query(models.Well).first():
        return
    well = models.Well(name="DG-01", field="North", well_type="Producer", tvd=2500, status="GREEN")
    db.add(well)
    db.commit()
    db.refresh(well)
    annulus = models.Annulus(name="A", fluid_gradient=0.012, safety_factor=0.9, well_id=well.id)
    db.add(annulus)
    db.commit()
    db.refresh(annulus)
    cp = models.CriticalPoint(name="Casing shoe", depth_m=1000, limit_at_depth=240, annulus_id=annulus.id, well_id=well.id)
    db.add(cp)
    db.commit()
    db.add(models.Measurement(annulus_id=annulus.id, well_id=well.id, pressure_bar=180))
    db.add(models.BarrierElement(well_id=well.id, barrier_type="SSSV", name="Primary SSSV", depth=1800, status="TESTED"))
    db.add(models.Task(well_id=well.id, title="Review corrosion log", priority="normal"))
    db.commit()

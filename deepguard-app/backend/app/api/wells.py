from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db
from app.models.well import Well
from app.models.annulus import Annulus
from app.models.measurement import Measurement
from app.schemas import well as schemas
from app.integrity.engine import IntegrityEngine

router = APIRouter()


@router.get("/wells", response_model=List[schemas.Well])
def list_wells(db: Session = Depends(get_db)):
    wells = db.query(Well).all()
    enriched = []
    for well in wells:
        for annulus in well.annuli:
            status_info = IntegrityEngine.status_for_annulus(annulus)
            annulus.status = status_info["status"]
            annulus.utilisation = status_info["utilisation"]
            annulus.maasp = status_info["maasp"]
        enriched.append(well)
    return enriched


@router.post("/wells", response_model=schemas.Well)
def create_well(well_in: schemas.WellCreate, db: Session = Depends(get_db)):
    well = Well(
        name=well_in.name, field=well_in.field, operator=well_in.operator, tvd=well_in.tvd
    )
    db.add(well)
    db.flush()
    for annulus in well_in.annuli:
        db.add(
            Annulus(
                name=annulus.name,
                well_id=well.id,
                limit_at_depth=annulus.limit_at_depth,
                gradient_bar_per_m=annulus.gradient_bar_per_m,
                safety_factor=annulus.safety_factor,
            )
        )
    db.commit()
    db.refresh(well)
    return well


@router.get("/wells/{well_id}", response_model=schemas.Well)
def get_well(well_id: int, db: Session = Depends(get_db)):
    well = db.query(Well).filter(Well.id == well_id).first()
    if not well:
        raise HTTPException(status_code=404, detail="Well not found")
    for annulus in well.annuli:
        status_info = IntegrityEngine.status_for_annulus(annulus)
        annulus.status = status_info["status"]
        annulus.utilisation = status_info["utilisation"]
        annulus.maasp = status_info["maasp"]
    return well


@router.post("/annuli/{annulus_id}/measurements", response_model=schemas.Measurement)
def add_measurement(
    annulus_id: int,
    measurement_in: schemas.MeasurementBase,
    db: Session = Depends(get_db),
):
    annulus = db.query(Annulus).filter_by(id=annulus_id).first()
    if not annulus:
        raise HTTPException(status_code=404, detail="Annulus not found")
    measurement = Measurement(annulus_id=annulus.id, pressure=measurement_in.pressure, tvd=measurement_in.tvd)
    db.add(measurement)
    db.commit()
    db.refresh(measurement)
    IntegrityEngine.process_measurement(db, measurement)
    return measurement


@router.get("/wells/{well_id}/schematic", response_model=schemas.SchematicResponse)
def schematic(well_id: int, db: Session = Depends(get_db)):
    well = db.query(Well).filter_by(id=well_id).first()
    if not well:
        raise HTTPException(status_code=404, detail="Well not found")
    casings = [t for t in well.tubulars if t.type == "casing"]
    tubing = [t for t in well.tubulars if t.type == "tubing"]
    cement = well.critical_points
    annuli = []
    maasp_values = []
    measurements = []
    for annulus in well.annuli:
        status_info = IntegrityEngine.status_for_annulus(annulus)
        annulus.status = status_info["status"]
        annulus.utilisation = status_info["utilisation"]
        annulus.maasp = status_info["maasp"]
        annuli.append(annulus)
        maasp_values.append(status_info["maasp"] if status_info["maasp"] else 0)
        measurements.extend(annulus.measurements)
    return schemas.SchematicResponse(
        casings=casings,
        tubing=tubing,
        cement=cement,
        barrier_elements=well.barrier_elements,
        depths=well.tvd or 0,
        annuli=annuli,
        maasp=maasp_values,
        measurements=measurements,
    )

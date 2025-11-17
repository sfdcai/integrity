from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app import models
from app.schemas import (
    WellCreate,
    WellOut,
    AnnulusCreate,
    AnnulusOut,
    CriticalPointCreate,
    MeasurementCreate,
    MeasurementOut,
    SchematicDTO,
    BarrierElementCreate,
    BarrierElementOut,
    TaskOut,
)
from app.utils.auth import get_current_user, get_db
from app.integrity.engine import calculate_maasp, classify_integrity, auto_tasks, sap_trend_alert

router = APIRouter(prefix="/wells", tags=["wells"])


@router.post("/", response_model=WellOut)
def create_well(payload: WellCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    well = models.Well(**payload.dict())
    db.add(well)
    db.commit()
    db.refresh(well)
    return well


@router.get("/", response_model=List[WellOut])
def list_wells(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.Well).all()


@router.post("/{well_id}/annuli", response_model=AnnulusOut)
def add_annulus(well_id: int, payload: AnnulusCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    well = db.query(models.Well).get(well_id)
    if not well:
        raise HTTPException(404, "Well not found")
    annulus = models.Annulus(well_id=well_id, **payload.dict())
    db.add(annulus)
    db.commit()
    db.refresh(annulus)
    return annulus


@router.post("/{well_id}/critical-points")
def add_critical_point(well_id: int, payload: CriticalPointCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    annulus = db.query(models.Annulus).get(payload.annulus_id)
    if not annulus or annulus.well_id != well_id:
        raise HTTPException(404, "Annulus not found")
    cp = models.CriticalPoint(well_id=well_id, **payload.dict())
    db.add(cp)
    db.commit()
    return {"status": "created", "id": cp.id}


@router.post("/{well_id}/measurements", response_model=MeasurementOut)
def add_measurement(well_id: int, payload: MeasurementCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    annulus = db.query(models.Annulus).get(payload.annulus_id)
    if not annulus or annulus.well_id != well_id:
        raise HTTPException(404, "Annulus not found")
    measurement = models.Measurement(well_id=well_id, pressure_bar=payload.pressure_bar, annulus_id=payload.annulus_id)
    db.add(measurement)
    db.commit()
    db.refresh(measurement)
    maasp = calculate_maasp(annulus, annulus.critical_points)
    auto_tasks(annulus.well, maasp, measurement)
    db.commit()
    return measurement


@router.post("/{well_id}/barriers", response_model=BarrierElementOut)
def add_barrier(well_id: int, payload: BarrierElementCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    well = db.query(models.Well).get(well_id)
    if not well:
        raise HTTPException(404, "Well not found")
    barrier = models.BarrierElement(well_id=well_id, **payload.dict())
    db.add(barrier)
    db.commit()
    db.refresh(barrier)
    return barrier


@router.get("/{well_id}", response_model=WellOut)
def well_detail(well_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    well = db.query(models.Well).get(well_id)
    if not well:
        raise HTTPException(404, "Not found")
    return well


@router.get("/{well_id}/schematic", response_model=SchematicDTO)
def schematic(well_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    well = db.query(models.Well).get(well_id)
    if not well:
        raise HTTPException(404, "Not found")
    annuli = well.annuli
    latest_measurements = (
        db.query(models.Measurement)
        .filter(models.Measurement.well_id == well_id)
        .order_by(models.Measurement.recorded_at.desc())
        .all()
    )
    annulus = annuli[0] if annuli else None
    maasp = calculate_maasp(annulus, annulus.critical_points) if annulus else 0
    measured = latest_measurements[0].pressure_bar if latest_measurements else 0
    status, utilisation, recommendation = classify_integrity(measured, maasp)
    if sap_trend_alert(latest_measurements):
        recommendation += " | Rising SAP trend detected"
    well.status = status
    db.commit()
    return SchematicDTO(
        well=well,
        annuli_pressures=latest_measurements,
        maasp=maasp,
        utilisation=utilisation,
        status=status,
        recommendation=recommendation,
    )


@router.get("/{well_id}/tasks", response_model=List[TaskOut])
def list_tasks(well_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.Task).filter(models.Task.well_id == well_id).all()

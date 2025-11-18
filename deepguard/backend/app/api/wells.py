from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import get_db
from ..models import Well, Annulus, PressureMeasurement, BarrierElement
from ..schemas import (
    WellCreate,
    Well as WellSchema,
    AnnulusCreate,
    BarrierElementCreate,
    SchematicDTO,
    PressureMeasurementCreate,
)
from ..integrity.maasp import compute_maasp, utilisation, classify_integrity, recommendations
from ..services.reminders import ensure_tasks
from .auth import get_current_user

router = APIRouter(prefix="/wells", tags=["wells"])


@router.post("/", response_model=WellSchema)
def create_well(well: WellCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_well = Well(name=well.name, field=well.field, well_type=well.well_type, status=well.status, owner_id=user.id)
    db.add(db_well)
    for annulus in well.annuli:
        db_annulus = Annulus(
            name=annulus.name,
            top_depth=annulus.top_depth,
            bottom_depth=annulus.bottom_depth,
            fluid_gradient=annulus.fluid_gradient,
            critical_pressure_limit=annulus.critical_pressure_limit,
            well=db_well,
        )
        db.add(db_annulus)
    db.commit()
    db.refresh(db_well)
    return db_well


@router.get("/", response_model=list[WellSchema])
def list_wells(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Well).filter(Well.owner_id == user.id).all()


@router.get("/{well_id}", response_model=WellSchema)
def get_well(well_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    well = db.query(Well).filter(Well.id == well_id, Well.owner_id == user.id).first()
    if not well:
        raise HTTPException(status_code=404, detail="Well not found")
    return well


@router.post("/{well_id}/annuli", response_model=WellSchema)
def add_annulus(well_id: int, annulus: AnnulusCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    well = db.query(Well).filter(Well.id == well_id, Well.owner_id == user.id).first()
    if not well:
        raise HTTPException(status_code=404, detail="Well not found")
    db_annulus = Annulus(
        name=annulus.name,
        top_depth=annulus.top_depth,
        bottom_depth=annulus.bottom_depth,
        fluid_gradient=annulus.fluid_gradient,
        critical_pressure_limit=annulus.critical_pressure_limit,
        well=well,
    )
    db.add(db_annulus)
    db.commit()
    db.refresh(well)
    return well


@router.post("/{well_id}/barriers", response_model=WellSchema)
def add_barrier_element(
    well_id: int,
    element: BarrierElementCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    well = db.query(Well).filter(Well.id == well_id, Well.owner_id == user.id).first()
    if not well:
        raise HTTPException(status_code=404, detail="Well not found")
    barrier = BarrierElement(
        well_id=well.id,
        element_type=element.element_type,
        name=element.name,
        depth=element.depth,
        last_test_date=element.last_test_date,
        status=element.status,
        notes=element.notes,
    )
    db.add(barrier)
    db.commit()
    db.refresh(well)
    return well


@router.post("/{well_id}/annuli/{annulus_id}/pressure", response_model=WellSchema)
def add_pressure_measurement(
    well_id: int,
    annulus_id: int,
    reading: PressureMeasurementCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    annulus = (
        db.query(Annulus)
        .join(Well)
        .filter(Annulus.id == annulus_id, Well.id == well_id, Well.owner_id == user.id)
        .first()
    )
    if not annulus:
        raise HTTPException(status_code=404, detail="Annulus not found")
    measurement = PressureMeasurement(
        annulus=annulus,
        pressure=reading.pressure,
        timestamp=reading.timestamp or datetime.utcnow(),
    )
    db.add(measurement)

    maasp_value = compute_maasp(
        [annulus.fluid_gradient],
        [annulus.critical_pressure_limit],
        [annulus.bottom_depth],
    )
    ensure_tasks(db, annulus, maasp_value)

    db.commit()
    db.refresh(annulus.well)
    return annulus.well


@router.get("/{well_id}/schematic", response_model=SchematicDTO)
def schematic(well_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    well = db.query(Well).filter(Well.id == well_id, Well.owner_id == user.id).first()
    if not well:
        raise HTTPException(status_code=404, detail="Well not found")

    maasp_values = []
    annulus_pressures = []
    for annulus in well.annuli:
        maasp_value = compute_maasp([
            annulus.fluid_gradient
        ], [annulus.critical_pressure_limit], [annulus.bottom_depth])
        current_pressure = annulus.measurements[-1].pressure if annulus.measurements else 0
        utilisation_pct = utilisation(current_pressure, maasp_value)
        maasp_values.append({
            "annulus": annulus.name,
            "maasp": maasp_value,
            "utilisation": utilisation_pct,
            "classification": classify_integrity(utilisation_pct),
            "recommendation": recommendations(utilisation_pct),
        })
        annulus_pressures.append({
            "annulus": annulus.name,
            "pressure": current_pressure,
            "measurements": [
                {"timestamp": m.timestamp.isoformat(), "pressure": m.pressure} for m in annulus.measurements
            ],
        })

    dto = {
        "casing_strings": [
            {"name": "Conductor", "top": 0, "bottom": 100},
            {"name": "Surface", "top": 0, "bottom": 500},
            {"name": "Intermediate", "top": 0, "bottom": 1200},
            {"name": "Production", "top": 0, "bottom": 2500},
        ],
        "tubing": [{"name": "Production Tubing", "top": 0, "bottom": 2400}],
        "cement": [
            {"casing": "Surface", "top": 0, "bottom": 500},
            {"casing": "Intermediate", "top": 0, "bottom": 1200},
        ],
        "barrier_elements": [
            {"name": b.name, "type": b.element_type, "depth": b.depth, "status": b.status}
            for b in well.barriers
        ],
        "annulus_pressures": annulus_pressures,
        "maasp_values": maasp_values,
        "wellhead_components": [
            {"name": "X-mas Tree", "status": "OK"},
            {"name": "Annulus Valve", "status": "OK"},
        ],
        "labels": [
            {"text": well.name, "depth": 0},
        ],
    }
    return dto

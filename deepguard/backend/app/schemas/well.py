from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class AnnulusCreate(BaseModel):
    name: str
    fluid_gradient: float
    safety_factor: float = 0.9


class AnnulusOut(BaseModel):
    id: int
    name: str
    fluid_gradient: float
    safety_factor: float

    class Config:
        orm_mode = True


class CriticalPointCreate(BaseModel):
    name: str
    depth_m: float
    limit_at_depth: float
    annulus_id: int


class MeasurementCreate(BaseModel):
    annulus_id: int
    pressure_bar: float


class MeasurementOut(BaseModel):
    id: int
    annulus_id: int
    pressure_bar: float
    recorded_at: datetime

    class Config:
        orm_mode = True


class BarrierElementCreate(BaseModel):
    barrier_type: str
    name: str
    depth: Optional[float] = None
    status: str = "UNKNOWN"
    anomalous: bool = False


class BarrierElementOut(BaseModel):
    id: int
    barrier_type: str
    name: str
    depth: Optional[float]
    status: str
    anomalous: bool

    class Config:
        orm_mode = True


class TaskOut(BaseModel):
    id: int
    title: str
    priority: str
    due_date: Optional[datetime]
    completed: bool

    class Config:
        orm_mode = True


class WellCreate(BaseModel):
    name: str
    field: Optional[str] = None
    well_type: Optional[str] = None
    tvd: Optional[float] = None


class WellOut(BaseModel):
    id: int
    name: str
    field: Optional[str]
    well_type: Optional[str]
    status: str
    tvd: Optional[float]
    annuli: List[AnnulusOut] = []
    barrier_elements: List[BarrierElementOut] = []
    tasks: List[TaskOut] = []

    class Config:
        orm_mode = True


class SchematicDTO(BaseModel):
    well: WellOut
    annuli_pressures: List[MeasurementOut]
    maasp: float
    utilisation: float
    status: str
    recommendation: str

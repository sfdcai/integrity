from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class AnnulusBase(BaseModel):
    name: str
    limit_at_depth: float
    gradient_bar_per_m: float
    safety_factor: float = 0.9


class AnnulusCreate(AnnulusBase):
    pass


class Annulus(AnnulusBase):
    id: int
    utilisation: Optional[float] = None
    status: Optional[str] = None
    maasp: Optional[float] = None

    class Config:
        orm_mode = True


class MeasurementBase(BaseModel):
    pressure: float
    tvd: float


class MeasurementCreate(MeasurementBase):
    annulus_id: int


class Measurement(MeasurementBase):
    id: int
    annulus_id: int
    recorded_at: datetime

    class Config:
        orm_mode = True


class CriticalPointBase(BaseModel):
    name: str
    depth: float
    description: Optional[str] = None


class CriticalPointCreate(CriticalPointBase):
    pass


class CriticalPoint(CriticalPointBase):
    id: int

    class Config:
        orm_mode = True


class TubularBase(BaseModel):
    type: str
    top_md: float
    bottom_md: float
    od_in: Optional[float] = None
    weight_ppf: Optional[float] = None


class TubularCreate(TubularBase):
    pass


class Tubular(TubularBase):
    id: int

    class Config:
        orm_mode = True


class BarrierBase(BaseModel):
    name: str
    type: str
    md: float
    status: str = "unknown"


class BarrierCreate(BarrierBase):
    pass


class Barrier(BarrierBase):
    id: int

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    title: str
    priority: str = "normal"
    due_date: Optional[datetime] = None
    status: str = "open"


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True


class WellBase(BaseModel):
    name: str
    field: Optional[str] = None
    operator: Optional[str] = None
    tvd: Optional[float] = None


class WellCreate(WellBase):
    annuli: List[AnnulusCreate] = []


class Well(WellBase):
    id: int
    annuli: List[Annulus] = []
    critical_points: List[CriticalPoint] = []
    tubulars: List[Tubular] = []
    barrier_elements: List[Barrier] = []
    tasks: List[Task] = []

    class Config:
        orm_mode = True


class SchematicResponse(BaseModel):
    casings: List[Tubular]
    tubing: List[Tubular]
    cement: List[CriticalPoint]
    barrier_elements: List[Barrier]
    depths: float
    annuli: List[Annulus]
    maasp: List[float]
    measurements: List[Measurement]

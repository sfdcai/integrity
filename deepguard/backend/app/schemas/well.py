from datetime import datetime
from pydantic import BaseModel, Field
from typing import List


class PressureMeasurementBase(BaseModel):
    pressure: float
    timestamp: datetime | None = Field(default=None, description="ISO timestamp of the reading")


class PressureMeasurementCreate(PressureMeasurementBase):
    timestamp: datetime | None = Field(default_factory=datetime.utcnow)


class PressureMeasurement(PressureMeasurementBase):
    id: int

    class Config:
        from_attributes = True


class AnnulusBase(BaseModel):
    name: str
    top_depth: float = 0.0
    bottom_depth: float = 0.0
    fluid_gradient: float = 0.00981
    critical_pressure_limit: float = 0.0


class AnnulusCreate(AnnulusBase):
    pass


class Annulus(AnnulusBase):
    id: int
    measurements: List[PressureMeasurement] = Field(default_factory=list)

    class Config:
        from_attributes = True


class BarrierElementBase(BaseModel):
    element_type: str
    name: str
    depth: float = 0.0
    last_test_date: datetime | None = None
    status: str = "OK"
    notes: str | None = None


class BarrierElementCreate(BarrierElementBase):
    pass


class BarrierElement(BarrierElementBase):
    id: int

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    due_date: datetime | None = None
    priority: str = "MEDIUM"
    status: str = "OPEN"


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int

    class Config:
        from_attributes = True


class WellBase(BaseModel):
    name: str
    field: str | None = None
    well_type: str | None = None
    status: str = "ACTIVE"


class WellCreate(WellBase):
    annuli: List[AnnulusCreate] = Field(default_factory=list)


class Well(WellBase):
    id: int
    annuli: List[Annulus] = Field(default_factory=list)
    barriers: List[BarrierElement] = Field(default_factory=list)
    tasks: List[Task] = Field(default_factory=list)

    class Config:
        from_attributes = True


class SchematicDTO(BaseModel):
    casing_strings: list
    tubing: list
    cement: list
    barrier_elements: list
    annulus_pressures: list
    maasp_values: list
    wellhead_components: list
    labels: list

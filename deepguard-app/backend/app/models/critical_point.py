from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class CriticalPoint(Base):
    __tablename__ = "critical_points"

    id = Column(Integer, primary_key=True, index=True)
    well_id = Column(Integer, ForeignKey("wells.id"), nullable=False)
    name = Column(String, nullable=False)
    depth = Column(Float, nullable=False)
    description = Column(String, nullable=True)

    well = relationship("Well", back_populates="critical_points")

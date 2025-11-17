from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class CriticalPoint(Base):
    __tablename__ = "critical_points"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    depth_m = Column(Float, nullable=False)
    limit_at_depth = Column(Float, nullable=False)
    annulus_id = Column(Integer, ForeignKey("annuli.id"), nullable=False)
    well_id = Column(Integer, ForeignKey("wells.id"), nullable=False)

    annulus = relationship("Annulus", back_populates="critical_points")
    well = relationship("Well", back_populates="critical_points")

from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Annulus(Base):
    __tablename__ = "annuli"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    well_id = Column(Integer, ForeignKey("wells.id"), nullable=False)
    fluid_gradient = Column(Float, nullable=False, default=0.012)
    safety_factor = Column(Float, default=0.9)

    well = relationship("Well", back_populates="annuli")
    critical_points = relationship("CriticalPoint", back_populates="annulus", cascade="all, delete-orphan")
    measurements = relationship("Measurement", back_populates="annulus", cascade="all, delete-orphan")

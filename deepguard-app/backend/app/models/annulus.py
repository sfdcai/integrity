from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Annulus(Base):
    __tablename__ = "annuli"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    well_id = Column(Integer, ForeignKey("wells.id"), nullable=False)
    limit_at_depth = Column(Float, nullable=False)
    gradient_bar_per_m = Column(Float, nullable=False)
    safety_factor = Column(Float, default=0.9)

    well = relationship("Well", back_populates="annuli")
    measurements = relationship("Measurement", back_populates="annulus", cascade="all, delete-orphan")

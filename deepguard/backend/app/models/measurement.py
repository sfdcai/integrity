from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    annulus_id = Column(Integer, ForeignKey("annuli.id"), nullable=False)
    well_id = Column(Integer, ForeignKey("wells.id"), nullable=False)
    pressure_bar = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    annulus = relationship("Annulus", back_populates="measurements")
    well = relationship("Well")

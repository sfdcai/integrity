from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    annulus_id = Column(Integer, ForeignKey("annuli.id"), nullable=False)
    pressure = Column(Float, nullable=False)
    tvd = Column(Float, nullable=False)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())

    annulus = relationship("Annulus", back_populates="measurements")

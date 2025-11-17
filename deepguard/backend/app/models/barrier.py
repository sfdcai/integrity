from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class BarrierElement(Base):
    __tablename__ = "barrier_elements"

    id = Column(Integer, primary_key=True, index=True)
    well_id = Column(Integer, ForeignKey("wells.id"), nullable=False)
    barrier_type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    depth = Column(Float, nullable=True)
    last_test_date = Column(DateTime, nullable=True)
    status = Column(String, default="UNKNOWN")
    anomalous = Column(Boolean, default=False)

    well = relationship("Well", back_populates="barrier_elements")

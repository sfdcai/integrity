from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class BarrierElement(Base):
    __tablename__ = "barrier_elements"

    id = Column(Integer, primary_key=True, index=True)
    well_id = Column(Integer, ForeignKey("wells.id"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    md = Column(Float, nullable=False)
    status = Column(String, default="unknown")

    well = relationship("Well", back_populates="barrier_elements")

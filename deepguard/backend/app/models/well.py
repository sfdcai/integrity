from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database import Base


class Well(Base):
    __tablename__ = "wells"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    field = Column(String, nullable=True)
    well_type = Column(String, nullable=True)
    status = Column(String, default="UNKNOWN")
    tvd = Column(Float, nullable=True)

    annuli = relationship("Annulus", back_populates="well", cascade="all, delete-orphan")
    tubulars = relationship("Tubular", back_populates="well", cascade="all, delete-orphan")
    barrier_elements = relationship("BarrierElement", back_populates="well", cascade="all, delete-orphan")
    critical_points = relationship("CriticalPoint", back_populates="well", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="well", cascade="all, delete-orphan")

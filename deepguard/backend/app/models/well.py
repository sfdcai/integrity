from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Well(Base):
    __tablename__ = "wells"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    field = Column(String, nullable=True)
    well_type = Column(String, nullable=True)
    status = Column(String, default="ACTIVE")
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="wells")
    annuli = relationship("Annulus", back_populates="well", cascade="all, delete-orphan")
    barriers = relationship("BarrierElement", back_populates="well", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="well", cascade="all, delete-orphan")


class Annulus(Base):
    __tablename__ = "annuli"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    well_id = Column(Integer, ForeignKey("wells.id"))
    top_depth = Column(Float, default=0.0)
    bottom_depth = Column(Float, default=0.0)
    fluid_gradient = Column(Float, default=0.00981)  # bar/m
    critical_pressure_limit = Column(Float, default=0.0)  # bar at depth

    well = relationship("Well", back_populates="annuli")
    measurements = relationship("PressureMeasurement", back_populates="annulus", cascade="all, delete-orphan")


class PressureMeasurement(Base):
    __tablename__ = "pressure_measurements"

    id = Column(Integer, primary_key=True, index=True)
    annulus_id = Column(Integer, ForeignKey("annuli.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    pressure = Column(Float, nullable=False)

    annulus = relationship("Annulus", back_populates="measurements")


class BarrierElement(Base):
    __tablename__ = "barrier_elements"

    id = Column(Integer, primary_key=True, index=True)
    well_id = Column(Integer, ForeignKey("wells.id"))
    element_type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    depth = Column(Float, default=0.0)
    last_test_date = Column(DateTime, nullable=True)
    status = Column(String, default="OK")
    notes = Column(Text, nullable=True)

    well = relationship("Well", back_populates="barriers")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    well_id = Column(Integer, ForeignKey("wells.id"))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime, nullable=True)
    priority = Column(String, default="MEDIUM")
    status = Column(String, default="OPEN")

    well = relationship("Well", back_populates="tasks")

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    well_id = Column(Integer, ForeignKey("wells.id"), nullable=False)
    title = Column(String, nullable=False)
    priority = Column(String, default="normal")
    due_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="open")

    well = relationship("Well", back_populates="tasks")

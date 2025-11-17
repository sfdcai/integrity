from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Tubular(Base):
    __tablename__ = "tubulars"

    id = Column(Integer, primary_key=True, index=True)
    well_id = Column(Integer, ForeignKey("wells.id"), nullable=False)
    name = Column(String, nullable=False)
    top_depth = Column(Float, nullable=True)
    bottom_depth = Column(Float, nullable=True)
    grade = Column(String, nullable=True)

    well = relationship("Well", back_populates="tubulars")

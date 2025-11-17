from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Tubular(Base):
    __tablename__ = "tubulars"

    id = Column(Integer, primary_key=True, index=True)
    well_id = Column(Integer, ForeignKey("wells.id"), nullable=False)
    type = Column(String, nullable=False)  # casing or tubing
    top_md = Column(Float, nullable=False)
    bottom_md = Column(Float, nullable=False)
    od_in = Column(Float, nullable=True)
    weight_ppf = Column(Float, nullable=True)

    well = relationship("Well", back_populates="tubulars")

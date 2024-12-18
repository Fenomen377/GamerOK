from sqlalchemy import JSON, Column, Integer, String, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship

from database import Base


class Table(Base):
    __tablename__ = 'tables'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specifications = Column(String, nullable=True)
    hourly_rate = Column(Float, nullable=False)
    is_available = Column(Boolean, nullable=False, default=True)
    zone_id = Column(Integer, ForeignKey('zones.id'))

    zone = relationship("Zone", back_populates="tables")



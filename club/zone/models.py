from sqlalchemy import JSON, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database import Base


class Zone(Base):
    __tablename__ = "zones"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    club_id = Column(Integer, ForeignKey("clubs.id"))
    hourly_rate = Column(Integer, nullable=False)

    club = relationship("Club", back_populates="zone")
    tables = relationship("Table", back_populates="zone")
    bookings = relationship("Booking", back_populates="zone")


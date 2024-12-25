from sqlalchemy import Column, Computed, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship

from database import Base

from sqlalchemy import Column, ForeignKey, Integer, DateTime, Computed
from sqlalchemy.orm import relationship
from database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    table_id = Column(ForeignKey("tables.id"), nullable=False)
    zone_id = Column(ForeignKey("zones.id"), nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    datetime_from = Column(DateTime, nullable=False)
    datetime_to = Column(DateTime, nullable=False)
    hourly_rate = Column(Integer, nullable=False)
    total_cost = Column(Integer, Computed("(datetime_to - datetime_from) / 3600 * hourly_rate", persisted=True))
    total_hours = Column(Integer, Computed("(datetime_to - datetime_from) / 3600", persisted=True))

    user = relationship("Users", back_populates="booking")
    table = relationship("Table", back_populates="bookings")
    zone = relationship("Zone", back_populates="bookings")

    def __str__(self):
        return f"Booking #{self.id}: {self.datetime_from} to {self.datetime_to}"

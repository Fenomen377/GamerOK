from sqlalchemy import JSON, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database import Base


class Zone(Base):
    __tablename__ = 'zones'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    club_id = Column(Integer, ForeignKey('clubs.id'))

    club = relationship("Club", back_populates="zones")
    tables = relationship("Table", back_populates="zone")


from sqlalchemy import JSON, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database import Base


class Club(Base):
    __tablename__ = 'clubs'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    description = Column(String, nullable=False)

    zones = relationship("Zone", back_populates="club")


from pydantic import BaseModel
from typing import Optional


class ZoneBase(BaseModel):
    name: str
    club_id: int
    hourly_rate: int



class ZoneCreate(ZoneBase):
    pass


class ZoneUpdate(ZoneBase):
    pass

class ZoneInfo(ZoneBase):
    id: int
    club_id: int

    class Config:
        orm_mode = True
        from_attributes = True
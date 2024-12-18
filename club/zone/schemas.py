from pydantic import BaseModel
from typing import Optional


class ZoneBase(BaseModel):
    name: str
    description: Optional[str]


class ZoneCreate(ZoneBase):
    pass


class ZoneUpdate(ZoneBase):
    name: Optional[str]
    description: Optional[str]


class ZoneInfo(ZoneBase):
    id: int
    club_id: int

    class Config:
        orm_mode = True
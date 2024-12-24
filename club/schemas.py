from pydantic import BaseModel
from typing import Optional


class ClubBase(BaseModel):
    name: str
    address: str


class ClubCreate(ClubBase):
    pass


class ClubUpdate(ClubBase):
    name: Optional[str]
    address: Optional[str]


class ClubInfo(ClubBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
from pydantic import BaseModel
from typing import Optional


class TableBase(BaseModel):
    name: str
    hourly_rate: float
    specifications: str


class TableCreate(TableBase):
    pass


class TableUpdate(TableBase):
    name: Optional[str]
    hourly_rate: Optional[float]
    specifications: Optional[str]


class TableInfo(TableBase):
    id: int
    zone_id: int

    class Config:
        orm_mode = True
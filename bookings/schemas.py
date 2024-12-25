from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class BookingBase(BaseModel):
    table_id: int
    zone_id: int
    datetime_from: datetime
    datetime_to: datetime


class BookingCreate(BookingBase):
    pass
    # hourly_rate: int = Field(..., gt=0, description="Цена аренды за час не может быть меньше нуля")


class BookingUpdate(BaseModel):
    datetime_from: Optional[datetime]
    datetime_to: Optional[datetime]
    hourly_rate: Optional[int]


class BookingInfo(BookingBase):
    id: int
    user_id: int
    total_cost: Optional[int]
    total_hours: Optional[int]

    class Config:
        orm_mode = True
        from_attributes = True

from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select, update, delete

from club.zone.dao import ZoneDAO
from database import async_session_maker
from .models import Booking
from .schemas import BookingCreate, BookingUpdate
from dao.base import BaseDAO


class BookingDAO(BaseDAO):
    model = Booking

    @classmethod
    async def create(cls, booking_data: BookingCreate, user_id: int) -> Booking:
        booking_data_dict = booking_data.dict()
        booking_data_dict["user_id"] = user_id
        if booking_data_dict["datetime_from"].tzinfo:
            booking_data_dict["datetime_from"] = booking_data_dict["datetime_from"].replace(tzinfo=None)
        if booking_data_dict["datetime_to"].tzinfo:
            booking_data_dict["datetime_to"] = booking_data_dict["datetime_to"].replace(tzinfo=None)
        zone = await ZoneDAO.find_one_or_none(id=booking_data_dict["zone_id"])
        if not zone:
            raise HTTPException(status_code=404, detail="Zone not found")
        hourly_rate = zone.hourly_rate
        booking_data_dict["hourly_rate"] = hourly_rate
        await cls.add(**booking_data_dict)
        return await cls.find_one_or_none(
            table_id=booking_data_dict["table_id"],
            zone_id=booking_data_dict["zone_id"],
            datetime_from=booking_data_dict["datetime_from"],
            datetime_to=booking_data_dict["datetime_to"],
        )

    @classmethod
    async def update(cls, booking_id: int, booking_data: BookingUpdate, user_id: int) -> Optional[Booking]:
        async with async_session_maker() as session:
            if booking_data.datetime_from and booking_data.datetime_from.tzinfo:
                booking_data = booking_data.copy(update={"datetime_from": booking_data.datetime_from.replace(tzinfo=None)})
            if booking_data.datetime_to and booking_data.datetime_to.tzinfo:
                booking_data = booking_data.copy(update={"datetime_to": booking_data.datetime_to.replace(tzinfo=None)})
            query = (
                update(cls.model)
                .where(cls.model.id == booking_id, cls.model.user_id == user_id)
                .values(**booking_data.dict(exclude_unset=True))
                .returning(cls.model)
            )
            result = await session.execute(query)
            updated_booking = result.scalars().first()
            await session.commit()
            return updated_booking

    @classmethod
    async def delete(cls, booking_id: int, user_id: int) -> bool:
        async with async_session_maker() as session:
            query = delete(cls.model).where(cls.model.id == booking_id, cls.model.user_id == user_id)
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0


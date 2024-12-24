from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from users.models import Users
from schemas import BookingCreate, BookingUpdate, BookingInfo
from bookings.dao import BookingDAO
from users.dependencies import get_current_user

router_booking = APIRouter(prefix="/bookings", tags=["Брони"])


@router_booking.post("/", response_model=BookingInfo)
async def create_booking(
    booking_data: BookingCreate,
    current_user: Users = Depends(get_current_user),
):
    return await BookingDAO.create(booking_data, user_id=current_user.id)


@router_booking.get("/{booking_id}", response_model=BookingInfo)
async def get_booking(booking_id: int):
    booking = await BookingDAO.find_one_or_none(id=booking_id)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    return booking


@router_booking.get("/", response_model=List[BookingInfo])
async def get_all_bookings():
    return await BookingDAO.find_all()


@router_booking.put("/{booking_id}", response_model=BookingInfo)
async def update_booking(
    booking_id: int,
    booking_data: BookingUpdate,
    current_user: Users = Depends(get_current_user),  # current_user - объект
):
    updated_booking = await BookingDAO.update(booking_id, booking_data, user_id=current_user.id)  # Передаем ID
    if not updated_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return updated_booking


@router_booking.delete("/{booking_id}", status_code=204)
async def delete_booking(
    booking_id: int,
    current_user: Users = Depends(get_current_user),
):
    deleted = await BookingDAO.delete(booking_id, user_id=current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Booking not found")


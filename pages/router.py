import httpx
from fastapi import APIRouter, Depends, Request, HTTPException, Response, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import List, Optional

from starlette.responses import RedirectResponse

from club.models import Club
from club.zone.models import Zone
from club.zone.schemas import ZoneInfo
from club.zone.table.models import Table
from bookings.models import Booking
from bookings.dao import BookingDAO
from club.dao import ClubDAO
from club.zone.dao import ZoneDAO
from club.zone.table.dao import TableDAO
from users.dependencies import get_current_user
from users.models import Users

router_frontend = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"]
)

async def get_user_context(request: Request, user: Optional[Users] = Depends(get_current_user)):
    return {"user": user}

templates = Jinja2Templates(directory="templates")

@router_frontend.get("/", response_class=HTMLResponse)
async def index(request: Request, user: Optional[Users] = Depends(get_current_user)):
    return templates.TemplateResponse("index.html", {"request": request, "user": user})


@router_frontend.get("/zones", response_class=HTMLResponse)
async def zones(request: Request, user_context: dict = Depends(get_user_context)):
    zones = await ZoneDAO.find_all()
    return templates.TemplateResponse("clubs and tables/zones.html", {"request": request, "zones": zones, **user_context})


@router_frontend.get("/tables", response_class=HTMLResponse)
async def tables(request: Request, user_context: dict = Depends(get_user_context)):
    tables = await TableDAO.find_all()
    return templates.TemplateResponse("clubs and tables/tables.html", {"request": request, "tables": tables, **user_context})


@router_frontend.get("/clubs", response_class=HTMLResponse)
async def clubs(request: Request, user_context: dict = Depends(get_user_context)):
    clubs = await ClubDAO.find_all()
    if not clubs:
        raise HTTPException(status_code=404, detail="Клубы не найдены")
    return templates.TemplateResponse("clubs and tables/clubs.html", {"request": request, "clubs": clubs, **user_context})


@router_frontend.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router_frontend.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router_frontend.get("/bookings", response_class=HTMLResponse)
async def bookings(request: Request, user: Users = Depends(get_current_user), user_context: dict = Depends(get_user_context)):
    bookings = await BookingDAO.find_all(user_id=user.id) if user else []
    return templates.TemplateResponse(
        "bookings/bookings.html", {"request": request, "bookings": bookings, **user_context}
    )


@router_frontend.get("/logout")
async def logout(response: Response):
    response = RedirectResponse(url="/pages/", status_code=302)
    response.delete_cookie("booking_access_token")
    return response


@router_frontend.get("/booking_successful", response_class=HTMLResponse)
async def booking_successful(request: Request, booking_id: int):
    booking = await BookingDAO.find_one_or_none(id=booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Бронирование не найдено")
    return templates.TemplateResponse("bookings/booking_successful.html", {"request": request, "booking": booking})


@router_frontend.get("/create_booking", response_class=HTMLResponse)
async def create_booking(request: Request, user_context: dict = Depends(get_user_context)):
    clubs = await ClubDAO.find_all()
    return templates.TemplateResponse(
        "bookings/create_booking.html",
        {"request": request, "clubs": clubs, **user_context},
    )


@router_frontend.post("/create_booking", response_class=HTMLResponse)
async def create_booking_post(
    request: Request,
    user: Users = Depends(get_current_user),
):
    form = await request.form()
    club_id = int(form.get("club"))
    zone_id = int(form.get("zone"))
    table_id = list(map(int, form.getlist("table")))
    start_time = form.get("start_time")
    end_time = form.get("end_time")

    if not all([club_id, zone_id, table_id, start_time, end_time]):
        raise HTTPException(status_code=400, detail="Некорректные данные")


    booking_data = {
        "club_id": club_id,
        "zone_id": zone_id,
        "table_id": table_id,
        "start_time": start_time,
        "end_time": end_time,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/bookings/",
            json=booking_data,
            cookies=request.cookies,
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Ошибка создания бронирования: {response.text}",
            )

        booking = response.json()

    return RedirectResponse(
        url=f"/pages/booking_successful?booking_id={booking['id']}",
        status_code=302,
    )


@router_frontend.get("/api/zones", response_model=List[ZoneInfo])
async def get_zones_by_club(club_id: int = Query(...)):
    zones = await ZoneDAO.find_by_club_id(club_id)
    if not zones:
        raise HTTPException(status_code=404, detail="Зоны не найдены")
    return zones

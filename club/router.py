from fastapi import APIRouter, HTTPException
from typing import List
from .schemas import ClubCreate, ClubInfo
from .dao import ClubDAO

router_club = APIRouter(prefix="/clubs", tags=["Клубы"])


@router_club.get("/", response_model=List[ClubInfo])
async def get_clubs():
    return await ClubDAO.find_all()


@router_club.get("/{club_id}", response_model=ClubInfo)
async def get_club(club_id: int):
    club = await ClubDAO.find_one_or_none(id=club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
    return club


@router_club.post("/", response_model=ClubInfo)
async def create_club(club_data: ClubCreate):
    return await ClubDAO.add(**club_data.dict())

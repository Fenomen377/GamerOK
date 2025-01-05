from fastapi import APIRouter, HTTPException, Depends
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db_session
from .schemas import ZoneCreate, ZoneInfo
from .dao import ZoneDAO

router_zone = APIRouter(prefix="/zones", tags=["Зоны"])


@router_zone.get("/", response_model=List[ZoneInfo])
async def get_zones():
    return await ZoneDAO.find_all()


@router_zone.get("/{zone_id}", response_model=ZoneInfo)
async def get_zone(zone_id: int):
    zone = await ZoneDAO.find_one_or_none(id=zone_id)
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    return zone


@router_zone.post("/", response_model=ZoneInfo)
async def create_zone(zone_data: ZoneCreate):
    return await ZoneDAO.add(**zone_data.dict())


@router_zone.get("/clubs/{club_id}/zones", response_model=List[ZoneInfo])
async def get_zones_by_club(club_id: int, session: AsyncSession = Depends(get_db_session)):
    dao = ZoneDAO(session)
    zones = await dao.find_by_club_id(club_id)
    if not zones:
        raise HTTPException(status_code=404, detail="Зоны не найдены для этого клуба")
    return zones
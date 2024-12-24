from fastapi import APIRouter, HTTPException
from typing import List
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

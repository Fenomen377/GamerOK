from fastapi import APIRouter, HTTPException, Depends
from typing import List

from database import async_session_maker
from schemas import TableCreate, TableInfo
from dao import TableDAO

router_table = APIRouter(prefix="/tables", tags=["Столы"])


@router_table.get("/", response_model=List[TableInfo])
async def get_tables():
    return await TableDAO.find_all()


@router_table.get("/{table_id}", response_model=TableInfo)
async def get_table(table_id: int):
    table = await TableDAO.find_one_or_none(id=table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return table


@router_table.post("/", response_model=TableInfo)
async def create_table(table: TableCreate):
    new_table = await TableDAO.add(
        name=table.name,
        hourly_rate=table.hourly_rate,
        specifications=table.specifications,
        zone_id=table.zone_id,
    )
    if not new_table:
        raise HTTPException(status_code=400, detail="Failed to create table")
    return TableInfo.from_orm(new_table)


@router_table.delete("/{table_id}")
async def delete_table(table_id: int):
    table = await TableDAO.find_one_or_none(id=table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    async with async_session_maker() as session:
        await session.delete(table)
        await session.commit()
    return {"detail": "Table deleted"}

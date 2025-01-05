from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from club.zone.models import Zone
from dao.base import BaseDAO


class ZoneDAO(BaseDAO):
    model = Zone

    async def find_by_club_id(self, club_id: int):
        result = await self.session.execute(
            select(self.model).where(self.model.club_id == club_id)
        )
        return result.scalars().all()


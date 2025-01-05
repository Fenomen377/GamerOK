from sqlalchemy import select

from club.zone.table.models import Table
from dao.base import BaseDAO


class TableDAO(BaseDAO):
    model = Table

    async def find_by_zone_id(self, zone_id: int):
        result = await self.session.execute(
            select(self.model).where(self.model.zone_id == zone_id)
        )
        return result.scalars().all()
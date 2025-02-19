from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models.models import AvailableSlot, Medic

class AvailabilityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_available_slots(self, region: int, comuna: int, area: int, specialty: str, is_reserved: bool = False):
        stmt = (
            select(AvailableSlot)
            .join(Medic, Medic.id == AvailableSlot.medic_id)
            .where(
                and_(
                    Medic.region_id == region,
                    Medic.comuna_id == comuna,
                    Medic.area_id == area,
                    Medic.specialty == specialty,
                    AvailableSlot.is_reserved == is_reserved
                )
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
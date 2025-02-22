from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models.models import AvailableSlot, Medic
from app.core.logging_config import get_logger, setup_logging
from app.core.config import settings

setup_logging(log_level=settings.LOG_LEVEL, log_to_file=settings.LOG_TO_FILE)
logger = get_logger(__name__)

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
                    Medic.specialty.ilike(specialty),
                    AvailableSlot.is_reserved == is_reserved
                )
            )
        )

        # Representación SQL para depuración
        sql_query = """
            SELECT available_slots.*
            FROM available_slots
            JOIN medics ON medics.id = available_slots.medic_id
            WHERE medics.region_id = %s
            AND medics.comuna_id = %s
            AND medics.area_id = %s
            AND medics.specialty ILIKE %s
            AND available_slots.is_reserved = %s;
        """
        logger.debug(
            "Ejecutando consulta SQL: %s",
            sql_query % (region, comuna, area, f"'{specialty}'", is_reserved)
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()
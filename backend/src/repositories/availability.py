from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func, TIME, or_
from src.models.database_models import AvailableSlot, Medic
from src.core.logging_config import get_logger, setup_logging
from src.core.config import settings
from src.schemas.availability import TimeRangeFilterEnum
from datetime import time
from typing import List

setup_logging(log_level=settings.LOG_LEVEL, log_to_file=settings.LOG_TO_FILE)
logger = get_logger(__name__)

class AvailabilityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_available_slots(
        self,
        region: int,
        commune: int,
        area: int,
        specialty: str,
        time_range_filter: TimeRangeFilterEnum,
        is_reserved: bool = False
    ) -> List[AvailableSlot]:
        time_ranges = {
            "morning": {"start": time(7, 0), "end": time(12, 0), "next_cycle": None},
            "afternoon": {"start": time(12, 0), "end": time(18, 0), "next_cycle": None},
            "night": {"start": time(18, 0), "end": time(23, 59, 59), "next_cycle": time(18, 0)}
        }
        range_info = time_ranges[time_range_filter.value]
        start_range = range_info["start"]
        end_range = range_info["end"]
        next_cycle_limit = range_info["next_cycle"]

        base_conditions = [
            Medic.region_id == region,
            Medic.commune_id == commune,
            Medic.area_id == area,
            Medic.specialty.ilike(specialty),
            AvailableSlot.is_reserved == is_reserved
        ]

        time_condition = and_(
            func.cast(AvailableSlot.start_time, TIME) >= start_range,
            func.cast(AvailableSlot.end_time, TIME) <= end_range
        )
        if next_cycle_limit:
            time_condition = or_(
                time_condition,
                and_(
                    func.cast(AvailableSlot.start_time, TIME) >= start_range,
                    func.cast(AvailableSlot.end_time, TIME) < next_cycle_limit
                )
            )

        query = (
            select(AvailableSlot)
            .join(Medic, Medic.id == AvailableSlot.medic_id)
            .where(and_(*base_conditions, time_condition))
        )

        sql_query_base = """
            SELECT available_slots.id, available_slots.start_time, available_slots.end_time
            FROM available_slots
            JOIN medics ON medics.id = available_slots.medic_id
            WHERE medics.region_id = {}
            AND medics.commune_id = {}
            AND medics.area_id = {}
            AND medics.specialty ILIKE '{}'
            AND available_slots.is_reserved = {}
        """
        sql_query_time = (
            "AND ((CAST(available_slots.start_time AS TIME) >= '{}' AND CAST(available_slots.end_time AS TIME) <= '{}') "
            "OR (CAST(available_slots.start_time AS TIME) >= '{}' AND CAST(available_slots.end_time AS TIME) < '{}'))"
            if next_cycle_limit else
            "AND CAST(available_slots.start_time AS TIME) >= '{}' "
            "AND CAST(available_slots.end_time AS TIME) <= '{}'"
        )
        sql_query_template = sql_query_base + sql_query_time + "\n"

        log_params = (
            [region, commune, area, specialty, is_reserved, start_range, end_range, start_range, next_cycle_limit]
            if next_cycle_limit else
            [region, commune, area, specialty, is_reserved, start_range, end_range]
        )

        sql_query = sql_query_template.format(*log_params)
        logger.debug("Ejecutando consulta SQL:\n%s", sql_query)

        result = await self.db.execute(query)
        slots = result.scalars().all()
        logger.debug("Slots disponibles encontrados: %d", len(slots))
        return slots
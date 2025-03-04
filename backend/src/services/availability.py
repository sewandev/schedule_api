from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound
from src.repositories.availability import AvailabilityRepository
from src.schemas.availability import AvailabilityResponse, AvailableSlot, TimeRangeFilterEnum
from src.core.logging_config import get_logger, setup_logging
from src.core.config import settings
from collections import defaultdict
import random

setup_logging(log_level=settings.LOG_LEVEL, log_to_file=settings.LOG_TO_FILE)
logger = get_logger(__name__)

class AvailabilityService:
    @staticmethod
    async def check_availability(
        region: int,
        commune: int,
        area: int,
        specialty: str,
        time_range_filter: TimeRangeFilterEnum,
        db: AsyncSession
    ) -> AvailabilityResponse:
        logger.info(
            "Verificando disponibilidad: region=%s, commune=%s, area=%s, specialty=%s, time_range=%s",
            region, commune, area, specialty, time_range_filter.value
        )
        repo = AvailabilityRepository(db)
        try:
            available_slots = await repo.get_available_slots(
                region, commune, area, specialty, time_range_filter, is_reserved=False
            )
            if not available_slots:
                detail_message = (
                    f"No se encontraron slots disponibles para la región {region}, comuna {commune}, "
                    f"área {area}, especialidad '{specialty}' y rango horario '{time_range_filter.value}'."
                )
                logger.debug(
                    "No se encontraron horarios disponibles: region=%s, commune=%s, area=%s, specialty=%s, time_range=%s",
                    region, commune, area, specialty, time_range_filter.value
                )
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail_message)

            slot_dict = defaultdict(list)
            for slot in available_slots:
                time_key = (slot.start_time.isoformat(), slot.end_time.isoformat())
                slot_dict[time_key].append(slot)

            unique_slots = []
            for time_key, slots in slot_dict.items():
                selected_slot = random.choice(slots)
                unique_slots.append(
                    AvailableSlot(
                        id=selected_slot.id,
                        start_time=selected_slot.start_time.isoformat(),
                        end_time=selected_slot.end_time.isoformat()
                    )
                )

            logger.debug(
                "Disponibilidad encontrada: %s slots únicos, region=%s, commune=%s, area=%s, specialty=%s, time_range=%s",
                len(unique_slots), region, commune, area, specialty, time_range_filter.value
            )
            return AvailabilityResponse(available_slots=unique_slots)

        except NoResultFound:
            logger.debug(
                "No se encontraron resultados en la base de datos: region=%s, commune=%s, area=%s, specialty=%s, time_range=%s",
                region, commune, area, specialty, time_range_filter.value
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontraron datos para la región {region}, comuna {commune}, área {area}, especialidad '{specialty}' y rango '{time_range_filter.value}'."
            )
        except Exception as e:
            logger.critical(
                "Error interno al consultar disponibilidad: %s",
                str(e),
                exc_info=True,
                extra={"region": region, "commune": commune, "area": area, "specialty": specialty, "time_range": time_range_filter.value}
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor al verificar disponibilidad."
            )
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound
from src.repositories.availability import AvailabilityRepository
from src.schemas.availability import AvailabilityResponse, AvailableSlot, TimeRangeFilterEnum
from src.core.logging_config import get_logger
from collections import defaultdict
import random

logger = get_logger(__name__)

class AvailabilityService:
    @staticmethod
    async def check_availability(
        region: int, comuna: int, area: int, specialty: str, time_range_filter: TimeRangeFilterEnum, db: AsyncSession
    ) -> AvailabilityResponse:
        repo = AvailabilityRepository(db)
        try:
            available_slots = await repo.get_available_slots(
                region, comuna, area, specialty, time_range_filter, is_reserved=False
            )

            if not available_slots:
                detail_message = (
                    f"No se encontraron slots disponibles para la región {region}, comuna {comuna}, "
                    f"área {area}, especialidad '{specialty}' y rango horario '{time_range_filter.value}'. "
                    "Por favor, verifica los parámetros o intenta con otros filtros."
                )
                logger.debug(
                    "No se encontraron horarios disponibles para region=%s, comuna=%s, area=%s, specialty=%s, time_range=%s",
                    region, comuna, area, specialty, time_range_filter.value
                )
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=detail_message
                )

            # Agrupa por rango horario (start_time, end_time) para eliminar duplicados
            slot_dict = defaultdict(list)
            for slot in available_slots:
                time_key = (slot.start_time.isoformat(), slot.end_time.isoformat())
                slot_dict[time_key].append(slot)

            logger.debug("Slots agrupados por rango horario")

            # Seleccionar aleatoriamente un slot por rango horario único
            unique_slots = []
            for time_key, slots in slot_dict.items():
                selected_slot = random.choice(slots)  # Elegir un slot aleatorio si hay múltiples coincidencias
                unique_slots.append(
                    AvailableSlot(
                        id=selected_slot.id,
                        start_time=selected_slot.start_time.isoformat(),
                        end_time=selected_slot.end_time.isoformat()
                    )
                )

            logger.debug(
                "Disponibilidad encontrada: %s horarios únicos en region=%s, comuna=%s, area=%s, specialty=%s, time_range=%s",
                len(unique_slots), region, comuna, area, specialty, time_range_filter.value
            )
            return AvailabilityResponse(available_slots=unique_slots)

        except HTTPException as e:
            raise e
        except NoResultFound:
            logger.debug(
                "No se encontraron resultados en la base de datos para region=%s, comuna=%s, area=%s, specialty=%s, time_range=%s",
                region, comuna, area, specialty, time_range_filter.value
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontraron datos para la región {region}, comuna {comuna}, área {area}, especialidad '{specialty}' y rango '{time_range_filter.value}'."
            )
        except Exception as e:
            logger.critical(
                "Error interno al consultar disponibilidad: %s",
                str(e),
                extra={"region": region, "comuna": comuna, "area": area, "specialty": specialty, "time_range": time_range_filter.value}
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor al verificar disponibilidad."
            )
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound
from app.repositories.availability import AvailabilityRepository
from app.schemas.availability import AvailabilityResponse, AvailableSlot, TimeRangeFilterEnum
from app.core.logging_config import get_logger
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
            # Consultar slots disponibles en la base de datos
            available_slots = await repo.get_available_slots(
                region, comuna, area, specialty, time_range_filter, is_reserved=False
            )

            # Manejar caso de lista vacía (no se encontraron resultados)
            if not available_slots:
                detail_message = (
                    f"No se encontraron slots disponibles para la región {region}, comuna {comuna}, "
                    f"área {area}, especialidad '{specialty}' y rango horario '{time_range_filter.value}'. "
                    "Por favor, verifica los parámetros o intenta con otros filtros."
                )
                logger.debug(
                    "No se encontraron slots disponibles para region=%s, comuna=%s, area=%s, specialty=%s, time_range=%s",
                    region, comuna, area, specialty, time_range_filter.value
                )
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=detail_message
                )

            # Agrupar slots por rango horario (start_time, end_time) para eliminar duplicados
            slot_dict = defaultdict(list)
            for slot in available_slots:
                time_key = (slot.start_time.isoformat(), slot.end_time.isoformat())
                slot_dict[time_key].append(slot)

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

            # Construir respuesta
            logger.debug(
                "Disponibilidad encontrada: %s slots únicos en region=%s, comuna=%s, area=%s, specialty=%s, time_range=%s",
                len(unique_slots), region, comuna, area, specialty, time_range_filter.value
            )
            return AvailabilityResponse(available_slots=unique_slots)

        except HTTPException as he:
            # Re-lanzar excepciones HTTP específicas (como el 404 anterior)
            raise he
        except NoResultFound:
            # Capturar específicamente cuando SQLAlchemy no encuentra resultados
            logger.debug(
                "No se encontraron resultados en la base de datos para region=%s, comuna=%s, area=%s, specialty=%s, time_range=%s",
                region, comuna, area, specialty, time_range_filter.value
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontraron datos para la región {region}, comuna {comuna}, área {area}, especialidad '{specialty}' y rango '{time_range_filter.value}'."
            )
        except Exception as e:
            # Capturar cualquier otro error inesperado
            logger.critical(
                "Error interno al consultar disponibilidad: %s",
                str(e),
                extra={"region": region, "comuna": comuna, "area": area, "specialty": specialty, "time_range": time_range_filter.value}
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor al verificar disponibilidad."
            )
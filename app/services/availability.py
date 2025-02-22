from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound
from app.repositories.availability import AvailabilityRepository
from app.schemas.availability import AvailabilityResponse, AvailableSlot, MedicAvailability, TimeRangeFilterEnum
from app.core.logging_config import get_logger
from collections import defaultdict

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

            # Agrupar slots por médico
            medic_slots = defaultdict(list)
            for slot in available_slots:
                medic_slots[slot.medic_id].append(
                    AvailableSlot(
                        start_time=slot.start_time.isoformat(),
                        end_time=slot.end_time.isoformat()
                    )
                )

            # Construir respuesta
            response_data = [
                MedicAvailability(medic_id=medic_id, slots=slots)
                for medic_id, slots in medic_slots.items()
            ]

            logger.debug(
                "Disponibilidad encontrada para %s médicos en region=%s, comuna=%s, area=%s, specialty=%s, time_range=%s",
                len(response_data), region, comuna, area, specialty, time_range_filter.value
            )
            return AvailabilityResponse(available_slots=response_data)

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
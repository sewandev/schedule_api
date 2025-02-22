from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound
from app.repositories.availability import AvailabilityRepository
from app.schemas.availability import AvailabilityResponse, AvailableSlot, MedicAvailability
from app.core.logging_config import get_logger
from collections import defaultdict

logger = get_logger(__name__)

class AvailabilityService:
    @staticmethod
    async def check_availability(
        region: int, comuna: int, area: int, specialty: str, db: AsyncSession
    ) -> AvailabilityResponse:
        """
        Verifica la disponibilidad de citas médicas según región, comuna, área y especialidad.

        Args:
            region (int): ID de la región.
            comuna (int): ID de la comuna.
            area (int): ID del área médica.
            specialty (str): Especialidad médica.
            db (AsyncSession): Sesión de base de datos.

        Returns:
            AvailabilityResponse: Respuesta con los slots disponibles agrupados por médico.

        Raises:
            HTTPException: Si no hay datos disponibles o ocurre un error interno.
        """
        repo = AvailabilityRepository(db)
        try:
            # Consultar slots disponibles
            available_slots = await repo.get_available_slots(
                region, comuna, area, specialty, is_reserved=False
            )

            # Verificar si hay resultados
            if not available_slots:
                logger.info(
                    "No se encontraron slots disponibles para region=%s, comuna=%s, area=%s, specialty=%s",
                    region, comuna, area, specialty
                )
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No hay citas disponibles para la región {region}, comuna {comuna}, área {area} y especialidad {specialty}."
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

            logger.info(
                "Disponibilidad encontrada para %s médicos en region=%s, comuna=%s, area=%s, specialty=%s",
                len(response_data), region, comuna, area, specialty
            )
            return AvailabilityResponse(available_slots=response_data)

        except HTTPException as he:
            # Dejar que las excepciones HTTP (como 404) se propaguen
            raise he
        except NoResultFound:
            # Manejo específico para consultas vacías en SQLAlchemy
            logger.info(
                "No se encontraron resultados en la base de datos para region=%s, comuna=%s, area=%s, specialty=%s",
                region, comuna, area, specialty
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontraron datos para la región {region}, comuna {comuna}, área {area} y especialidad {specialty}."
            )
        except Exception as e:
            # Solo capturar errores reales del servidor
            logger.critical(
                "Error interno al consultar disponibilidad: %s",
                str(e),
                extra={"region": region, "comuna": comuna, "area": area, "specialty": specialty}
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor al verificar disponibilidad. Por favor, intenta de nuevo más tarde."
            )
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.core.logging_config import get_logger, setup_logging
from src.core.config import settings
from src.schemas.availability import AvailabilityQuery, AvailabilityResponse
from src.services.availability import AvailabilityService

setup_logging(log_level=settings.LOG_LEVEL, log_to_file=settings.LOG_TO_FILE)
logger = get_logger(__name__)

router = APIRouter()

@router.get(
    "/",
    response_model=AvailabilityResponse,
    status_code=status.HTTP_200_OK,
    summary="Verifica la disponibilidad de horas médicas",
    description="Consulta la disponibilidad de horas médicas según región, comuna, área, especialidad y rango horario.",
    responses={
        200: {"description": "Devuelve las citas disponibles según los datos ingresados"},
        400: {"description": "Parámetros inválidos proporcionados"},
        404: {"description": "No se encontraron citas disponibles para los criterios especificados"},
        500: {"description": "Error interno del servidor"}
    }
)
async def check_availability(
    query: AvailabilityQuery = Depends(),
    db: AsyncSession = Depends(get_db)
) -> AvailabilityResponse:
    logger.info(
        "Solicitud recibida para verificar disponibilidad: region=%s, comuna=%s, area=%s, specialty=%s, time_range_filter=%s",
        query.region, query.commune, query.area, query.specialty, query.time_range_filter
    )
    try:
        normalized_specialty = query.specialty.lower()
        result = await AvailabilityService.check_availability(
            query.region, query.commune, query.area, normalized_specialty, query.time_range_filter, db
        )
        logger.debug(
            "Disponibilidad encontrada para region=%s, comuna=%s, area=%s, specialty=%s, time_range_filter=%s: %s",
            query.region, query.commune, query.area, normalized_specialty, query.time_range_filter, result.model_dump()
        )
        return result
    except ValueError as ve:
        logger.error("Error de validación: %s", str(ve))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.critical("Error inesperado en el endpoint: %s", str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor. Contacte al soporte con el ID de traza en los logs."
        )
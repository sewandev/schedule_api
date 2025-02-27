from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.logging_config import get_logger
from app.schemas.availability import AvailabilityQuery, AvailabilityResponse
from app.services.availability import AvailabilityService

router = APIRouter()
logger = get_logger(__name__)

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
    try:
        normalized_specialty = query.specialty.lower()
        result = await AvailabilityService.check_availability(
            query.region, query.comuna, query.area, normalized_specialty, query.time_range_filter, db
        )
        logger.debug(
            "Disponibilidad encontrada para region=%s, comuna=%s, area=%s, specialty=%s, time_range_filter=%s",
            query.region, query.comuna, query.area, normalized_specialty, query.time_range_filter
        )
        return result
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.critical("Error inesperado en el endpoint: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor. Por favor, intenta de nuevo más tarde."
        )
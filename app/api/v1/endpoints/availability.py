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
    summary="Check available appointments",
    responses={
        200: {"description": "Returns available appointments based on input"},
        400: {"description": "Invalid parameters provided"},
        404: {"description": "No available appointments found for the specified criteria"},
        500: {"description": "Internal server error"}
    }
)
async def check_availability(
    query: AvailabilityQuery = Depends(),
    db: AsyncSession = Depends(get_db)
) -> AvailabilityResponse:
    """
    Consulta la disponibilidad de citas médicas según región, comuna, área y especialidad.

    Args:
        query (AvailabilityQuery): Parámetros de consulta validados por Pydantic.
        db (AsyncSession): Sesión de base de datos inyectada.

    Returns:
        AvailabilityResponse: Respuesta con la disponibilidad encontrada.
    """
    try:
        normalized_specialty = query.specialty.lower()
        result = await AvailabilityService.check_availability(
            query.region, query.comuna, query.area, normalized_specialty, db
        )
        logger.info(
            "Disponibilidad encontrada para region=%s, comuna=%s, area=%s, specialty=%s",
            query.region, query.comuna, query.area, normalized_specialty
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
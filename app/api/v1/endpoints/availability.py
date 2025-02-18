from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.availability import AvailabilityResponse
from app.services.availability import AvailabilityService
from app.core.database import get_db

router = APIRouter()

@router.get(
    "/",
    response_model=AvailabilityResponse,
    status_code=200,
    summary="Check available appointments",
    responses={
        200: {"description": "Returns available appointments based on input"},
        404: {"description": "No available appointments found for the specified criteria"},
        500: {"description": "Internal server error"}
    }
)
async def check_availability(
    region: int = Query(..., description="Region for the appointment"),
    comuna: int = Query(..., description="Commune within the region"),
    area: str = Query(..., description="Medical area"),
    specialty: str = Query(..., description="Specialty within the medical area"),
    db: AsyncSession = Depends(get_db)
):
    # Aquí se asume que `AvailabilityService.check_availability` toma los parámetros necesarios y la sesión de base de datos.
    return await AvailabilityService.check_availability(region, comuna, area, specialty, db)
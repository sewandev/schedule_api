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
    region: int = Query(..., description="Region ID for the appointment"),
    comuna: int = Query(..., description="Commune ID within the region"),
    area: int = Query(..., description="Medical area ID"),
    specialty: str = Query(..., description="Specialty within the medical area"),
    db: AsyncSession = Depends(get_db)
):
    return await AvailabilityService.check_availability(region, comuna, area, specialty, db)
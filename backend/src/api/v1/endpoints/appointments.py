from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.appointments import AppointmentCreate, AppointmentResponse
from src.services.appointments import AppointmentService
from src.core.database import get_db

router = APIRouter()

@router.post(
    "/",
    response_model=AppointmentResponse,
    status_code=201,
    summary="Crea una nueva cita.",
    description="Crea una nueva cita en el sistema y depende de la disponibilidad de los médicos.",
    responses={
        201: {"description": "Cita agendada satisfactoriamente"},
        500: {"description": "Error interno del servidor"}
    }
)

async def create_appointment(
    data: AppointmentCreate,
    db: AsyncSession = Depends(get_db)
):
    return await AppointmentService.create_appointment(data, db)

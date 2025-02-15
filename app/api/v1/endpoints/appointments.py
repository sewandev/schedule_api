from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.appointments import AppointmentCreate, AppointmentResponse
from app.services.appointments import AppointmentService
from app.core.database import get_db

router = APIRouter()

@router.post(
    "/",
    response_model=AppointmentResponse,
    status_code=201,
    summary="Create new appointment",
    responses={
        201: {"description": "Appointment created successfully"},
        409: {"description": "Time slot not available"},
        500: {"description": "Internal server error"}
    }
)
async def create_appointment(
    data: AppointmentCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    ### Endpoint para enviar una solicitud de reserva de hora.

    **Returns:**
    - **201**: Cita agendada satisfactoriamente.
    - **409**: Cupo horario no disponible.
    - **500**: Error interno del servidor.
    """
    return await AppointmentService.create_appointment(data, db)

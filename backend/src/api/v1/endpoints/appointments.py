from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.schemas.appointments import AppointmentCreate, AppointmentResponse
from src.services.appointments import AppointmentService
from src.core.database import get_db
from src.core.logging_config import get_logger, setup_logging
from src.core.config import settings

setup_logging(log_level=settings.LOG_LEVEL, log_to_file=settings.LOG_TO_FILE)
logger = get_logger(__name__)

router = APIRouter()

@router.post(
    "/",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crea una nueva cita.",
    description="Crea una nueva cita en el sistema verificando disponibilidad de médicos.",
    responses={
        201: {
            "description": "Cita agendada satisfactoriamente",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "patient_id": 1,
                        "start_time": "2025-03-03T09:00:00",
                        "end_time": "2025-03-03T10:00:00"
                    }
                }
            }
        },
        400: {"description": "Datos de entrada inválidos"},
        409: {"description": "Conflicto de disponibilidad"},
        500: {"description": "Error interno del servidor"}
    }
)
async def create_appointment(data: AppointmentCreate, db: AsyncSession = Depends(get_db)) -> AppointmentResponse:
    logger.info(f"Solicitud recibida para crear cita: {data.model_dump()}")
    try:
        appointment = await AppointmentService.create_appointment(data, db)
        logger.info(f"Cita creada exitosamente con ID: {appointment.id}")
        return appointment
    except ValueError as ve:
        logger.error(f"Error de validación: {str(ve)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except IntegrityError as ie:
        logger.error(f"Conflicto de integridad en la base de datos: {str(ie)}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Conflicto de disponibilidad o datos duplicados"
        )
    except Exception as e:
        logger.error(f"Error inesperado al crear cita: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )
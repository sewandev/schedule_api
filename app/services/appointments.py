from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound
from app.repositories.appointments import AppointmentRepository
from app.schemas.appointments import AppointmentCreate, AppointmentResponse

# Clase que encapsula la lógica de negocio para la creación de citas
class AppointmentService:

    # Método estatico que creará una nueva cita y su data proviene de la clase AppointmentCreate que se encuenta en app/schemas/appointments.py y retornará un objeto de la clase AppointmentResponse
    @staticmethod
    async def create_appointment(data: AppointmentCreate, db: AsyncSession) -> AppointmentResponse:
        try:
            repo = AppointmentRepository(db)
            appointment = await repo.create(data)
            return AppointmentResponse.model_validate(appointment)
        except NoResultFound as e:
            # Manejo específico para slots no disponibles
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,  # 409 Conflict
                detail= f"Slot not available for medic_id={data.medic_id}, "
                        f"start_time={data.start_time}, end_time={data.end_time}"
            )
        except Exception as e:
            # Manejo de errores inesperados
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  # 500 Internal Server Error
                detail="An unexpected error occurred."
            )
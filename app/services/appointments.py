from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound
from app.repositories.appointments import AppointmentRepository
from app.schemas.appointments import AppointmentCreate, AppointmentResponse

'''
    Propósito de la capa de servicios
    La capa de servicios es responsable de:

    Contener la lógica de negocio: Aquí se implementan las reglas y operaciones específicas del dominio (en este caso, la creación de citas).
    Coordinación: Orquesta las interacciones entre los repositorios (que acceden a la base de datos) y otros componentes.
    Manejo de errores: Captura excepciones y las convierte en respuestas HTTP amigables para el cliente.
    Transformación de datos: Convierte los datos entre los formatos utilizados por la base de datos, los esquemas de validación y las respuestas de la API.
'''

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
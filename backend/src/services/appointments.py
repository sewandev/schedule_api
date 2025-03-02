from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound
from src.repositories.appointments import AppointmentRepository
from src.schemas.appointments import AppointmentCreate, AppointmentResponse

class AppointmentService:
    @staticmethod
    async def create_appointment(data: AppointmentCreate, db: AsyncSession) -> AppointmentResponse:
        try:
            repo = AppointmentRepository(db)
            appointment = await repo.create(data)
            return AppointmentResponse.model_validate(appointment)
        except NoResultFound as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail= f"Slot not available for medic_id={data.medic_id}, "
                        f"start_time={data.start_time}, end_time={data.end_time}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred."
            )
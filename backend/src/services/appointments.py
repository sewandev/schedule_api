from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.repositories.appointments import AppointmentRepository
from src.schemas.appointments import AppointmentCreate, AppointmentResponse

class AppointmentService:
    @staticmethod
    async def create_appointment(data: AppointmentCreate, db: AsyncSession) -> AppointmentResponse:
        repo = AppointmentRepository(db)
        try:
            appointment = await repo.create(data)
            return AppointmentResponse.model_validate(appointment)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred."
            )
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.appointments import AppointmentRepository
from app.schemas.appointments import AppointmentCreate, AppointmentResponse

class AppointmentService:
    @staticmethod
    async def create_appointment(
        data: AppointmentCreate,
        db: AsyncSession
    ) -> AppointmentResponse:
        repo = AppointmentRepository(db)
        try:
            appointment = await repo.create(data)
            return AppointmentResponse.model_validate(appointment)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
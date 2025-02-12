from sqlalchemy.orm import Session
from app.repositories.appointments import AppointmentRepository
from app.schemas.appointments import AppointmentCreate, AppointmentResponse

async def create_new_appointment(
    appointment_data: AppointmentCreate, db: Session
) -> AppointmentResponse:
    repo = AppointmentRepository(db)
    new_appointment = repo.create_appointment(appointment_data.dict())
    return new_appointment

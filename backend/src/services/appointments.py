from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.appointments import AppointmentCreate, AppointmentResponse
from src.repositories.appointments import AppointmentRepository
from src.core.logging_config import get_logger, setup_logging
from src.core.config import settings

setup_logging(log_level=settings.LOG_LEVEL, log_to_file=settings.LOG_TO_FILE)
logger = get_logger(__name__)

class AppointmentService:
    @staticmethod
    async def create_appointment(data: AppointmentCreate, db: AsyncSession) -> AppointmentResponse:
        logger.debug(f"Procesando reserva para slot ID: {data.id}")
        slot = await AppointmentRepository.get_available_slot(db, data.id)
        if not slot or slot.is_reserved:
            raise ValueError("El slot seleccionado no está disponible")
        appointment_data = {
            "patient_id": data.patient_id,
            "medic_id": slot.medic_id,
            "start_time": slot.start_time,
            "end_time": slot.end_time
        }
        appointment = await AppointmentRepository.create(db, appointment_data)
        await AppointmentRepository.mark_slot_as_reserved(db, slot.id)
        await db.commit()
        return AppointmentResponse(**appointment.__dict__)
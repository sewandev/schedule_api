from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from src.models.database_models import Appointment, AvailableSlot
from src.core.logging_config import get_logger, setup_logging
from src.core.config import settings

setup_logging(log_level=settings.LOG_LEVEL, log_to_file=settings.LOG_TO_FILE)
logger = get_logger(__name__)

class AppointmentRepository:
    @staticmethod
    async def get_available_slot(db: AsyncSession, slot_id: int) -> AvailableSlot:
        query = select(AvailableSlot).where(AvailableSlot.id == slot_id).with_for_update()
        sql_query = str(query.compile(compile_kwargs={"literal_binds": True}))
        logger.debug("Ejecutando consulta SQL:\n%s", sql_query)
        result = await db.execute(query)
        slot = result.scalar_one_or_none()
        logger.debug(f"Slot ID {slot_id} encontrado: {slot is not None}")
        return slot

    @staticmethod
    async def mark_slot_as_reserved(db: AsyncSession, slot_id: int):
        query = update(AvailableSlot).where(AvailableSlot.id == slot_id).values(is_reserved=True)
        await db.execute(query)
        logger.debug(f"Slot ID {slot_id} marcado como reservado")

    @staticmethod
    async def create(db: AsyncSession, data: dict) -> Appointment:
        appointment = Appointment(**data)
        db.add(appointment)
        await db.flush()
        logger.debug(f"Cita creada en DB con ID: {appointment.id}")
        return appointment
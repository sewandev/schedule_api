from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from src.models.models import Appointment, AvailableSlot
from src.core.logging_config import get_logger, setup_logging
from src.core.config import settings
from src.schemas.appointments import AppointmentCreate

setup_logging(log_level=settings.LOG_LEVEL, log_to_file=settings.LOG_TO_FILE)
logger = get_logger(__name__)

class AppointmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: AppointmentCreate) -> Appointment:
        try:
            stmt_slot = select(AvailableSlot.medic_id).where(AvailableSlot.id == data.id)
            logger.debug(f"SQL Query for slot: {str(stmt_slot)}")

            slot = await self.db.execute(stmt_slot)
            medic_id = slot.scalar_one_or_none()

            if medic_id is None:
                logger.error(f"No available slot found for id={data.id}")
                raise ValueError("No available slot found")

            stmt = insert(Appointment).values(
                patient_id=data.patient_id,
                medic_id=medic_id,
                start_time=data.start_time,
                end_time=data.end_time,
                status="pending"
            ).returning(Appointment)

            logger.debug(f"SQL Query: {str(stmt)}")

            result = await self.db.execute(stmt)
            await self.db.commit()

            appointment = result.scalar_one()
            await self.db.refresh(appointment)

            return appointment

        except Exception as e:
            logger.error(f"Error inserting appointment: {str(e)}")
            await self.db.rollback()
            raise
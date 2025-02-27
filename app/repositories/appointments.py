from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select, and_
from app.models.models import Appointment, AvailableSlot
from app.schemas.appointments import AppointmentCreate

class AppointmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: AppointmentCreate) -> Appointment:
        print("Datos recibidos en el repositorio:")
        print(f"patient_id: {data.patient_id}")
        print(f"medic_id: {data.medic_id}")
        print(f"start_time: {data.start_time}")
        print(f"end_time: {data.end_time}")

        slot = await self.db.execute(
            select(AvailableSlot).where(
                and_(
                    AvailableSlot.medic_id == data.medic_id,
                    AvailableSlot.start_time <= data.start_time,
                    AvailableSlot.end_time >= data.end_time,
                    AvailableSlot.is_reserved == False  
                )
            )
        )
        slot_result = slot.scalar()
        
        if not slot_result:
            raise NoResultFound("Slot not available")
        
        new_appointment = Appointment(**data.model_dump())
        self.db.add(new_appointment)
        
        slot_result.is_reserved = True
        
        try:
            await self.db.commit()
            await self.db.refresh(new_appointment)
        except Exception as e:
            print(f"Error al realizar commit: {e}")
            await self.db.rollback()
            raise

        return new_appointment

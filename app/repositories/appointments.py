from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models.models import Appointment, AvailableSlot
from app.schemas.appointments import AppointmentCreate
from datetime import datetime

class AppointmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: AppointmentCreate) -> Appointment:
        # Verificar disponibilidad
        slot = await self.db.execute(
            select(AvailableSlot).where(
                and_(
                    AvailableSlot.medic_id == data.medic_id,
                    AvailableSlot.start_time == data.start_time,
                    AvailableSlot.end_time == data.end_time,
                    AvailableSlot.is_reserved == False
                )
            )
        )
        slot_result = slot.scalar()

        if not slot_result:
            raise ValueError(
                f"Slot not available for medic_id={data.medic_id}, "
                f"start_time={data.start_time}, end_time={data.end_time}"
            )
        
        # Crear la cita
        new_appointment = Appointment(**data.model_dump())
        self.db.add(new_appointment)
        
        # Actualizar el estado del slot
        slot_result.is_reserved = True
        
        # Guardar los cambios
        await self.db.commit()
        await self.db.refresh(new_appointment)
        return new_appointment

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import AvailableSlot
from datetime import datetime

class UploadSchedulesRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_slot(self, medic_id: int, start_time: datetime, end_time: datetime) -> AvailableSlot:
        """
        Crea un nuevo slot disponible en la base de datos.
        
        Args:
            medic_id (int): ID del médico.
            start_time (datetime): Hora de inicio del slot.
            end_time (datetime): Hora de fin del slot.
        
        Returns:
            AvailableSlot: El slot creado.
        """
        new_slot = AvailableSlot(
            medic_id=medic_id,
            start_time=start_time,
            end_time=end_time,
            is_reserved=False,  # Por defecto, el slot no está reservado
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        self.db.add(new_slot)

        try:
            await self.db.commit()
            await self.db.refresh(new_slot)
        except Exception as e:
            print(f"Error al realizar commit: {e}")
            await self.db.rollback()  # Revierte la transacción en caso de error
            raise

        return new_slot
    
        
# app/repositories/availability.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, join
from app.models.models import AvailableSlot, Medic, Region, Comuna, Area
from app.schemas.availability import AvailableSlot as SchemaAvailableSlot

class AvailabilityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_available_slots(
        self, 
        region: str, 
        comuna: str, 
        area: str, 
        specialty: str, 
        is_reserved: bool = False
    ) -> list[SchemaAvailableSlot]:
        """
        Obtiene los slots disponibles para citas médicas basados en los filtros dados.
        
        :param region: Región donde se buscará la disponibilidad.
        :param comuna: Comuna dentro de la región.
        :param area: Área médica.
        :param specialty: Especialidad dentro del área médica.
        :param is_reserved: Filtro para slots no reservados (por defecto False).
        :return: Lista de slots disponibles convertidos a SchemaAvailableSlot.
        """
        # Construir la consulta con joins
        stmt = (
            select(AvailableSlot)
            .join(Medic, Medic.id == AvailableSlot.medic_id)
            .join(Region, Region.id == Medic.region_id)
            .join(Comuna, Comuna.id == Medic.comuna_id)
            .join(Area, Area.id == Medic.area_id)
            .where(
                and_(
                    Region.name == region,
                    Comuna.name == comuna,
                    Area.name == area,
                    Medic.specialty == specialty,
                    AvailableSlot.is_reserved == is_reserved
                )
            )
        )
        
        result = await self.db.execute(stmt)
        slots = result.scalars().all()
        
        # Convertir los slots de base de datos a objetos SchemaAvailableSlot
        return [
            SchemaAvailableSlot(
                medic_id=slot.medic_id,
                start_time=str(slot.start_time),  # Asumiendo que start_time es un datetime en la base de datos
                end_time=str(slot.end_time)       # Asumiendo que end_time es un datetime en la base de datos
            ) for slot in slots
        ]
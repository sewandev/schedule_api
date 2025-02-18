from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound
from app.repositories.availability import AvailabilityRepository
from app.schemas.availability import AvailabilityResponse, AvailableSlot

class AvailabilityService:

   @staticmethod
   async def check_availability(region: str, comuna: str, area: str, specialty: str, db: AsyncSession, repo: AvailabilityRepository) -> AvailabilityResponse:
        try:
            available_slots = await repo.get_available_slots(
                region=region, 
                comuna=comuna, 
                area=area, 
                specialty=specialty, 
                is_reserved=False
            )
            
            # Convertir los resultados de la base de datos a objetos AvailableSlot
            slots = [
                AvailableSlot(medic_id=slot.medic_id, start_time=slot.start_time, end_time=slot.end_time)
                for slot in available_slots
            ]

            return AvailabilityResponse(available_slots=slots)

        except NoResultFound:
            # No se encontraron slots disponibles, lo cual no es un conflicto sino una ausencia de datos
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No available appointments found for the specified criteria."
            )
        except Exception as e:
            # Manejar cualquier otro tipo de error
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while checking availability."
            )
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound
from app.repositories.availability import AvailabilityRepository
from app.schemas.availability import AvailabilityResponse, AvailableSlot, MedicAvailability
from collections import defaultdict

class AvailabilityService:

    @staticmethod
    async def check_availability(region: int, comuna: int, area: int, specialty: str, db: AsyncSession) -> AvailabilityResponse:
        repo = AvailabilityRepository(db)
        try:
            available_slots = await repo.get_available_slots(region, comuna, area, specialty, is_reserved=False)
            
            medic_slots = defaultdict(list)
            for slot in available_slots:
                # Asegúrate de que cada slot sea un AvailableSlot
                medic_slots[slot.medic_id].append(AvailableSlot(start_time=slot.start_time.isoformat(), 
                                                                end_time=slot.end_time.isoformat()))

            response_data = [
                MedicAvailability(medic_id=medic_id, slots=slots) 
                for medic_id, slots in medic_slots.items()
            ]

            return AvailabilityResponse(available_slots=response_data)

        except Exception as e:
            # Manejo más detallado de errores para depuración
            print(f"Error details: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while checking availability."
            )
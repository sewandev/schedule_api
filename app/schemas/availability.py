from pydantic import BaseModel
from typing import List

class AvailableSlot(BaseModel):
    start_time: str
    end_time: str

class MedicAvailability(BaseModel):
    medic_id: int
    slots: List[AvailableSlot]

class AvailabilityResponse(BaseModel):
    available_slots: List[MedicAvailability]
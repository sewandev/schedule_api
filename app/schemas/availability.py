from pydantic import BaseModel
from typing import List

class AvailableSlot(BaseModel):
    medic_id: int
    start_time: str
    end_time: str

class AvailabilityResponse(BaseModel):
    available_slots: List[AvailableSlot]
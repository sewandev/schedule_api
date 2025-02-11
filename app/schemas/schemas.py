from pydantic import BaseModel
from datetime import datetime

class ScheduleCreate(BaseModel):
    patient_id: int
    medic_id: int
    initial_date: datetime
    final_date: datetime


class ScheduleResponse(ScheduleCreate):
    id: int
    status: str

    class Config:
        from_attributes = True
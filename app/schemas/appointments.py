from pydantic import BaseModel
from datetime import datetime

class AppointmentCreate(BaseModel):
    patient_id: int
    medic_id: int
    initial_date: datetime
    final_date: datetime

class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    medic_id: int
    initial_date: datetime
    final_date: datetime
    status: str

    class Config:
        from_attributes = True
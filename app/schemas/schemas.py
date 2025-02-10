from pydantic import BaseModel
from datetime import datetime

class CitaCreate(BaseModel):
    paciente_id: int
    medico_id: int
    fecha_hora: datetime

class CitaResponse(CitaCreate):
    id: int
    estado: str

    class Config:
        from_attributes = True
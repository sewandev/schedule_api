from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import List

# Modelo para los parámetros de entrada
class AvailabilityQuery(BaseModel):
    region: int = Field(..., ge=1, description="Region ID for the appointment")
    comuna: int = Field(..., ge=1, description="Commune ID within the region")
    area: int = Field(..., ge=1, description="Medical area ID")
    specialty: str = Field(..., min_length=1, description="Specialty within the medical area")

    model_config = ConfigDict(
        # Desactivar coerción automática de tipos
        strict=True
    )

# Modelos para la respuesta
class AvailableSlot(BaseModel):
    start_time: str
    end_time: str

class MedicAvailability(BaseModel):
    medic_id: int
    slots: List[AvailableSlot]

class AvailabilityResponse(BaseModel):
    available_slots: List[MedicAvailability]
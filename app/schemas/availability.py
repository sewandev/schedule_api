from pydantic import BaseModel, Field, ConfigDict
from typing import List
from enum import Enum

class TimeRangeFilterEnum(str, Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    NIGHT = "night"

# Modelo para los parámetros de entrada
class AvailabilityQuery(BaseModel):
    region: int = Field(..., ge=1, le=999, description="Region ID for the appointment")
    comuna: int = Field(..., ge=1, le=999, description="Commune ID within the region")
    area: int = Field(..., ge=1, le=999, description="Medical area ID")
    specialty: str = Field(..., min_length=1, description="Specialty within the medical area")
    time_range_filter: TimeRangeFilterEnum = Field(..., min_length=1, description="Time range of the day")

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
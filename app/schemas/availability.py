from pydantic import BaseModel, Field, ConfigDict
from typing import List
from enum import Enum

class TimeRangeFilterEnum(str, Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    NIGHT = "night"

class AvailabilityQuery(BaseModel):
    region: int = Field(..., ge=1, le=999, description="Region ID for the appointment")
    comuna: int = Field(..., ge=1, le=999, description="Commune ID within the region")
    area: int = Field(..., ge=1, le=999, description="Medical area ID")
    specialty: str = Field(..., min_length=1, description="Specialty within the medical area")
    time_range_filter: TimeRangeFilterEnum = Field(..., description="Time range of the day")

    model_config = ConfigDict(
        strict=True
    )

class AvailableSlot(BaseModel):
    id: int
    start_time: str
    end_time: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "start_time": "2025-02-27T12:00:00",
                "end_time": "2025-02-27T12:30:00"
            }
        }
    )

class AvailabilityResponse(BaseModel):
    available_slots: List[AvailableSlot]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "available_slots": [
                    {"id": 1, "start_time": "2025-02-27T12:00:00", "end_time": "2025-02-27T12:30:00"},
                    {"id": 2, "start_time": "2025-02-27T13:00:00", "end_time": "2025-02-27T13:30:00"}
                ]
            }
        }
    )
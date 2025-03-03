from datetime import datetime
from pydantic import BaseModel, ValidationInfo, ConfigDict, Field, field_validator

class AppointmentBase(BaseModel):
    id: int = Field(..., ge=1, le=9999, description="Identificador único de la cita")
    patient_id: int = Field(..., ge=1, le=9999, description="ID del paciente")
    start_time: str = Field(..., description="Hora de inicio de la cita (debe ser futura y anterior a end_time)")
    end_time: str = Field(..., description="Hora de fin de la cita (debe ser posterior a start_time)")

    @field_validator("start_time")
    @classmethod
    def no_past_dates(cls, v: datetime) -> datetime:
        """Valida que start_time no sea una fecha pasada."""
        now = datetime.now()
        if v < now:
            raise ValueError("start_time no puede ser una fecha pasada")
        return v

    @field_validator("end_time")
    @classmethod
    def validate_times(cls, end_time: datetime, info: ValidationInfo) -> datetime:
        """Valida que end_time sea una fecha posterior al start_time."""
        start_time = info.data.get("start_time")
        if start_time is not None and end_time <= start_time:
            raise ValueError("End time must be after start time")
        return end_time

class AppointmentCreate(AppointmentBase):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "patient_id": 1,
                    "start_time": "2025-03-03T09:00:00",
                    "end_time": "2025-03-03T10:00:00"
                }
            ]
        }
    )

class AppointmentResponse(AppointmentBase):
    id: int
    medic_id: int
    status: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "patient_id": 1,
                "medic_id": 1,
                "start_time": "2025-02-13T09:00:00",
                "end_time": "2025-02-13T10:00:00",
                "status": "pending"
            }
        }

# Esquema para crear un nuevo pago
class PaymentCreate(BaseModel):
    appointment_id: int
    amount: int

    class Config:
        json_schema_extra = {
            "example": {
                "appointment_id": 1,
                "amount": 10000
            }
        }

# Esquema para la respuesta al iniciar un pago
class PaymentInitResponse(BaseModel):
    url: str
    token: str

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://webpay3g.transbank.cl/webpayserver/initTransaction",
                "token": "abc123xyz"
            }
        }

# Esquema para la respuesta al confirmar un pago
class PaymentCommitResponse(BaseModel):
    status: str
    payment_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "status": "approved",
                "payment_id": 1
            }
        }

# Esquema para la respuesta detallada de un pago
class PaymentResponse(BaseModel):
    id: int
    appointment_id: int
    amount: int
    transbank_token: str | None
    url: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "appointment_id": 1,
                "amount": 10000,
                "transbank_token": "abc123xyz",
                "url": "https://webpay3g.transbank.cl/webpayserver/initTransaction",
                "status": "pending",
                "created_at": "2025-02-22T10:00:00",
                "updated_at": "2025-02-22T10:00:00"
            }
        }
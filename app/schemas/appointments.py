from datetime import datetime
from pydantic import BaseModel, field_validator, ValidationInfo

# Clase base que contiene los atributos necesarios para crear una cita.
class AppointmentBase(BaseModel):
    patient_id: int
    medic_id: int
    start_time: datetime
    end_time: datetime

    @field_validator("end_time")
    def validate_times(cls, end_time: datetime, info: ValidationInfo) -> datetime:
        start_time = info.data.get("start_time")
        if start_time is not None and end_time <= start_time:
            raise ValueError("End time must be after start time")
        return end_time

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentResponse(AppointmentBase):
    id: int
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

# Esquema para crear un nuevo pago.
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

# Esquema para la respuesta al iniciar un pago.
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

# Esquema para la respuesta al confirmar un pago.
class PaymentCommitResponse(BaseModel):
    status: str  # Ej: "approved", "rejected"
    payment_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "status": "approved",
                "payment_id": 1
            }
        }

# Esquema para la respuesta detallada de un pago (útil para consultas futuras).
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
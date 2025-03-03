from datetime import datetime
from pydantic import BaseModel, ValidationInfo, ConfigDict, Field, field_validator

class AppointmentBase(BaseModel):
    patient_id: int = Field(..., description="ID del paciente")

class AppointmentCreate(AppointmentBase):
    id: int = Field(..., description="ID del slot disponible desde available_slots")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"id": 1, "patient_id": 1}]
        }
    )

class AppointmentResponse(AppointmentBase):
    id: int = Field(..., description="ID único de la cita")
    medic_id: int = Field(..., description="ID del médico")
    start_time: datetime = Field(..., description="Hora de inicio")
    end_time: datetime = Field(..., description="Hora de fin")
    status: str = Field(..., description="Estado de la cita")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "patient_id": 1,
                    "medic_id": 1,
                    "start_time": "2025-03-03T09:00:00",
                    "end_time": "2025-03-03T10:00:00",
                    "status": "pending"
                }
            ]
        }
    )

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
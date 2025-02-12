from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.appointments import create_new_appointment
from app.schemas.appointments import AppointmentCreate, AppointmentResponse
from app.core.database import get_db

router = APIRouter(prefix="/v1/appointments", tags=["appointments"])

@router.post("/", response_model=AppointmentResponse)
async def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
):
    try:
        return await create_new_appointment(appointment, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

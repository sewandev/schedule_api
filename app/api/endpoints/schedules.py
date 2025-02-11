from fastapi import APIRouter, Depends, HTTPException
from app.repositories.schedules import ScheduleRepository
from app.schemas.schemas import ScheduleCreate, ScheduleResponse
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/v1/schedules", tags=["schedules"])

@router.post(
    "/",
    response_model=ScheduleResponse,
    description="Crea una nueva cita médica",
    summary="Crear cita",
    response_description="Cita creada exitosamente",
    status_code=201
)

def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    repo = ScheduleRepository(db)
    return repo.create_schedule(schedule.dict())
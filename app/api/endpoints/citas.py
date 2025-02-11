from fastapi import APIRouter, Depends, HTTPException
from app.repositories.citas import CitaRepository
from app.schemas.schemas import CitaCreate, CitaResponse
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/v1/citas", tags=["citas"])

@router.post(
    "/",
    response_model=CitaResponse,
    description="Crea una nueva cita médica",
    summary="Crear cita",
    response_description="Cita creada exitosamente",
    status_code=201
)

def crear_cita(cita: CitaCreate, db: Session = Depends(get_db)):
    repo = CitaRepository(db)
    return repo.create_cita(cita.dict())
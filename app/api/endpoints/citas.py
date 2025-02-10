from fastapi import APIRouter, Depends, HTTPException
from app.repositories.citas import CitaRepository
from app.schemas.schemas import CitaCreate, CitaResponse
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/citas", tags=["citas"])

@router.post("/", response_model=CitaResponse)
def crear_cita(cita: CitaCreate, db: Session = Depends(get_db)):
    repo = CitaRepository(db)
    return repo.create_cita(cita.dict())
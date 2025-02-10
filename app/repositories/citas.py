from sqlalchemy.orm import Session
from app.models.models import Cita

class CitaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_cita(self, cita_id: int):
        return self.db.query(Cita).filter(Cita.id == cita_id).first()

    def create_cita(self, cita_data: dict):
        nueva_cita = Cita(**cita_data)
        self.db.add(nueva_cita)
        self.db.commit()
        self.db.refresh(nueva_cita)
        return nueva_cita
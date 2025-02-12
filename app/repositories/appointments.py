from sqlalchemy.orm import Session
from app.models.models import Appointment

class AppointmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_appointment(self, appointment_data: dict) -> Appointment:
        appointment = Appointment(**appointment_data)
        self.db.add(appointment)
        self.db.commit()
        self.db.refresh(appointment)
        return appointment

from sqlalchemy.orm import Session
from app.models.models import Schedule

class ScheduleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_schedule(self, schedule_id: int):
        return self.db.query(Schedule).filter(Schedule.id == schedule_id).first()

    def create_schedule(self, schedule_data: dict):
        new_schedule = Schedule(**schedule_data)
        self.db.add(new_schedule)
        self.db.commit()
        self.db.refresh(new_schedule)
        return new_schedule
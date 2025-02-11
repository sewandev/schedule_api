from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.core.database import Base

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)

class Medic(Base):
    __tablename__ = "medics"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    specialty = Column(String(50))

class Schedule(Base):
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id")) 
    medic_id = Column(Integer, ForeignKey("medics.id"))  
    initial_date = Column(DateTime)
    final_date = Column(DateTime)
    status = Column(String(20), default="pending")
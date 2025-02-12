from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from app.core.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)

class Medic(Base):
    __tablename__ = "medics"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    specialty = Column(String(50), nullable=False)
    # Relación con los intervalos disponibles
    available_slots = relationship("AvailableSlot", back_populates="medic")

class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id")) 
    medic_id = Column(Integer, ForeignKey("medics.id"))  
    initial_date = Column(DateTime)
    final_date = Column(DateTime)
    status = Column(String(20), default="pending")

class AvailableSlot(Base):
    __tablename__ = "available_slots"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    medic_id = Column(Integer, ForeignKey("medics.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_reserved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relación con la tabla de médicos
    medic = relationship("Medic", back_populates="available_slots")
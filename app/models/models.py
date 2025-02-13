from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

'''
Ventajas de usar ORM (Object-Relational Mapping):

Abstracción: No necesitas escribir SQL manualmente.
Seguridad: Previene vulnerabilidades como la inyección SQL.
Legibilidad: El código es más claro y fácil de mantener.
Productividad: Reduce la cantidad de código repetitivo.
Relaciones: Facilita el manejo de relaciones entre tablas.
Migraciones: Simplifica la evolución del esquema de la base de datos.
'''

class Patient(Base):
    __tablename__ = "patients"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100), index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="patient")

class Medic(Base):
    __tablename__ = "medics"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    specialty: Mapped[str] = mapped_column(String(50), nullable=False)
    available_slots: Mapped[list["AvailableSlot"]] = relationship(back_populates="medic")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="medic")

class Appointment(Base):
    __tablename__ = "appointments"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"))
    medic_id: Mapped[int] = mapped_column(ForeignKey("medics.id"))
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now().timestamp())
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.now().timestamp())
    
    patient: Mapped["Patient"] = relationship(back_populates="appointments")
    medic: Mapped["Medic"] = relationship(back_populates="appointments")

class AvailableSlot(Base):
    __tablename__ = "available_slots"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    medic_id: Mapped[int] = mapped_column(ForeignKey("medics.id"))
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    is_reserved: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now().timestamp())
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.now().timestamp())
    
    medic: Mapped["Medic"] = relationship(back_populates="available_slots")
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

class Region(Base):
    __tablename__ = "regiones"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    provinces: Mapped[list["Provincia"]] = relationship(back_populates="region")

class Provincia(Base):
    __tablename__ = "provincias"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    region_id: Mapped[int] = mapped_column(ForeignKey("regiones.id"))
    communes: Mapped[list["Comuna"]] = relationship(back_populates="province")
    region: Mapped["Region"] = relationship(back_populates="provinces")

class Comuna(Base):
    __tablename__ = "comunas"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    province_id: Mapped[int] = mapped_column(ForeignKey("provincias.id"))
    province: Mapped["Provincia"] = relationship(back_populates="communes")

class Area(Base):
    __tablename__ = "areas"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

class Patient(Base):
    __tablename__ = "patients"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100), index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    region_id: Mapped[int] = mapped_column(ForeignKey("regiones.id"), nullable=True)
    comuna_id: Mapped[int] = mapped_column(ForeignKey("comunas.id"), nullable=True)
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="patient")
    
    region: Mapped["Region"] = relationship()
    comuna: Mapped["Comuna"] = relationship()

class Medic(Base):
    __tablename__ = "medics"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    specialty: Mapped[str] = mapped_column(String(50), nullable=False)
    area_id: Mapped[int] = mapped_column(ForeignKey("areas.id"), nullable=True)
    region_id: Mapped[int] = mapped_column(ForeignKey("regiones.id"), nullable=True)
    comuna_id: Mapped[int] = mapped_column(ForeignKey("comunas.id"), nullable=True)
    available_slots: Mapped[list["AvailableSlot"]] = relationship(back_populates="medic")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="medic")
    
    area: Mapped["Area"] = relationship()
    region: Mapped["Region"] = relationship()
    comuna: Mapped["Comuna"] = relationship()

class Appointment(Base):
    __tablename__ = "appointments"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"))
    medic_id: Mapped[int] = mapped_column(ForeignKey("medics.id"))
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    
    patient: Mapped["Patient"] = relationship(back_populates="appointments")
    medic: Mapped["Medic"] = relationship(back_populates="appointments")

class AvailableSlot(Base):
    __tablename__ = "available_slots"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    medic_id: Mapped[int] = mapped_column(ForeignKey("medics.id"))
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    is_reserved: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    
    medic: Mapped["Medic"] = relationship(back_populates="available_slots")
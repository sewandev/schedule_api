from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Region(Base):
    __tablename__ = "regions"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    provinces: Mapped[list["Province"]] = relationship(back_populates="region")

class Province(Base):
    __tablename__ = "provinces"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"))
    communes: Mapped[list["Commune"]] = relationship(back_populates="province")
    region: Mapped["Region"] = relationship(back_populates="provinces")

class Commune(Base):
    __tablename__ = "communes"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    province_id: Mapped[int] = mapped_column(ForeignKey("provinces.id"))
    province: Mapped["Province"] = relationship(back_populates="communes")

class Area(Base):
    __tablename__ = "areas"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

class Patient(Base):
    __tablename__ = "patients"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100), index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"), nullable=True)
    commune_id: Mapped[int] = mapped_column(ForeignKey("communes.id"), nullable=True)
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="patient")
    region: Mapped["Region"] = relationship()
    commune: Mapped["Commune"] = relationship()

class Medic(Base):
    __tablename__ = "medics"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    specialty: Mapped[str] = mapped_column(String(50), nullable=False)
    area_id: Mapped[int] = mapped_column(ForeignKey("areas.id"), nullable=True)
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"), nullable=True)
    commune_id: Mapped[int] = mapped_column(ForeignKey("communes.id"), nullable=True)
    available_slots: Mapped[list["AvailableSlot"]] = relationship(back_populates="medic")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="medic")
    area: Mapped["Area"] = relationship()
    region: Mapped["Region"] = relationship()
    commune: Mapped["Commune"] = relationship()

class Appointment(Base):
    __tablename__ = "appointments"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"))
    medic_id: Mapped[int] = mapped_column(ForeignKey("medics.id"), index=True)
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    
    patient: Mapped["Patient"] = relationship(back_populates="appointments")
    medic: Mapped["Medic"] = relationship(back_populates="appointments")
    payment: Mapped["Payment"] = relationship(back_populates="appointment", uselist=False)

class AvailableSlot(Base):
    __tablename__ = "available_slots"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    medic_id: Mapped[int] = mapped_column(ForeignKey("medics.id"), index=True)
    start_time: Mapped[datetime] = mapped_column(DateTime, index=True)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    is_reserved: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    
    medic: Mapped["Medic"] = relationship(back_populates="available_slots")

class Payment(Base):
    __tablename__ = "payments"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    appointment_id: Mapped[int] = mapped_column(ForeignKey("appointments.id"), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    transbank_token: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    
    appointment: Mapped["Appointment"] = relationship(back_populates="payment")
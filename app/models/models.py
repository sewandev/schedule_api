from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.core.database import Base

class Paciente(Base):
    __tablename__ = "pacientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    email = Column(String(100), unique=True)

class Medico(Base):
    __tablename__ = "medicos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    especialidad = Column(String(50))

class Cita(Base):
    __tablename__ = "citas"
    
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id")) 
    medico_id = Column(Integer, ForeignKey("medicos.id"))  
    fecha_hora = Column(DateTime)
    estado = Column(String(20), default="pendiente")
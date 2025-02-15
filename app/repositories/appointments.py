from sqlalchemy.ext.asyncio import AsyncSession # Es una sesión asíncrona de SQLAlchemy para interactuar con la base de datos de manera no bloqueante.
from sqlalchemy.exc import NoResultFound # Excepción que se lanza cuando no se encuentra un resultado en una consulta.
from sqlalchemy import select, and_ # Funciones de SQLAlchemy para construir consultas SQL.
from app.models.models import Appointment, AvailableSlot # Modelos de la base de datos que representan las tablas de citas y slots disponibles.
from app.schemas.appointments import AppointmentCreate # Esquema de validación para la creación de citas.

# Propósito: Esta clase encapsula la lógica para interactuar con la base de datos relacionada con las citas.
class AppointmentRepository:
    def __init__(self, db: AsyncSession): # Recibe una sesión de base de datos (AsyncSession) y la almacena en self.db
        self.db = db

    # Propósito: Método asincrónico que crea una nueva cita en la base de datos -> Retorna: Un objeto de tipo Appointment que representa la cita creada.
    async def create(self, data: AppointmentCreate) -> Appointment:
        print("Datos recibidos en el repositorio:")
        print(f"patient_id: {data.patient_id}")
        print(f"medic_id: {data.medic_id}")
        print(f"start_time: {data.start_time}")
        print(f"end_time: {data.end_time}")

        # Verifica si el slot de tiempo solicitado está disponible para el médico (medic_id) en el horario especificado.
        slot = await self.db.execute(
            select(AvailableSlot).where(
                and_(
                    AvailableSlot.medic_id == data.medic_id,
                    AvailableSlot.start_time <= data.start_time,  # La hora de inicio debe ser mayor o igual al inicio del slot
                    AvailableSlot.end_time >= data.end_time,  # La hora de fin debe ser menor o igual al fin del slot
                    AvailableSlot.is_reserved == False  # El slot no debe estar reservado
                )
            )
            # SQL equivalente: SELECT * FROM available_slot WHERE medic_id = medic_id AND start_time <= start_time AND end_time >= end_time AND is_reserved = FALSE;
        )
        slot_result = slot.scalar()
        
        # Si no se encuentra un slot disponible, lanza una excepción.
        if not slot_result:
            raise NoResultFound("Slot not available")  # Excepción específica
        
        # Crear la cita
        new_appointment = Appointment(**data.model_dump())
        self.db.add(new_appointment)
        
        # Actualizar el estado del slot
        slot_result.is_reserved = True
        
        # Guardar los cambios
        try:
            await self.db.commit()
            await self.db.refresh(new_appointment)
        except Exception as e:
            print(f"Error al realizar commit: {e}")
            await self.db.rollback()  # Revierte la transacción en caso de error
            raise
        
        # Retorna los datos de la cita creada en la BD.
        return new_appointment

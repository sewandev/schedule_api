# app/dummy_data_generator.py

import logging
from logging.handlers import RotatingFileHandler
from sqlalchemy import text, inspect
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, ProgrammingError
from datetime import datetime, date
import asyncio
import os
from app.models.models import Region, Provincia, Comuna, Area, AvailableSlot, Medic, Appointment, Patient
from app.core.database import AsyncSessionLocal, engine

# Configuración del logger
logger = logging.getLogger("reserva-hora-api-dummy")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

log_dir = "/tmp/logs" if os.getenv("VERCEL") else "logs"
os.makedirs(log_dir, exist_ok=True)
file_handler = RotatingFileHandler(
    filename=os.path.join(log_dir, "dummy_data.log"),
    maxBytes=10*1024*1024,
    backupCount=5,
    encoding="utf-8"
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

async def check_tables_exist():
    """Verifica si todas las tablas esperadas existen en la base de datos."""
    async with engine.connect() as conn:
        def sync_inspector(connection):
            inspector = inspect(connection)
            # Forzar actualización del estado de las tablas
            return inspector.get_table_names(schema="public")
        
        existing_tables = await conn.run_sync(sync_inspector)
        expected_tables = [
            Appointment.__tablename__,
            AvailableSlot.__tablename__,
            Medic.__tablename__,
            Patient.__tablename__,
            Provincia.__tablename__,
            Comuna.__tablename__,
            Region.__tablename__,
            Area.__tablename__
        ]
        missing_tables = [table for table in expected_tables if table not in existing_tables]
        
        if missing_tables:
            logger.error("Faltan las siguientes tablas en la base de datos: %s", missing_tables)
            return False
        logger.debug("Todas las tablas esperadas existen: %s", expected_tables)
        return True

async def clear_tables(session):
    """Trunca todas las tablas especificadas en la base de datos si existen."""
    if not await check_tables_exist():
        raise RuntimeError(
            "No se pueden truncar las tablas porque algunas no existen. "
            "Asegúrate de que las tablas estén creadas antes de ejecutar este script."
        )
    
    try:
        tables = [
            Appointment.__tablename__,
            AvailableSlot.__tablename__,
            Medic.__tablename__,
            Patient.__tablename__,
            Provincia.__tablename__,
            Comuna.__tablename__,
            Region.__tablename__,
            Area.__tablename__
        ]
        truncate_query = text(f"TRUNCATE TABLE {', '.join(tables)} RESTART IDENTITY CASCADE;")
        logger.debug("Ejecutando consulta de truncado: %s", truncate_query)
        await session.execute(truncate_query)
        await session.commit()
        logger.info("Todas las tablas han sido truncadas exitosamente.")
    except IntegrityError as ie:
        logger.error("Error de integridad al truncar tablas: %s", str(ie), exc_info=True)
        await session.rollback()
        raise
    except SQLAlchemyError as sae:
        logger.error("Error de SQLAlchemy al truncar tablas: %s", str(sae), exc_info=True)
        await session.rollback()
        raise
    except Exception as e:
        logger.critical("Error inesperado al truncar tablas: %s", str(e), exc_info=True)
        await session.rollback()
        raise

async def insert_dummy_data():
    """Inserta datos ficticios en la base de datos para propósitos de desarrollo."""
    async with AsyncSessionLocal() as session:
        logger.info("Iniciando inserción de datos ficticios.")
        try:
            await clear_tables(session)

            # Insertar regiones
            regions = [Region(name="Región Metropolitana de Santiago")]
            session.add_all(regions)
            await session.flush()
            logger.debug("Regiones insertadas: %s", [r.name for r in regions])

            # Insertar provincias
            provinces = [
                Provincia(name="Provincia de Santiago", region_id=1),
                Provincia(name="Provincia de Cordillera", region_id=1),
            ]
            session.add_all(provinces)
            await session.flush()
            logger.debug("Provincias insertadas: %s", [p.name for p in provinces])

            # Insertar comunas
            communes = [
                Comuna(name="Santiago", province_id=1),
                Comuna(name="Cerrillos", province_id=1),
                Comuna(name="Cerro Navia", province_id=1),
                Comuna(name="Conchalí", province_id=1),
                Comuna(name="El Bosque", province_id=1),
                Comuna(name="Estación Central", province_id=1),
            ]
            session.add_all(communes)
            await session.flush()
            logger.debug("Comunas insertadas: %s", [c.name for c in communes])

            # Insertar áreas médicas
            areas = [
                Area(name="Kinesiología"),
                Area(name="Cardiología"),
                Area(name="Fonoaudiología"),
            ]
            session.add_all(areas)
            await session.flush()
            logger.debug("Áreas insertadas: %s", [a.name for a in areas])

            # Insertar pacientes
            patients = [
                Patient(full_name="Juan Pérez", email="juan.perez@example.com", region_id=1, comuna_id=1),
                Patient(full_name="María López", email="maria.lopez@example.com", region_id=1, comuna_id=2),
            ]
            session.add_all(patients)
            await session.flush()
            logger.debug("Pacientes insertados: %s", [p.full_name for p in patients])

            # Insertar médicos
            medics = [
                Medic(id=1, full_name="Dr Mavencio Dota N00b", specialty="Trauma", area_id=3, region_id=1, comuna_id=1),
                Medic(id=2, full_name="Dr SeWaN Oliva Ogre", specialty="Trauma", area_id=3, region_id=1, comuna_id=1),
                Medic(id=3, full_name="Dra Pepe Julian Onzima", specialty="Trauma", area_id=3, region_id=1, comuna_id=1),
            ]
            session.add_all(medics)
            await session.flush()
            logger.debug("Médicos insertados: %s", [m.full_name for m in medics])

            # Insertar horarios disponibles
            today = date.today()
            slots = [
                AvailableSlot(
                    medic_id=1,
                    start_time=datetime(today.year, today.month, today.day, hour, 0),
                    end_time=datetime(today.year, today.month, today.day, hour+1, 0)
                )
                for hour in range(9, 18)
            ]
            session.add_all(slots)
            await session.flush()
            logger.debug("Horarios disponibles insertados: %d slots", len(slots))

            # Insertar citas
            appointments = [
                Appointment(
                    patient_id=1,
                    medic_id=1,
                    start_time=datetime(today.year, today.month, today.day, 9, 0),
                    end_time=datetime(today.year, today.month, today.day, 10, 0),
                    status="confirmed"
                )
            ]
            session.add_all(appointments)
            await session.flush()
            logger.debug("Citas insertadas: %d appointments", len(appointments))

            await session.commit()
            logger.info("Datos ficticios insertados exitosamente.")
        except IntegrityError as ie:
            logger.error("Error de integridad al insertar datos: %s", str(ie), exc_info=True)
            await session.rollback()
            raise
        except SQLAlchemyError as sae:
            logger.error("Error de SQLAlchemy al insertar datos: %s", str(sae), exc_info=True)
            await session.rollback()
            raise
        except Exception as e:
            logger.critical("Error inesperado al insertar datos: %s", str(e), exc_info=True)
            await session.rollback()
            raise
        finally:
            logger.debug("Finalizando operación de inserción de datos ficticios.")
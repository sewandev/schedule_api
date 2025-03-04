from sqlalchemy import text, inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from datetime import datetime, date, timedelta
from src.core.config import settings
from src.models.database_models import Region, Province, Commune, Area, AvailableSlot, Medic, Appointment, Patient, Payment
from src.core.database import AsyncSessionLocal, engine
from src.core.logging_config import setup_logging, get_logger

setup_logging(log_level=settings.LOG_LEVEL, log_to_file=settings.LOG_TO_FILE)
logger = get_logger(__name__)

async def check_tables_exist() -> bool:
    async with engine.connect() as conn:
        def sync_inspector(connection):
            inspector = inspect(connection)
            return inspector.get_table_names(schema="public")
        
        existing_tables = await conn.run_sync(sync_inspector)
        expected_tables = [
            Payment.__tablename__,
            Appointment.__tablename__,
            AvailableSlot.__tablename__,
            Medic.__tablename__,
            Patient.__tablename__,
            Province.__tablename__,
            Commune.__tablename__,
            Region.__tablename__,
            Area.__tablename__
        ]
        missing_tables = [table for table in expected_tables if table not in existing_tables]
        
        if missing_tables:
            logger.error("Faltan las siguientes tablas en la base de datos: %s", missing_tables)
            return False
        logger.debug("Todas las tablas esperadas existen: %s", expected_tables)
        return True

async def clear_tables(session: AsyncSession) -> None:
    if not await check_tables_exist():
        raise RuntimeError(
            "No se pueden truncar las tablas porque algunas no existen. "
            "Asegúrate de que las tablas estén creadas antes de ejecutar este script."
        )
    
    try:
        tables = [
            Payment.__tablename__,
            Appointment.__tablename__,
            AvailableSlot.__tablename__,
            Medic.__tablename__,
            Patient.__tablename__,
            Province.__tablename__,
            Commune.__tablename__,
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

async def insert_dummy_data() -> None:
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
                Province(name="Provincia de Santiago", region_id=1),
                Province(name="Provincia de Cordillera", region_id=1),
            ]
            session.add_all(provinces)
            await session.flush()
            logger.debug("Provincias insertadas: %s", [p.name for p in provinces])

            # Insertar comunas
            communes = [
                Commune(name="Santiago", province_id=1),
                Commune(name="Cerrillos", province_id=1),
                Commune(name="Cerro Navia", province_id=1),
                Commune(name="Conchalí", province_id=1),
                Commune(name="El Bosque", province_id=1),
                Commune(name="Estación Central", province_id=1),
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
                Patient(full_name="Juan Pérez", email="juan.perez@example.com", region_id=1, commune_id=1),
                Patient(full_name="María López", email="maria.lopez@example.com", region_id=1, commune_id=2),
            ]
            session.add_all(patients)
            await session.flush()
            logger.debug("Pacientes insertados: %s", [p.full_name for p in patients])

            # Insertar médicos
            medics = [
                Medic(id=1, full_name="Dr Mavencio Dota N00b", specialty="trauma", area_id=3, region_id=1, commune_id=1),
                Medic(id=2, full_name="Dr SeWaN Oliva Ogre", specialty="trauma", area_id=3, region_id=1, commune_id=1),
                Medic(id=3, full_name="Dra Pepe Julian Onzima", specialty="trauma", area_id=3, region_id=1, commune_id=1),
            ]
            session.add_all(medics)
            await session.flush()
            logger.debug("Médicos insertados: %s", [m.full_name for m in medics])

            # Insertar horarios disponibles
            today = date.today()
            medic_ids = [1, 2, 3]
            hours = range(9, 12)

            slots = [
                AvailableSlot(
                    medic_id=medic_id,
                    start_time=datetime(today.year, today.month, today.day, hour, 0) + timedelta(days=day_offset),
                    end_time=datetime(today.year, today.month, today.day, hour + 1, 0) + timedelta(days=day_offset),
                    is_reserved=False
                )
                for day_offset in range(3)
                for medic_id in medic_ids
                for hour in hours
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
from app.models.models import Region, Provincia, Comuna, Area, AvailableSlot, Medic, Appointment
from app.core.database import AsyncSessionLocal
from datetime import datetime, date
from sqlalchemy import delete
import asyncio

async def clear_tables(session):
    """Elimina todos los datos de las tablas antes de insertar nuevos datos ficticios."""
    try:
        for table in [Appointment, AvailableSlot, Medic, Provincia, Comuna, Region, Area]:
            await session.execute(delete(table))
        await session.commit()
        print("All tables have been cleared.")
    except Exception as e:
        await session.rollback()
        print(f"Error clearing tables: {e}")

async def insert_dummy_data():
    """Inserta datos ficticios en la base de datos."""
    async with AsyncSessionLocal() as session:
        try:
            await clear_tables(session)

            # Insertar regiones
            regions = [Region(name="Región Metropolitana de Santiago")]
            session.add_all(regions)
            
            # Insertar provincias
            provinces = [
                Provincia(name="Provincia de Santiago", region_id=1),
                Provincia(name="Provincia de Cordillera", region_id=1),
            ]
            session.add_all(provinces)

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

            # Insertar áreas médicas
            areas = [
                Area(name="Kinesiología"),
                Area(name="Cardiología"),
                Area(name="Fonoaudiología"),
            ]
            session.add_all(areas)

            # Insertar médicos
            medics = [
                Medic(id=1, full_name="Dr Mavencio Dota N00b", specialty="Trauma", area_id=3, region_id=1, comuna_id=1),
                Medic(id=2, full_name="Dr SeWaN Oliva Ogre", specialty="Trauma", area_id=3, region_id=1, comuna_id=1),
                Medic(id=3, full_name="Dra Pepe Julian Onzima", specialty="Trauma", area_id=3, region_id=1, comuna_id=1),
            ]
            session.add_all(medics)

            # Insertar horarios disponibles
            today = date.today()
            slots = [
                AvailableSlot(medic_id=1, start_time=datetime(today.year, today.month, today.day, hour, 0), 
                              end_time=datetime(today.year, today.month, today.day, hour+1, 0))
                for hour in range(9, 18)
            ]
            session.add_all(slots)
            
            await session.commit()
            print("Dummy data inserted successfully.")
        except Exception as e:
            await session.rollback()
            print(f"Error inserting dummy data: {e}")

if __name__ == "__main__":
    asyncio.run(insert_dummy_data())
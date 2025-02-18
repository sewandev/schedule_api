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
            regions = [Region(id=1, name="Región Metropolitana de Santiago")]
            session.add_all(regions)
            
            # Insertar provincias
            provinces = [
                Provincia(id=1, name="Provincia de Santiago", region_id=1),
                Provincia(id=2, name="Provincia de Cordillera", region_id=1),
            ]
            session.add_all(provinces)

            # Insertar comunas
            communes = [
                Comuna(id=1, name="Santiago", province_id=1),
                Comuna(id=2, name="Cerrillos", province_id=1),
                Comuna(id=3, name="Cerro Navia", province_id=1),
                Comuna(id=4, name="Conchalí", province_id=1),
                Comuna(id=5, name="El Bosque", province_id=1),
                Comuna(id=6, name="Estación Central", province_id=1),
                Comuna(id=7, name="Huechuraba", province_id=1),
                Comuna(id=8, name="Independencia", province_id=1),
                Comuna(id=9, name="La Cisterna", province_id=1),
                Comuna(id=10, name="La Florida", province_id=1),
                Comuna(id=11, name="La Granja", province_id=1),
                Comuna(id=12, name="La Pintana", province_id=1),
                Comuna(id=13, name="La Reina", province_id=1),
                Comuna(id=14, name="Las Condes", province_id=1),
                Comuna(id=15, name="Lo Barnechea", province_id=1),
                Comuna(id=16, name="Lo Espejo", province_id=1),
                Comuna(id=17, name="Lo Prado", province_id=1),
                Comuna(id=18, name="Macul", province_id=1),
                Comuna(id=19, name="Maipú", province_id=1),
                Comuna(id=20, name="Ñuñoa", province_id=1),
                Comuna(id=21, name="Pedro Aguirre Cerda", province_id=1),
                Comuna(id=22, name="Peñalolén", province_id=1),
                Comuna(id=23, name="Providencia", province_id=1),
                Comuna(id=24, name="Pudahuel", province_id=1),
                Comuna(id=25, name="Quilicura", province_id=1),
                Comuna(id=26, name="Quinta Normal", province_id=1),
                Comuna(id=27, name="Recoleta", province_id=1),
                Comuna(id=28, name="Renca", province_id=1),
                Comuna(id=29, name="San Joaquín", province_id=1),
                Comuna(id=30, name="San Miguel", province_id=1),
                Comuna(id=31, name="San Ramón", province_id=1),
                Comuna(id=32, name="Vitacura", province_id=1),
                Comuna(id=33, name="Puente Alto", province_id=2),  # Cordillera
                Comuna(id=34, name="Pirque", province_id=2),  # Cordillera
                Comuna(id=35, name="San José de Maipo", province_id=2),  # Cordillera
            ]
            session.add_all(communes)

            # Insertar áreas médicas
            areas = [
                Area(id=1, name="Kinesiología"),
                Area(id=2, name="Cardiología"),
                Area(id=3, name="Fonoaudiología"),
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

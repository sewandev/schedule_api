from app.models.models import Region, Provincia, Comuna, Area, AvailableSlot, Medic, Appointment
from app.core.database import AsyncSessionLocal
from datetime import datetime, date
from sqlalchemy import delete

import asyncio

async def horarios_disponibles():
    async with AsyncSessionLocal() as session:
        try:
            # Datos ficticios para horarios disponibles (available_slots)
            today = date.today()
            horarios_data = [
                AvailableSlot(medic_id=1, start_time=datetime(today.year, today.month, today.day, 9, 0), end_time=datetime(today.year, today.month, today.day, 10, 0)),
                AvailableSlot(medic_id=1, start_time=datetime(today.year, today.month, today.day, 10, 0), end_time=datetime(today.year, today.month, today.day, 11, 0)),
                AvailableSlot(medic_id=1, start_time=datetime(today.year, today.month, today.day, 11, 0), end_time=datetime(today.year, today.month, today.day, 12, 0)),
                AvailableSlot(medic_id=1, start_time=datetime(today.year, today.month, today.day, 12, 0), end_time=datetime(today.year, today.month, today.day, 13, 0)),
                AvailableSlot(medic_id=1, start_time=datetime(today.year, today.month, today.day, 13, 0), end_time=datetime(today.year, today.month, today.day, 14, 0)),
                AvailableSlot(medic_id=1, start_time=datetime(today.year, today.month, today.day, 15, 0), end_time=datetime(today.year, today.month, today.day, 16, 0)),
                AvailableSlot(medic_id=1, start_time=datetime(today.year, today.month, today.day, 16, 0), end_time=datetime(today.year, today.month, today.day, 17, 0)),
                AvailableSlot(medic_id=1, start_time=datetime(today.year, today.month, today.day, 17, 0), end_time=datetime(today.year, today.month, today.day, 18, 0)),
            ]
            
            for horario in horarios_data:
                session.add(horario)

            await session.commit()
        except Exception as e:
            await session.rollback()
            print(f"An error occurred: {e}")
        finally:
            await session.close()

async def medicos():
    async with AsyncSessionLocal() as session:
        try:
            # Datos ficticios para medicos
            medicos_data = [
                Medic(id=1, full_name="Dr Mavencio Dota N00b", specialty="Trauma", area_id=3, region_id=1, comuna_id=1),
                Medic(id=2, full_name="Dr SeWaN Oliva Ogre", specialty="Trauma", area_id=3, region_id=1, comuna_id=1),
                Medic(id=3, full_name="Dra Pepe Julian Onzima", specialty="Trauma", area_id=3, region_id=1, comuna_id=1),
            ]
            
            for medico in medicos_data:
                session.add(medico)

            await session.commit()
        except Exception as e:
            await session.rollback()
            print(f"An error occurred: {e}")
        finally:
            await session.close()
        
async def regiones_comunas_provincias():
    async with AsyncSessionLocal() as session:
        try:
            # Datos ficticios para Region
            regions_data = [
                Region(id=1, name="Región Metropolitana de Santiago"),
            ]
            
            for region in regions_data:
                session.add(region)

            # Datos ficticios para Provincia
            provinces_data = [
                Provincia(id=1, name="Provincia de Santiago", region_id=1),
                Provincia(id=2, name="Provincia de Cordillera", region_id=1),
            ]
            
            for province in provinces_data:
                session.add(province)

            # Datos ficticios para Comuna
            communes_data = [
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
            
            for commune in communes_data:
                session.add(commune)

            # Datos ficticios para Area
            areas_data = [
                Area(id=1, name="Kinesiología"),
                Area(id=2, name="Cardiología"),
                Area(id=3, name="Fonoaudiología"),
                # ... Añadir más áreas según sea necesario
            ]
            
            for area in areas_data:
                session.add(area)

            await session.commit()
        except Exception as e:
            await session.rollback()
            print(f"An error occurred: {e}")
        finally:
            await session.close()

async def main():
    async with AsyncSessionLocal() as session:
        try:
            # Ahora sí estamos llamando a vaciar_tablas
            await vaciar_tablas(session)
            await regiones_comunas_provincias(session)
            await horarios_disponibles(session)
            await medicos(session)
            await session.commit()
            print("Datos ficticios insertados con éxito.")
        except Exception as e:
            await session.rollback()
            print(f"An error occurred in main: {e}")
            
async def vaciar_tablas(session):
    try:
        for table in [Appointment, AvailableSlot, Medic, Comuna, Provincia, Region, Area]:
            await session.execute(delete(table))
        print("Todas las tablas han sido vaciadas.")
    except Exception as e:
        await session.rollback()
        print(f"Error al vaciar tablas: {e}")

if __name__ == "__main__":
    asyncio.run(main())
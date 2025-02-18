from app.models.models import Region, Provincia, Comuna, Area
from app.core.database import AsyncSessionLocal

import asyncio

async def insert_seed_data():
    async with AsyncSessionLocal() as session:
        try:
            # Datos ficticios para Region
            regions_data = [
                Region(id=1, name="Región de Tarapacá"),
                Region(id=2, name="Región de Antofagasta"),
                # ... Añadir más regiones según sea necesario
            ]
            
            for region in regions_data:
                session.add(region)

            # Datos ficticios para Provincia
            provinces_data = [
                Provincia(id=1, name="Provincia de Iquique", region_id=1),
                Provincia(id=2, name="Provincia de El Tamarugal", region_id=1),
                # ... Añadir más provincias según sea necesario
            ]
            
            for province in provinces_data:
                session.add(province)

            # Datos ficticios para Comuna
            communes_data = [
                Comuna(id=1, name="Iquique", province_id=1),
                Comuna(id=2, name="Alto Hospicio", province_id=1),
                # ... Añadir más comunas según sea necesario
            ]
            
            for commune in communes_data:
                session.add(commune)

            # Datos ficticios para Area
            areas_data = [
                Area(id=1, name="Pediatría"),
                Area(id=2, name="Cardiología"),
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

if __name__ == "__main__":
    asyncio.run(insert_seed_data())
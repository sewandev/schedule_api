from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base, logger as db_logger
from app.core.config import settings
from app.api.routes import api_router
from app.dummy_data_generator import insert_dummy_data
from app.models.models import Base

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_logger.info("Iniciando lifespan: creación de tablas y datos dummy.")
    
    # Verifica las tablas registradas en Base.metadata
    registered_tables = list(Base.metadata.tables.keys())
    db_logger.info("Tablas registradas en Base.metadata antes de create_all: %s", registered_tables)
    
    async with engine.begin() as conn:
        db_logger.info("Ejecutando Base.metadata.create_all para crear tablas.")
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()  # Commit explícito para asegurar que las tablas estén visibles
        db_logger.info("Creación de tablas completada, procediendo a insertar datos dummy.")
        await insert_dummy_data()
    db_logger.info("Lifespan completado.")
    yield

app = FastAPI(lifespan=lifespan)

# Creación de la aplicación FastAPI
app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# Configuración CORS mejorada
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

# Registrar todos los routers
app.include_router(api_router, prefix=settings.API_PREFIX)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
    )
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.api.routes import api_router
from src.core.config import settings
from src.core.database import Base, engine
from src.core.logging_config import get_logger, setup_logging, LOG_DIR
from src.dummy_data_generator import insert_dummy_data

setup_logging(log_level=settings.LOG_LEVEL, log_to_file=settings.LOG_TO_FILE)
logger = get_logger(__name__)

# Definir el lifespan de la aplicación
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando lifespan: creación de tablas y datos dummy.")
    
    # Verifica las tablas registradas en Base.metadata
    registered_tables = list(Base.metadata.tables.keys())
    logger.debug("Tablas registradas en Base.metadata antes de create_all: %s", registered_tables)
    
    async with engine.begin() as conn:
        logger.info("Ejecutando Base.metadata.create_all para crear tablas.")
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
        logger.info("Creación de tablas completada, procediendo a insertar datos dummy.")
        await insert_dummy_data()
    logger.info("Lifespan completado.")
    yield

# Crear la aplicación FastAPI
app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1, "syntaxHighlight": {"theme": "obsidian"}},
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

# Montar la carpeta logs como archivos estáticos
app.mount("/logs", StaticFiles(directory=LOG_DIR), name="logs")

# Registrar todos los routers
app.include_router(api_router, prefix=settings.API_PREFIX)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
    )
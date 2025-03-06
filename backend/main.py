from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from src.api.routes import api_router
from src.core.config import settings
from src.core.database import engine
from src.models.database_models import Base
from src.core.logging_config import get_logger, setup_logging, LOG_DIR
from src.dummy_data_generator import insert_dummy_data

setup_logging(log_level=settings.LOG_LEVEL, log_to_file=settings.LOG_TO_FILE)
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Iniciando lifespan: creación de tablas y datos dummy.")
    registered_tables = list(Base.metadata.tables.keys())
    logger.debug("Tablas registradas en Base.metadata antes de create_all: %s", registered_tables)
    
    try:
        async with engine.begin() as conn:
            logger.info("Ejecutando Base.metadata.create_all para crear tablas.")
            await conn.run_sync(Base.metadata.create_all)
            await conn.commit()
            logger.info("Creación de tablas completada, procediendo a insertar datos dummy.")
            await insert_dummy_data()
    except Exception as e:
        logger.critical("Error durante el lifespan: %s", str(e), exc_info=True)
        raise
    
    logger.info("Lifespan completado.")
    yield

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1, "syntaxHighlight": {"theme": "obsidian"}},
    lifespan=lifespan
)

ALLOWED_IPS = {"186.79.236.112", "127.0.0.1"}

@app.middleware("http")
async def validate_ip(request: Request, call_next):
    client_ip = request.client.host
    if client_ip not in ALLOWED_IPS:
        return JSONResponse(status_code=403, content={"detail": "IP no autorizada"})
    return await call_next(request)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True if settings.APP_ENVIRONMENT != "production" else False,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
    expose_headers=settings.CORS_EXPOSE_HEADERS
)

if settings.APP_ENVIRONMENT == "development":
    app.mount("/logs", StaticFiles(directory=LOG_DIR), name="logs")

app.include_router(api_router, prefix=settings.APP_API_PREFIX)
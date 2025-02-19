from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.core.config import settings
from app.api.routes import api_router
from app.dummy_data import insert_dummy_data  # Importa la función de datos dummy

# Decorador y método asincrónico que se encarga de crear las tablas de la BD cada vez que se inicia la aplicación
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Asegura que las tablas existen
    if settings.ENVIRONMENT in ("development","production"): # Solo de forma momentanea
        await insert_dummy_data()  # Inserta datos ficticios solo en desarrollo
    yield

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
        reload=settings.DEBUG
    )
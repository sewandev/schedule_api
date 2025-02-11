from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.api.endpoints import citas
from app.core.config import settings
from app.models.models import Paciente, Medico, Cita

# Crear las tablas en la base de datos SQLite si no existen "citas.db"
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,   
    version=settings.APP_VERSION
)

# Configuración del middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # Permitir todos los orígenes. Cambiar a dominios específicos en producción.
    allow_credentials=True,
    allow_methods=settings.CORS_METHODS,  # Permitir todos los métodos HTTP
    allow_headers=settings.CORS_HEADERS  # Permitir todos los encabezados
)

# Registrar el router de citas
app.include_router(citas.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import APIRouter
from app.api.endpoints import appointments

api_router = APIRouter()

# Configuración unificada del router
api_router.include_router(
    appointments.router,
    prefix="/appointments",  # 👈 Prefijo único
    tags=["Appointments Management"]  # Mismo tag que en el endpoint
)
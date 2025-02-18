from fastapi import APIRouter
from app.api.v1.endpoints import appointments, upload_schedules, availability

api_router = APIRouter()

# Configuración unificada del router
api_router.include_router(
    appointments.router,
    prefix="/appointments",
    tags=["Appointments Management"]
)

api_router.include_router(
    upload_schedules.router,
    prefix="/upload-schedules",
    tags=["Upload Schedules"]
)

api_router.include_router(
    availability.router,
    prefix="/availability/check",
    tags=["Check available appointments"]
)
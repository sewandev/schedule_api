from fastapi import APIRouter
from app.api.v1.endpoints import appointments, availability, payments #, upload_schedules

api_router = APIRouter()

# Configuración unificada del router
api_router.include_router(
    availability.router,
    prefix="/availability/check",
    tags=["Check available appointments"]
)

api_router.include_router(
    payments.router,
    prefix="/payments",
    tags=["payments"]
)

"""
api_router.include_router(
    upload_schedules.router,
    prefix="/upload-schedules",
    tags=["Upload Schedules"]
)

api_router.include_router(
    appointments.router,
    prefix="/appointments",
    tags=["Appointments Management"]
)
"""
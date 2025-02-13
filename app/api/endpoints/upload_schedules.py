# api/endpoints/upload_schedules.py
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.upload_schedules import UploadSchedulesService

# Router para upload_schedules
router = APIRouter()

@router.post(
    "/",
    status_code=200,
    summary="Upload available schedules from an Excel file",
    responses={
        200: {"description": "Schedules uploaded successfully"},
        400: {"description": "Invalid file format or data"},
        500: {"description": "Internal server error"}
    }
)
async def upload_schedules(
    file: UploadFile = File(...),  # Recibe el archivo .xlsx
    db: AsyncSession = Depends(get_db)
):
    """
    ### Endpoint para cargar horarios disponibles desde un archivo Excel.

    **Returns:**
    - **200**: Horarios cargados correctamente.
    - **400**: Formato de archivo inválido o falta una columna.
    - **500**: Error interno del servidor.
    """

    # Leer el contenido del archivo
    contents = await file.read()
    
    # Llamar al servicio para procesar el archivo
    service = UploadSchedulesService(db)
    return await service.upload_schedules(contents, file.filename)
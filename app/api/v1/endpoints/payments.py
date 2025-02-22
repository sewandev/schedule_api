# app/api/v1/endpoints/payments.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.logging_config import get_logger
from app.schemas.appointments import PaymentCreate  # Solo necesitamos PaymentCreate aquí
from app.services.payments import PaymentService

router = APIRouter()
logger = get_logger(__name__)

@router.post(
    "/",
    response_model=dict,  # Respuesta es un dict con url y token
    status_code=status.HTTP_200_OK,
    summary="Initiate a payment for an appointment",
    responses={
        200: {"description": "Returns payment initiation URL and token"},
        400: {"description": "Invalid payment data provided"},
        500: {"description": "Internal server error"}
    }
)
async def initiate_payment(
    payment_data: PaymentCreate,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Inicia un pago para una cita médica con Transbank.

    Args:
        payment_data (PaymentCreate): Datos del pago validados por Pydantic (appointment_id, amount).
        db (AsyncSession): Sesión de base de datos inyectada.

    Returns:
        dict: URL y token para redirigir al usuario al formulario de pago de Transbank.
    """
    logger.debug(
        "Iniciando solicitud de pago con appointment_id=%s, amount=%s",
        payment_data.appointment_id, payment_data.amount
    )
    
    try:
        return_url = "http://localhost:8000/api/v1/payments/commit"
        logger.debug("URL de retorno configurada: %s", return_url)
        
        service = PaymentService(db)
        logger.debug("Instancia de PaymentService creada para procesar el pago")
        
        result = await service.initiate_payment(
            appointment_id=payment_data.appointment_id,
            amount=payment_data.amount,
            return_url=return_url
        )
        logger.debug(
            "Pago iniciado exitosamente, respuesta: url=%s, token=%s",
            result["url"], result["token"]
        )
        
        return result
    
    except HTTPException as he:
        logger.debug("Excepción HTTP capturada: %s", str(he))
        raise he
    except Exception as e:
        logger.critical("Error inesperado al iniciar el pago: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al iniciar el pago. Por favor, intenta de nuevo más tarde."
        )

@router.get(
    "/commit",
    response_model=dict,  # Respuesta es un dict con status y payment_id
    status_code=status.HTTP_200_OK,
    summary="Commit a payment after Transbank redirection",
    responses={
        200: {"description": "Returns payment confirmation status"},
        400: {"description": "Invalid token provided"},
        500: {"description": "Internal server error"}
    }
)
async def commit_payment(
    token: str,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Confirma un pago tras la redirección de Transbank.

    Args:
        token (str): Token de transacción recibido de Transbank.
        db (AsyncSession): Sesión de base de datos inyectada.

    Returns:
        dict: Estado de la confirmación del pago (completed o failed).
    """
    logger.debug("Iniciando confirmación de pago con token=%s", token)
    
    try:
        service = PaymentService(db)
        logger.debug("Instancia de PaymentService creada para confirmar el pago")
        
        result = await service.commit_payment(token=token)
        logger.debug(
            "Confirmación procesada, resultado: status=%s, payment_id=%s",
            result["status"], result["payment_id"]
        )
        
        return result
    
    except HTTPException as he:
        logger.debug("Excepción HTTP capturada: %s", str(he))
        raise he
    except Exception as e:
        logger.critical("Error inesperado al confirmar el pago: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al confirmar el pago. Por favor, intenta de nuevo más tarde."
        )
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.logging_config import get_logger
from app.core.config import settings
from app.schemas.appointments import PaymentCreate, PaymentInitResponse, PaymentCommitResponse
from app.services.payments import PaymentService

router = APIRouter()
logger = get_logger(__name__)

@router.post(
    "/init",
    response_model=PaymentInitResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Initiate a payment for an appointment"
)
async def initiate_payment(
    payment_data: PaymentCreate,
    db: AsyncSession = Depends(get_db)
) -> PaymentInitResponse:
    """Inicia un pago con Transbank y devuelve URL y token para redirigir al usuario."""
    logger.debug(
        "Iniciando pago para appointment_id=%s, amount=%s",
        payment_data.appointment_id, payment_data.amount
    )
    try:
        # Usar APP_HOST, PORT y API_PREFIX para construir la return_url
        return_url = f"http://{settings.PAYMENT_REDIRECT_HOST}:{settings.SERVER_BIND_PORT}{settings.API_PREFIX}/payments/commit"
        service = PaymentService(db)
        result = await service.initiate_payment(
            appointment_id=payment_data.appointment_id,
            amount=payment_data.amount,
            return_url=return_url
        )
        logger.info("Pago iniciado: url=%s, token=%s", result["url"], result["token"])
        return result
    except Exception as e:
        logger.critical("Error al iniciar el pago: %s", str(e))
        raise HTTPException(status_code=500, detail="Error al iniciar el pago")

@router.get(
    "/commit",
    response_model=PaymentCommitResponse,
    status_code=status.HTTP_200_OK,
    summary="Commit a payment after Transbank redirection"
)
async def commit_payment(
    token_ws: str,
    db: AsyncSession = Depends(get_db)
) -> PaymentCommitResponse:
    """Confirma el pago tras la redirección de Transbank y actualiza el estado."""
    logger.debug("Confirmando pago con token_ws=%s", token_ws)
    try:
        service = PaymentService(db)
        result = await service.commit_payment(token=token_ws)
        logger.info("Pago confirmado: status=%s, payment_id=%s", result["status"], result["payment_id"])
        return result
    except Exception as e:
        logger.critical("Error al confirmar el pago: %s", str(e))
        raise HTTPException(status_code=500, detail="Error al confirmar el pago")
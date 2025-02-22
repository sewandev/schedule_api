# app/services/payments.py
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from transbank.error.transbank_error import TransbankError
from app.core.config import settings
from app.repositories.payments import PaymentRepository
from app.models.models import Payment
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.logging_config import get_logger, setup_logging

# Configuración inicial de logging
setup_logging(log_level=settings.LOG_LEVEL, log_to_file=settings.LOG_TO_FILE)
logger = get_logger(__name__)

class PaymentService:
    def __init__(self, db: AsyncSession):
        self.payment_repo = PaymentRepository(db)
        self.transaction = Transaction(WebpayOptions(
            commerce_code=settings.transbank_commerce_code,
            api_key=settings.transbank_api_key,
            integration_type=settings.transbank_environment
        ))
        logger.debug("Instancia de PaymentService creada con PaymentRepository y Transbank Transaction inicializados")

    async def initiate_payment(self, appointment_id: int, amount: int, return_url: str) -> dict:
        """Inicia una transacción de pago con Transbank."""
        logger.debug(f"Iniciando transacción de pago para appointment_id: {appointment_id}, monto: {amount}, return_url: {return_url}")
        
        try:
            # Preparar datos iniciales del pago
            payment_data = {"appointment_id": appointment_id, "amount": amount}
            logger.debug(f"Datos preparados para crear pago: {payment_data}")
            
            # Crear el pago en la base de datos
            payment = await self.payment_repo.create_payment(payment_data)
            logger.debug(f"Pago creado en la base de datos con ID: {payment.id}")
            
            # Generar identificadores para Transbank
            buy_order = f"appointment_{payment.id}"
            session_id = f"session_{payment.id}"
            logger.debug(f"Identificadores generados - buy_order: {buy_order}, session_id: {session_id}")
            
            # Iniciar transacción con Transbank
            logger.debug("Enviando solicitud de creación de transacción a Transbank")
            response = self.transaction.create(
                buy_order=buy_order,
                session_id=session_id,
                amount=amount,
                return_url=return_url
            )
            logger.debug(f"Respuesta de Transbank recibida: {response}")
            
            # Verificar que la respuesta sea un dict y tenga las claves esperadas
            if not isinstance(response, dict) or "url" not in response or "token" not in response:
                logger.error(f"Respuesta de Transbank inválida: {response}")
                raise ValueError("Respuesta de Transbank no contiene 'url' o 'token'")
            
            # Actualizar el pago con el token de Transbank
            update_data = {"transbank_token": response["token"]}
            logger.debug(f"Actualizando pago con token: {update_data}")
            updated_payment = await self.payment_repo.update_payment(payment.id, update_data)
            if not updated_payment:
                logger.error(f"No se pudo actualizar el pago con ID: {payment.id}")
                raise ValueError(f"No se encontró el pago con ID: {payment.id} para actualizar")
            logger.debug(f"Pago actualizado con token en la base de datos: {updated_payment.id}")
            
            # Log de éxito
            logger.info(f"Transacción iniciada para pago ID: {payment.id}, Token: {response['token']}")
            return {"url": response["url"], "token": response["token"]}
        
        except TransbankError as e:
            logger.error(f"Error al iniciar transacción con Transbank: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado al iniciar transacción: {str(e)}")
            raise

    async def commit_payment(self, token: str) -> dict:
        """Confirma una transacción de pago con Transbank."""
        logger.debug(f"Iniciando confirmación de pago con token: {token}")
        
        try:
            # Confirmar transacción con Transbank
            logger.debug("Enviando solicitud de commit a Transbank")
            response = self.transaction.commit(token=token)
            logger.debug(f"Respuesta de commit recibida: {response}")
            
            # Verificar que la respuesta sea un dict y tenga las claves esperadas
            if not isinstance(response, dict) or "response_code" not in response:
                logger.error(f"Respuesta de commit inválida: {response}")
                raise ValueError("Respuesta de commit de Transbank no contiene 'response_code'")
            
            # Buscar el pago asociado al token
            logger.debug(f"Consultando pago en la base de datos con transbank_token: {token}")
            result = await self.payment_repo.db.execute(
                select(Payment).filter(Payment.transbank_token == token)
            )
            payment = result.scalar_one_or_none()
            logger.debug(f"Resultado de la consulta: payment_id={payment.id if payment else None}")
            
            if payment and response["response_code"] == 0:  # Transacción exitosa
                logger.debug(f"Pago encontrado y transacción exitosa, actualizando estado a 'completed'")
                update_data = {"status": "completed"}
                updated_payment = await self.payment_repo.update_payment(payment.id, update_data)
                if not updated_payment:
                    logger.error(f"No se pudo actualizar el pago con ID: {payment.id} a 'completed'")
                    raise ValueError(f"No se encontró el pago con ID: {payment.id} para actualizar")
                logger.info(f"Pago confirmado para ID: {payment.id}")
                return {"status": "completed", "payment_id": payment.id}
            else:
                logger.debug(f"Pago no encontrado o transacción fallida, actualizando estado a 'failed'")
                update_data = {"status": "failed"}
                if payment:
                    updated_payment = await self.payment_repo.update_payment(payment.id, update_data)
                    if not updated_payment:
                        logger.error(f"No se pudo actualizar el pago con ID: {payment.id} a 'failed'")
                        raise ValueError(f"No se encontró el pago con ID: {payment.id} para actualizar")
                logger.warning(f"Fallo en confirmación de pago para token: {token}")
                return {"status": "failed", "payment_id": payment.id if payment else None}
        
        except TransbankError as e:
            logger.error(f"Error al confirmar transacción con Transbank: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado al confirmar transacción: {str(e)}")
            raise
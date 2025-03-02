from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from transbank.error.transbank_error import TransbankError
from src.core.config import settings
from src.repositories.payments import PaymentRepository
from src.models.models import Payment
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.core.logging_config import get_logger, setup_logging

# Configuración inicial de logging
setup_logging(log_level=settings.LOG_LEVEL, log_to_file=settings.LOG_TO_FILE)
logger = get_logger(__name__)

class PaymentService:
    def __init__(self, db: AsyncSession):
        self.payment_repo = PaymentRepository(db)
        self.transaction = Transaction(WebpayOptions(
            commerce_code=settings.transbank_commerce_code,  # Minúsculas para coincidir con config.py
            api_key=settings.transbank_api_key,              # Minúsculas
            integration_type=settings.transbank_environment  # Minúsculas
        ))
        logger.debug("Instancia de PaymentService creada con PaymentRepository y Transbank Transaction inicializados")

    async def initiate_payment(self, appointment_id: int, amount: int, return_url: str) -> dict:
        """Inicia una transacción de pago con Transbank y devuelve URL y token."""
        logger.debug(f"Iniciando transacción para appointment_id: {appointment_id}, monto: {amount}, return_url: {return_url}")

        try:
            # Crear el pago inicial en la base de datos con estado 'pending'
            payment_data = {"appointment_id": appointment_id, "amount": amount, "status": "pending"}
            payment = await self.payment_repo.create_payment(payment_data)
            logger.debug(f"Pago creado en la base de datos con ID: {payment.id}")

            # Generar identificadores únicos para Transbank
            buy_order = f"appt_{payment.id}"
            session_id = f"session_{payment.id}"
            logger.debug(f"Identificadores generados - buy_order: {buy_order}, session_id: {session_id}")

            # Iniciar la transacción con Transbank
            logger.debug("Enviando solicitud de creación de transacción a Transbank")
            response = self.transaction.create(
                buy_order=buy_order,
                session_id=session_id,
                amount=amount,
                return_url=return_url
            )
            logger.debug(f"Respuesta de Transbank recibida: {response}")

            # Validar la respuesta de Transbank
            if not isinstance(response, dict) or "url" not in response or "token" not in response:
                logger.error(f"Respuesta de Transbank inválida: {response}")
                raise ValueError("Respuesta de Transbank no contiene 'url' o 'token'")

            # Actualizar el pago con el token de Transbank
            update_data = {"transbank_token": response["token"]}
            updated_payment = await self.payment_repo.update_payment(payment.id, update_data)
            if not updated_payment:
                logger.error(f"No se pudo actualizar el pago con ID: {payment.id}")
                raise ValueError(f"No se encontró el pago con ID: {payment.id} para actualizar")
            logger.debug(f"Pago actualizado con token: {response['token']}")

            logger.info(f"Transacción iniciada para pago ID: {payment.id}, token: {response['token']}")
            return {"url": response["url"], "token": response["token"]}

        except TransbankError as e:
            logger.error(f"Error de Transbank al iniciar transacción: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado al iniciar transacción: {str(e)}")
            raise

    async def commit_payment(self, token: str) -> dict:
        """Confirma una transacción de pago con Transbank y actualiza el estado."""
        logger.debug(f"Iniciando confirmación de pago con token: {token}")

        try:
            # Buscar el pago en la base de datos por el token
            logger.debug(f"Consultando pago con transbank_token: {token}")
            result = await self.payment_repo.db.execute(
                select(Payment).filter(Payment.transbank_token == token)
            )
            payment = result.scalar_one_or_none()
            if not payment:
                logger.error(f"No se encontró pago con token: {token}")
                raise ValueError("No se encontró el pago asociado al token")

            # Confirmar la transacción con Transbank
            logger.debug("Enviando solicitud de commit a Transbank")
            response = self.transaction.commit(token=token)
            logger.debug(f"Respuesta de commit recibida: {response}")

            # Validar la respuesta de Transbank
            if not isinstance(response, dict) or "response_code" not in response:
                logger.error(f"Respuesta de commit inválida: {response}")
                raise ValueError("Respuesta de commit de Transbank no contiene 'response_code'")

            # Actualizar el estado del pago según el resultado
            new_status = "approved" if response["response_code"] == 0 else "rejected"
            update_data = {"status": new_status}
            updated_payment = await self.payment_repo.update_payment(payment.id, update_data)
            if not updated_payment:
                logger.error(f"No se pudo actualizar el pago con ID: {payment.id}")
                raise ValueError(f"No se encontró el pago con ID: {payment.id} para actualizar")

            logger.info(f"Pago ID: {payment.id} confirmado con estado: {new_status}")
            return {"status": new_status, "payment_id": payment.id}

        except TransbankError as e:
            logger.error(f"Error de Transbank al confirmar transacción: {str(e)}")
            if 'payment' in locals():
                await self.payment_repo.update_payment(payment.id, {"status": "rejected"})
            raise
        except Exception as e:
            logger.error(f"Error inesperado al confirmar transacción: {str(e)}")
            raise
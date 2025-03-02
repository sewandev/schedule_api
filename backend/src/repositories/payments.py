from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.models import Payment
from src.core.logging_config import get_logger, setup_logging
from src.core.config import settings

# Configuración inicial de logging (global para el módulo)
setup_logging(log_level=settings.LOG_LEVEL, log_to_file=settings.LOG_TO_FILE)
logger = get_logger(__name__)

class PaymentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        logger.debug("Instancia de PaymentRepository creada con nueva sesión de base de datos")

    async def create_payment(self, payment_data: dict) -> Payment:
        """Crea un registro de pago en la base de datos."""
        logger.debug(f"Iniciando creación de pago con datos: {payment_data}")
        
        # Crear instancia del modelo Payment
        payment = Payment(**payment_data)
        logger.debug(f"Objeto Payment creado con ID temporal: {payment.id}, datos: {payment_data}")
        
        # Agregar a la sesión
        self.db.add(payment)
        logger.debug("Pago añadido a la sesión de la base de datos, esperando commit")
        
        # Confirmar transacción
        await self.db.commit()
        logger.debug(f"Commit ejecutado para el pago, ID asignado: {payment.id}")
        
        # Refrescar instancia para obtener datos actualizados
        await self.db.refresh(payment)
        logger.debug(f"Pago refrescado desde la base de datos: {payment.id}, estado: {payment.status}")
        
        # Log de éxito a nivel info
        logger.info(f"Pago creado exitosamente con ID: {payment.id}")
        return payment

    async def update_payment(self, payment_id: int, update_data: dict) -> Payment | None:
        """Actualiza un pago existente."""
        logger.debug(f"Iniciando actualización de pago con ID: {payment_id}, datos: {update_data}")
        
        # Consultar el pago existente
        logger.debug(f"Ejecutando consulta SELECT para payment_id: {payment_id}")
        result = await self.db.execute(select(Payment).filter(Payment.id == payment_id))
        payment = result.scalar_one_or_none()
        
        if payment:
            logger.debug(f"Pago encontrado con ID: {payment_id}, datos actuales: {payment.__dict__}")
            
            # Actualizar atributos dinámicamente
            for key, value in update_data.items():
                logger.debug(f"Actualizando atributo '{key}' con valor: {value}")
                setattr(payment, key, value)
            
            logger.debug(f"Atributos actualizados en el objeto Payment: {payment.__dict__}")
            
            # Confirmar cambios
            await self.db.commit()
            logger.debug(f"Commit ejecutado para el pago con ID: {payment_id}")
            
            # Refrescar instancia
            await self.db.refresh(payment)
            logger.debug(f"Pago refrescado tras actualización: {payment.__dict__}")
            
            # Log de éxito a nivel info
            logger.info(f"Pago actualizado exitosamente con ID: {payment.id}")
            return payment
        else:
            logger.warning(f"No se encontró pago con ID: {payment_id} para actualizar")
            return None
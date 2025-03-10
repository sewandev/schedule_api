from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.core.logging_config import setup_logging, get_logger
from sqlalchemy.sql import text
from src.core.config import settings
from src.models.database_models import Base
from typing import AsyncGenerator
from fastapi import HTTPException

setup_logging(log_level=settings.LOG_LEVEL, log_to_file=settings.LOG_TO_FILE)
logger = get_logger(__name__)

try:
    logger.debug("Inicializando motor de base de datos con URL: %s", settings.DATABASE_URL)
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DB_ECHO,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_pre_ping=True,
        pool_recycle=3600,
        pool_timeout=30
    )
    logger.info("Motor de base de datos inicializado correctamente.")
except Exception as e:
    logger.critical("Error al inicializar el motor de base de datos: %s", str(e), exc_info=True)
    raise

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = AsyncSessionLocal()
    try:
        logger.debug("Iniciando nueva sesión de base de datos: %s", id(session))
        await session.execute(text("SELECT 1"))
        logger.debug("Conexión a la base de datos confirmada en la sesión: %s", id(session))
        yield session
    except HTTPException as e:
        logger.debug("Excepción HTTP controlada en la sesión: %s", str(e))
        await session.rollback()
        raise
    except Exception as e:
        logger.error("Error en la sesión de base de datos: %s", str(e), exc_info=True)
        await session.rollback()
        raise
    finally:
        await session.close()
        logger.debug("Sesión cerrada correctamente: %s", id(session))

async def test_connection() -> None:
    async with AsyncSessionLocal() as session:
        try:
            await session.execute(text("SELECT 1"))
            logger.info("Prueba de conexión a la base de datos exitosa.")
        except Exception as e:
            logger.critical("Fallo en la prueba de conexión: %s", str(e), exc_info=True)
            raise
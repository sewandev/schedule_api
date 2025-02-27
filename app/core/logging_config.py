import logging
import logging.handlers
from pathlib import Path
from app.core.config import settings

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)


def setup_logging(log_level: str = "INFO", log_to_file: bool = True) -> None:
    """
    Configura el sistema de logging global para la aplicación.

    Args:
        log_level (str): Nivel de logging (e.g., "DEBUG", "INFO", "ERROR").
        log_to_file (bool): Si True, escribe logs en un archivo; si False, solo en consola.
    """
    log_level = log_level.upper()
    numeric_level = getattr(logging, log_level, logging.INFO)

    logger = logging.getLogger()
    logger.setLevel(numeric_level)

    log_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    logger.handlers.clear()

    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    if log_to_file:
        log_file = LOG_DIR / settings.LOG_FILE_NAME
        file_handler = logging.handlers.RotatingFileHandler(
            filename = log_file,
            maxBytes = 5 * 1024 * 1024,
            backupCount = 5,
            encoding = settings.LOG_FILE_ENCODING
        )

        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(log_formatter)
        logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger configurado para un módulo específico.

    Args:
        name (str): Nombre del módulo que solicita el logger (e.g., __name__).

    Returns:
        logging.Logger: Instancia del logger configurada.
    """
    return logging.getLogger(name)

setup_logging(log_level="INFO", log_to_file=True)

if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.debug("Este es un mensaje de debug")
    logger.info("Aplicación iniciada correctamente")
    logger.warning("Advertencia: algo podría estar mal")
    logger.error("Error crítico detectado")
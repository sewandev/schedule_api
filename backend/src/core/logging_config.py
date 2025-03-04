import logging
import logging.handlers
from pathlib import Path
from typing import Literal
from src.core.config import settings

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

def setup_logging(
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO",
    log_to_file: bool = True
) -> None:
    try:
        log_level_upper = log_level.upper()
        numeric_level = getattr(logging, log_level_upper, logging.INFO)

        logger = logging.getLogger("schedule_api")
        logger.setLevel(numeric_level)
        logger.handlers.clear()

        log_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        console_handler = logging.StreamHandler()
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(log_formatter)
        logger.addHandler(console_handler)

        if log_to_file:
            log_file = LOG_DIR / settings.LOG_FILE_NAME
            file_handler = logging.handlers.RotatingFileHandler(
                filename=log_file,
                maxBytes=settings.LOG_MAX_BYTES,
                backupCount=settings.LOG_BACKUP_COUNT,
                encoding=settings.LOG_FILE_ENCODING
            )
            file_handler.setLevel(numeric_level)
            file_handler.setFormatter(log_formatter)
            logger.addHandler(file_handler)

    except PermissionError as e:
        print(f"Error de permisos al configurar logging: {e}")
        raise
    except Exception as e:
        print(f"Error inesperado al configurar logging: {e}")
        raise

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"schedule_api.{name}")
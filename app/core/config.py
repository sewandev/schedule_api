from pydantic_settings import BaseSettings
from pydantic import RedisDsn, field_validator
from typing import Optional

class Settings(BaseSettings):
    # Configuración general de la aplicación
    ENVIRONMENT: str = "development"
    APP_TITLE: str = "Medical Appointments API"
    APP_DESCRIPTION: str = "API for managing medical appointments and schedules"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # Configuración CORS
    CORS_ORIGINS: list[str] = ["*"]
    CORS_METHODS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]
    CORS_EXPOSE_HEADERS: list[str] = ["Content-Disposition"]
    
    # Configuración de base de datos (Async SQLAlchemy)
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/reserva_hora_api"
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    TEST_DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/reserva_hora_api-test"
    TESTING: bool = False
    
    # Configuración de autenticación JWT
    JWT_SECRET_KEY: str = "super-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuración de logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    LOG_FILE: Optional[str] = "app.log"
    
    # Configuración de Redis (opcional para cache/eventos)
    REDIS_URL: Optional[RedisDsn] = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Instancia singleton de configuración
settings = Settings()
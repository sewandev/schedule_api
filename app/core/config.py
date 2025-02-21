from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    # Configuración general de la aplicación
    ENVIRONMENT: str = "development"
    APP_TITLE: str = "Medical Appointments API"
    APP_DESCRIPTION: str = "API for managing medical appointments and schedules"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Configuración CORS
    CORS_ORIGINS: list[str] = ["*"]
    CORS_METHODS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]
    CORS_EXPOSE_HEADERS: list[str] = ["Content-Disposition"]
    
    # Configuración de base de datos
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    
    @property
    def DATABASE_URL(self) -> str:
        """Construye la URL de la base de datos dinámicamente, agregando sslmode=require en Vercel."""
        ssl_mode = "?sslmode=require" if os.getenv("VERCEL") else ""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}{ssl_mode}"
        )

    model_config = SettingsConfigDict(
        env_file=".env" if ENVIRONMENT == "development" else None,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

settings = Settings()
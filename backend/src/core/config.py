from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    # Configuración general de la aplicación
    ENVIRONMENT: str = "development"
    APP_TITLE: str = "API Citas Médicas"
    APP_DESCRIPTION: str = "API que administra citas médicas según disponibilidad de horas integrada con Transbank."
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8005
    PAYMENT_REDIRECT_HOST: str = "localhost"  # URLs externas para redirección de pagos

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

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_TO_FILE: bool = True
    LOG_FILE_NAME: str = "reserva_hora_api.log"
    LOG_FILE_ENCODING: str = "utf-8"

    # Configuración de Transbank TEST
    transbank_commerce_code: str = "597055555532"
    transbank_api_key: str = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"
    transbank_environment: str = "TEST"
    
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(
        env_file=".env" if ENVIRONMENT == "development" else None,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

settings = Settings()
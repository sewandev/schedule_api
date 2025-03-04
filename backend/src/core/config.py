from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, computed_field

class Settings(BaseSettings):
    # Configuración general de la aplicación
    APP_ENVIRONMENT: str = Field(default="development")
    APP_TITLE: str = Field(default="API Citas Médicas")
    APP_DESCRIPTION: str = Field(default="API que administra citas médicas según disponibilidad de horas integrada con Transbank.")
    APP_VERSION: str = Field(default="1.0.0")
    APP_API_PREFIX: str = Field(default="/api/v1")
    APP_HOST: str = Field(default="0.0.0.0")
    APP_PORT: int = Field(default=8005)
    APP_PAYMENT_REDIRECT_HOST: str = Field(default="localhost")

    # Configuración CORS
    CORS_ORIGINS: list[str] = Field(default=["*"])
    CORS_METHODS: list[str] = Field(default=["*"])
    CORS_HEADERS: list[str] = Field(default=["*"])
    CORS_EXPOSE_HEADERS: list[str] = Field(default=["Content-Disposition"])
    
    # Configuración de base de datos
    DB_POSTGRES_USER: str
    DB_POSTGRES_PASSWORD: str
    DB_POSTGRES_HOST: str
    DB_POSTGRES_PORT: int
    DB_POSTGRES_DB: str
    DB_ECHO: bool = Field(default=False)
    DB_POOL_SIZE: int = Field(default=5)
    DB_MAX_OVERFLOW: int = Field(default=10)

    # Logging
    LOG_LEVEL: str = Field(default="INFO")
    LOG_TO_FILE: bool = Field(default=True)
    LOG_FILE_NAME: str = Field(default="reserva_hora_api.log")
    LOG_FILE_ENCODING: str = Field(default="utf-8")

    # Configuración de Transbank
    TBK_COMMERCE_CODE: str
    TBK_API_KEY: str
    TBK_ENVIRONMENT: str = Field(default="TEST")
    
    @computed_field(return_type=str)
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_POSTGRES_USER}:{self.DB_POSTGRES_PASSWORD}@"
            f"{self.DB_POSTGRES_HOST}:{self.DB_POSTGRES_PORT}/{self.DB_POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

settings = Settings()
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Configuración general
    ENVIRONMENT: str = "dev"
    APP_TITLE: str = "Citas Médicas API"
    APP_DESCRIPTION: str = "API para gestionar citas médicas"
    APP_VERSION: str = "1.0.0"
    CORS_ORIGINS: list = ["*"]
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]
    
    # Configuración de la base de datos
    DATABASE_URL: str = "sqlite:///appointments.db"
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    
    # Configuración de autenticación
    JWT_SECRET_KEY: str = "supersecretkey"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuración de logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: str = "app.log"
    
    # Configuración de testing
    TEST_DATABASE_URL: str = "sqlite:///test_appointments.db"
    TESTING: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Instancia de configuración
settings = Settings()
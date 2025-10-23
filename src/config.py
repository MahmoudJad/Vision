from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # Database configuration for Docker
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql+asyncpg://db_user:db_password@dev_db:5432/dev_db"
    )
    TEST_DATABASE_URL: str = os.getenv(
        "TEST_DATABASE_URL",
        "postgresql+asyncpg://db_user:db_password@test_db:5432/test_db"
    )
    
    # Application configuration
    APP_NAME: str = "vision"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    class Config:
        env_file = ".env"

settings = Settings()

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./inventory_dev.db"
    )
    
    # API
    API_TITLE: str = "Inventory Management System"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Production-ready Inventory & Order Management System"
    
    # CORS
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://frontend:3000",
        "https://peaceful-heliotrope-f711a7.netlify.app"
    ]
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT == "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

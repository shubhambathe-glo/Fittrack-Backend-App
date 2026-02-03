# ==================== Config Settings ====================
# File: app/core/config.py

import os
from typing import Optional

# Handle both Pydantic v1 and v2
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Application settings and configuration
    """
    # App Info
    APP_NAME: str = "Fitness Tracking App"
    APP_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Server Configuration
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "8000"))
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-change-me")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Database - SQLite
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./fitness_tracking.db"
    )
    
    # Azure (for future use)
    AZURE_STORAGE_CONNECTION_STRING: Optional[str] = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    AZURE_STORAGE_CONTAINER_NAME: str = "workout-media"
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",  # React dev server
        "http://localhost:4200",  # Angular dev server
        "http://localhost:5173",  # Vite dev server
        "https://yourdomain.com"
    ]
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_FILE_TYPES: list = ["image/jpeg", "image/png", "video/mp4"]
    
    # Email (for notifications - future)
    SMTP_HOST: Optional[str] = os.getenv("SMTP_HOST")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: Optional[str] = os.getenv("SMTP_USER")
    SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    class Config:
        case_sensitive = True
        env_file = ".env"
    
    # Computed properties
    @property
    def server_url(self) -> str:
        """
        Get full server base URL for APIs
        """
        protocol = "https" if self.ENVIRONMENT == "production" else "http"
        
        # Use SERVER_BASE_URL if explicitly set (for production/custom domains)
        base_url = os.getenv("SERVER_BASE_URL")
        if base_url:
            return base_url.rstrip("/")
        
        # For development, construct from host and port
        if self.SERVER_HOST in ["0.0.0.0", "127.0.0.1"]:
            host = "localhost"
        else:
            host = self.SERVER_HOST
        
        # Don't include port 80 (http) or 443 (https) in URL
        if (protocol == "http" and self.SERVER_PORT == 80) or \
           (protocol == "https" and self.SERVER_PORT == 443):
            return f"{protocol}://{host}"
        
        return f"{protocol}://{host}:{self.SERVER_PORT}"
    
    @property
    def api_base_url(self) -> str:
        """
        Get full API base URL including version prefix
        """
        return f"{self.server_url}{self.API_V1_PREFIX}"


# Create global settings instance
settings = Settings()


# ==================== Environment-based Configuration ====================

def get_database_url() -> str:
    """
    Get database URL based on environment
    """
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        return os.getenv("DATABASE_URL_PROD", "sqlite:///./fitness_tracking_prod.db")
    elif env == "staging":
        return os.getenv("DATABASE_URL_STAGING", "sqlite:///./fitness_tracking_staging.db")
    else:
        return os.getenv("DATABASE_URL_DEV", "sqlite:///./fitness_tracking.db")


def is_production() -> bool:
    """
    Check if running in production environment
    """
    return os.getenv("ENVIRONMENT", "development").lower() == "production"


def is_development() -> bool:
    """
    Check if running in development environment
    """
    return os.getenv("ENVIRONMENT", "development").lower() == "development"


def is_staging() -> bool:
    """
    Check if running in staging environment
    """
    return os.getenv("ENVIRONMENT", "development").lower() == "staging"

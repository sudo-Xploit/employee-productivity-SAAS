import secrets
import os
from typing import Any, Dict, List, Optional, Set, Union

from pydantic import AnyHttpUrl, EmailStr, field_validator, HttpUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)
    
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    
    # Token settings
    # 60 minutes * 24 hours = 1 day
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    # 30 days
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # Server settings
    SERVER_NAME: str = "Employee Productivity API"
    SERVER_HOST: AnyHttpUrl = "http://localhost"
    
    # CORS settings
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: ["http://localhost", "http://localhost:4200", "http://localhost:3000"]
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    # Rate limiting settings
    RATE_LIMIT_PER_MINUTE: int = 60  # 60 requests per minute
    RATE_LIMIT_PER_HOUR: int = 1000  # 1000 requests per hour

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "Employee Productivity SAAS"
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800  # 30 minutes
    DB_ECHO: bool = False  # Set to True for development to log SQL queries
    
    # Production database URL override
    @field_validator("DATABASE_URL", mode="before")
    def assemble_db_connection(cls, v: Optional[str]) -> str:
        if os.environ.get("DATABASE_URL"):
            return os.environ.get("DATABASE_URL")
        return v
    
    # Users
    FIRST_SUPERUSER: EmailStr = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin"
    USERS_OPEN_REGISTRATION: bool = False
    
    # Security settings
    ENCRYPTION_KEY: str = secrets.token_urlsafe(32)  # For encrypting sensitive fields
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 24
    EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS: int = 48
    
    # HTTPS settings
    USE_HTTPS: bool = False  # Set to True in production
    SSL_KEYFILE: str = ""
    SSL_CERTFILE: str = ""
    
    # ML model settings
    MODEL_RETRAIN_DAYS: int = 7  # Retrain models every 7 days
    
    # Logging settings
    LOG_LEVEL: str = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    JSON_LOGS: bool = True  # Use JSON format for logs in production
    
    # Metrics settings
    ENABLE_METRICS: bool = True  # Enable Prometheus metrics
    
    # Health check settings
    HEALTH_CHECK_INCLUDE_DB: bool = True  # Include database check in health endpoint


settings = Settings()
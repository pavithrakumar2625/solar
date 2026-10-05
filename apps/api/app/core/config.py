"""
SolarRecover AI — Application Configuration
Loads settings from environment variables with validated defaults.
"""
from pydantic import model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "SolarRecover AI"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_VERSION: str = "0.1.0"
    APP_SECRET_KEY: str = "CHANGE_ME_TO_A_RANDOM_64_CHAR_STRING"

    # Server
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_WORKERS: int = 1
    API_CORS_ORIGINS: str = "http://localhost:3000"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://solarrecover:solarrecover@localhost:5432/solarrecover"
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10

    # Redis (optional)
    REDIS_URL: str | None = None

    # JWT Authentication
    JWT_SECRET_KEY: str = "CHANGE_ME_TO_A_RANDOM_64_CHAR_STRING"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # AI / LLM
    AI_PROVIDER: str = "gemini"
    GEMINI_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None
    AI_MODEL: str = "gemini-2.0-flash"
    AI_MAX_TOKENS: int = 4096
    AI_TEMPERATURE: float = 0.3

    # Weather
    WEATHER_PROVIDER: str = "open_meteo"
    OPENWEATHERMAP_API_KEY: str | None = None

    # File Storage
    STORAGE_PROVIDER: str = "local"
    STORAGE_LOCAL_PATH: str = "./storage"
    S3_BUCKET: str | None = None
    S3_REGION: str | None = None
    S3_ACCESS_KEY: str | None = None
    S3_SECRET_KEY: str | None = None

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    # ML
    ML_MODELS_PATH: str = "./ml/models/artifacts"
    ML_DATA_PATH: str = "./ml/data"

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.API_CORS_ORIGINS.split(",")]

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == "development"

    @model_validator(mode="after")
    def validate_production_settings(self) -> "Settings":
        """Prevent obvious insecure production boot settings."""
        placeholder = "CHANGE_ME_TO_A_RANDOM_64_CHAR_STRING"
        if self.is_production:
            if placeholder == self.APP_SECRET_KEY or placeholder == self.JWT_SECRET_KEY:
                raise ValueError("Production secrets must be configured with non-placeholder values.")
            if self.APP_DEBUG:
                raise ValueError("APP_DEBUG must be false in production.")
        return self

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


settings = Settings()

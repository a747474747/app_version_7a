"""
Configuration settings for Four-Engine System Architecture.

This module provides Pydantic-based configuration management for all
environment variables and application settings.
"""

import os
from typing import Optional, List
from pydantic import validator, Field
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""

    # PostgreSQL connection
    host: str = "localhost"
    port: int = 5432
    name: str = "four_engine_db"
    user: str = "postgres"
    password: str = ""

    # SQLAlchemy settings
    pool_size: int = 10
    max_overflow: int = 20
    pool_timeout: int = 30
    echo: bool = False  # Set to True for SQL debugging

    @property
    def url(self) -> str:
        """Generate database URL."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    class Config:
        env_prefix = "DB_"


class ClerkSettings(BaseSettings):
    """Clerk authentication settings."""

    secret_key: Optional[str] = None
    publishable_key: Optional[str] = None

    def __init__(self, **data):
        super().__init__(**data)
        # If publishable_key is not set, try NEXT_PUBLIC version
        if not self.publishable_key:
            import os
            self.publishable_key = os.getenv('NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY')

    class Config:
        env_prefix = "CLERK_"


class LLMSettings(BaseSettings):
    """LLM and AI service settings."""

    # OpenRouter configuration
    openrouter_api_key: Optional[str] = None
    openrouter_base_url: str = "https://openrouter.ai/api/v1"

    # Model configurations
    default_model: str = "anthropic/claude-3-haiku"
    embedding_model: str = "text-embedding-ada-002"

    # Alternative models for different use cases
    calculation_model: str = "anthropic/claude-3-haiku"  # For deterministic math validation
    reasoning_model: str = "anthropic/claude-3-sonnet"   # For complex reasoning
    creative_model: str = "anthropic/claude-3-haiku"     # For narrative generation

    # Performance limits
    max_tokens: int = 4096
    temperature: float = 0.1  # Low temperature for factual responses

    # Rate limiting
    requests_per_minute: int = 50
    requests_per_hour: int = 1000

    # Cost tracking
    enable_cost_tracking: bool = True
    cost_tracking_currency: str = "USD"

    class Config:
        env_prefix = "LLM_"


class EngineSettings(BaseSettings):
    """Four-engine performance and configuration settings."""

    # Calculation Engine
    calc_timeout_seconds: int = 30
    calc_cache_ttl_seconds: int = 3600  # 1 hour

    # Strategy Engine
    strategy_timeout_seconds: int = 300  # 5 minutes
    strategy_max_iterations: int = 1000

    # Advice Engine
    advice_timeout_seconds: int = 60

    # LLM Orchestrator
    llm_timeout_seconds: int = 120
    llm_max_retries: int = 3

    class Config:
        env_prefix = "ENGINE_"


class APISettings(BaseSettings):
    """API and web service settings."""

    # FastAPI settings
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    reload: bool = False

    # CORS settings
    cors_origins: List[str] = ["http://localhost:3000", "https://localhost:3000"]

    # Rate limiting
    rate_limit_requests: int = 100
    rate_limit_window_seconds: int = 60

    class Config:
        env_prefix = "API_"


class SecuritySettings(BaseSettings):
    """Security and encryption settings."""

    # JWT and session settings
    jwt_secret_key: str = "change-this-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24

    # Encryption
    encryption_key: Optional[str] = None

    class Config:
        env_prefix = "SEC_"


class AppSettings(BaseSettings):
    """Main application settings combining all components."""

    # Application metadata
    name: str = "Four-Engine System Architecture"
    version: str = "1.0.0"
    description: str = "Financial advice system with four computational engines"

    # Environment
    environment: str = "development"  # development, staging, production

    # Component settings
    database: DatabaseSettings = DatabaseSettings()
    clerk: Optional[ClerkSettings] = ClerkSettings()
    llm: Optional[LLMSettings] = None
    engines: EngineSettings = EngineSettings()
    api: APISettings = APISettings()
    security: SecuritySettings = SecuritySettings()

    # Feature flags
    enable_caching: bool = True
    enable_metrics: bool = True
    enable_tracing: bool = True

    @validator("environment")
    def validate_environment(cls, v):
        valid_envs = ["development", "staging", "production"]
        if v not in valid_envs:
            raise ValueError(f"Environment must be one of: {valid_envs}")
        return v

    class Config:
        env_file = [".env", "../.env.local"]
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra env vars that belong to nested models


# Global settings instance
settings = AppSettings()


def get_settings() -> AppSettings:
    """Get application settings instance."""
    return settings


def is_development() -> bool:
    """Check if running in development environment."""
    return settings.environment == "development"


def is_production() -> bool:
    """Check if running in production environment."""
    return settings.environment == "production"


# Database setup for development
_engine = create_engine(
    "sqlite:///./dev_database.db",  # Simple SQLite database for development
    connect_args={"check_same_thread": False},
    echo=settings.database.echo,
)

_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


def get_db() -> Session:
    """Get database session for dependency injection."""
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()

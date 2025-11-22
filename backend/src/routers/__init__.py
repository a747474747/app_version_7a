"""
FastAPI routers for Four-Engine System Architecture.

This package provides route handlers organized by functionality:
health checks, API endpoints, and domain-specific routes.
"""

from .health import router as health_router
from .api import router as api_router

__all__ = ["health_router", "api_router"]

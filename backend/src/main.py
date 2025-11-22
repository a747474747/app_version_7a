"""
Main FastAPI application for Four-Engine System Architecture.

This module initializes the FastAPI application with routing structure,
middleware, and core configuration for the financial advice system.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from .auth import ClerkAuthMiddleware, CORSMiddleware
from .middleware import (
    RequestValidationMiddleware,
    ErrorHandlingMiddleware,
    LoggingMiddleware,
    SecurityHeadersMiddleware
)
from .routers import health_router, api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    # Startup
    print("🚀 Starting Four-Engine System Architecture")

    yield

    # Shutdown
    print("🛑 Shutting down Four-Engine System Architecture")


# Create FastAPI application
app = FastAPI(
    title="Four-Engine System Architecture",
    description="Financial advice system with four computational engines",
    version="1.0.0",
    lifespan=lifespan,
)

# Add middleware (order matters - middleware is applied in reverse order)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(RequestValidationMiddleware)
app.add_middleware(
    ClerkAuthMiddleware,
    exclude_paths=["/health", "/docs", "/openapi.json", "/redoc"]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://localhost:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router, prefix="", tags=["health"])
app.include_router(api_router, prefix="/api/v1", tags=["api"])


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "type": "server_error"
        }
    )


if __name__ == "__main__":
    # Development server
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )

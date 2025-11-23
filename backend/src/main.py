"""
Main FastAPI application for Four-Engine System Architecture.

This module initializes the FastAPI application with routing structure,
middleware, and core configuration for the financial advice system.
"""

import os
from contextlib import asynccontextmanager

# Load environment variables from project root
try:
    from dotenv import load_dotenv
    from pathlib import Path
    # Get project root (parent of backend directory)
    backend_dir = Path(__file__).parent.parent  # backend/src -> backend
    project_root = backend_dir.parent  # backend -> project root
    # Load .env.local first (higher priority), then .env
    env_local = project_root / '.env.local'
    env_file = project_root / '.env'
    if env_local.exists():
        load_dotenv(env_local, override=True)
        print(f"Loaded environment from: {env_local}")
    if env_file.exists():
        load_dotenv(env_file, override=False)  # Don't override .env.local values
except ImportError:
    pass  # dotenv not installed, rely on system env vars
except Exception as e:
    print(f"Warning: Failed to load environment variables: {e}")
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn

from auth import ClerkAuthMiddleware
from auth.middleware import CORSMiddleware
from middleware import (
    RequestValidationMiddleware,
    ErrorHandlingMiddleware,
    LoggingMiddleware,
    SecurityHeadersMiddleware
)
from routers import health_router, api_router
from routers.debug import router as debug_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    # Startup
    print("Starting Four-Engine System Architecture")

    yield

    # Shutdown
    print("Shutting down Four-Engine System Architecture")


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
    exclude_paths=["/", "/health", "/docs", "/openapi.json", "/redoc", "/debug"]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for dev dashboard (file://, localhost, etc.)
)

# Mount static files for dev dashboard
dev_dashboard_path = os.path.join(os.path.dirname(__file__), "..", "dev-dashboard")
if os.path.exists(dev_dashboard_path):
    app.mount("/dev-dashboard", StaticFiles(directory=dev_dashboard_path, html=True), name="dev-dashboard")
    print("Dev dashboard mounted at /dev-dashboard")

# Include routers
app.include_router(health_router, prefix="", tags=["health"])
app.include_router(api_router, prefix="/api/v1", tags=["api"])

# Mount debug router at root level for dev dashboard (already excluded from auth)
# This allows dashboard to access /debug/* endpoints directly
app.include_router(debug_router, prefix="/debug", tags=["Debug"])

# Mount LLM debug router at root level for dev dashboard (if available)
try:
    from shared.dev_routers.llm_debug import router as llm_debug_router
    # Router already has prefix="/debug/llm", so mount at root
    app.include_router(llm_debug_router, tags=["LLM Debug"])
    print("LLM debug router mounted at /debug/llm")
except ImportError as e:
    print(f"WARNING: LLM debug router not available: {e}")
except Exception as e:
    print(f"WARNING: LLM debug router failed to load: {e}")


@app.get("/")
async def root():
    """Root endpoint - provides API information."""
    return {
        "name": "Four-Engine System Architecture",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "api": "/api/v1",
            "dev_dashboard": "/dev-dashboard"
        }
    }


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

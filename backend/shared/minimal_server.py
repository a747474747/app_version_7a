#!/usr/bin/env python3
"""
Minimal FastAPI server for dev dashboard testing with calculation engine.
Bypasses authentication for development purposes.
"""

import sys
import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime

# Add backend to path for imports
backend_path = os.path.join(os.path.dirname(__file__), '..')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Import calculation engine components
try:
    from calculation_engine.registry import get_registered_calculations
    from services.rule_loader import rule_loader
    CALC_ENGINE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Calculation engine not available: {e}")
    CALC_ENGINE_AVAILABLE = False
    get_registered_calculations = lambda: {}
    rule_loader = None

# Create a dummy user dependency for development
class DummyUser:
    clerk_id = "dev-user"
    email = "dev@example.com"
    role = "admin"

def get_dummy_user():
    """Dummy user dependency for development."""
    return DummyUser()

app = FastAPI(title="Dev Four-Engine Server", version="1.0.0")

# Mount static files for dev dashboard
app.mount("/dev-dashboard", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "dev-dashboard"), html=True), name="dev-dashboard")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for dev dashboard
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers conditionally
from dev_routers.health import router as health_router

app.include_router(health_router)

# Load debug router (contains LLM monitoring endpoints) regardless of calc engine status
try:
    from dev_routers.debug import router as debug_router
    app.include_router(debug_router, prefix="/debug")
    print("Debug endpoints loaded")
except ImportError as e:
    print(f"Warning: Debug router failed to load: {e}")

if CALC_ENGINE_AVAILABLE:
    try:
        from dev_routers.calculations import router as calculations_router
        app.include_router(calculations_router, prefix="/calculations")
        print("Calculation endpoints loaded")
    except ImportError as e:
        print(f"Warning: Calculation router failed to load: {e}")
        CALC_ENGINE_AVAILABLE = False
else:
    print("Warning: Calculation engine not available - limited functionality")

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Dev Four-Engine Server Running",
        "calculation_functions": len(get_registered_calculations()) if CALC_ENGINE_AVAILABLE else 0,
        "rules_loaded": rule_loader.load_rules() is not None if CALC_ENGINE_AVAILABLE else False,
        "calc_engine_available": CALC_ENGINE_AVAILABLE
    }

@app.get("/health/detailed")
async def detailed_health():
    """Detailed health check for development."""
    try:
        registered = get_registered_calculations()
        rules = rule_loader.load_rules()

        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "components": {
                "calculation_engine": {
                    "status": "healthy",
                    "function_count": len(registered),
                    "functions": list(registered.keys())
                },
                "rule_loader": {
                    "status": "healthy",
                    "rules_loaded": True
                },
                "debug_endpoints": "enabled",
                "authentication": "bypassed (dev mode)"
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

if __name__ == "__main__":
    import uvicorn
    print("Starting Dev Four-Engine Server...")
    print("Calculation functions:", len(get_registered_calculations()))
    print("Debug endpoints: enabled")
    print("Authentication: bypassed (dev mode)")
    uvicorn.run(app, host="0.0.0.0", port=8000)

"""
FastAPI middleware for Clerk authentication integration.

This module provides middleware classes for integrating Clerk
authentication with FastAPI applications.
"""

from typing import Optional, Callable
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import jwt


class ClerkAuthMiddleware(BaseHTTPMiddleware):
    """Middleware for Clerk JWT token validation."""

    def __init__(self, app: Callable, exclude_paths: Optional[list] = None):
        super().__init__(app)
        self.exclude_paths = exclude_paths or ["/health", "/docs", "/openapi.json"]
        self.clerk_secret_key = None  # Will be set from config

    async def dispatch(self, request: Request, call_next):
        # Skip authentication for excluded paths
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        # Check for Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization header missing or invalid"}
            )

        token = auth_header.split(" ")[1]

        try:
            # Basic JWT validation (in production, validate against Clerk's JWKS)
            # For now, we'll do basic structure validation
            payload = jwt.decode(token, options={"verify_signature": False})

            # Add user info to request state
            request.state.user_clerk_id = payload.get("sub")
            request.state.user_email = payload.get("email")
            request.state.user_role = payload.get("role", "CLIENT")

        except jwt.InvalidTokenError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid JWT token"}
            )
        except Exception as e:
            return JSONResponse(
                status_code=401,
                content={"detail": f"Authentication error: {str(e)}"}
            )

        # Continue with request
        response = await call_next(request)
        return response


class CORSMiddleware(BaseHTTPMiddleware):
    """CORS middleware for cross-origin requests."""

    def __init__(self, app: Callable, allow_origins: Optional[list] = None):
        super().__init__(app)
        self.allow_origins = allow_origins or ["http://localhost:3000", "https://localhost:3000"]

    async def dispatch(self, request: Request, call_next):
        # Handle preflight requests
        if request.method == "OPTIONS":
            response = JSONResponse(content={})
        else:
            response = await call_next(request)

        # Add CORS headers
        response.headers["Access-Control-Allow-Origin"] = ", ".join(self.allow_origins)
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"

        return response

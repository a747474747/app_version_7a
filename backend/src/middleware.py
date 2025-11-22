"""
Additional middleware for request validation and error handling.

This module provides middleware for input validation, error handling,
and request processing enhancements for the Four-Engine System Architecture.
"""

import json
import time
from typing import Callable, Optional
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)


class RequestValidationMiddleware(BaseHTTPMiddleware):
    """Middleware for request validation and sanitization."""

    def __init__(self, app: Callable, max_request_size: int = 1024 * 1024):  # 1MB default
        super().__init__(app)
        self.max_request_size = max_request_size

    async def dispatch(self, request: Request, call_next):
        # Check request size
        content_length = request.headers.get("content-length")
        if content_length:
            try:
                size = int(content_length)
                if size > self.max_request_size:
                    return JSONResponse(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        content={
                            "detail": "Request entity too large",
                            "max_size": self.max_request_size
                        }
                    )
            except ValueError:
                pass  # Invalid content-length header, continue

        # Validate content-type for POST/PUT/PATCH requests
        if request.method in ["POST", "PUT", "PATCH"]:
            content_type = request.headers.get("content-type", "").lower()
            if not content_type.startswith("application/json"):
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "detail": "Content-Type must be application/json for this request"
                    }
                )

        response = await call_next(request)
        return response


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Enhanced error handling middleware with structured error responses."""

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response

        except HTTPException as exc:
            # Handle FastAPI HTTP exceptions
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "detail": exc.detail,
                    "type": "http_exception",
                    "path": str(request.url),
                    "method": request.method
                }
            )

        except ValueError as exc:
            # Handle validation errors
            logger.warning(f"Validation error: {exc}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "detail": str(exc),
                    "type": "validation_error",
                    "path": str(request.url),
                    "method": request.method
                }
            )

        except Exception as exc:
            # Handle unexpected errors
            logger.error(f"Unexpected error: {exc}", exc_info=True)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail": "An unexpected error occurred",
                    "type": "internal_server_error",
                    "path": str(request.url),
                    "method": request.method
                }
            )


class LoggingMiddleware(BaseHTTPMiddleware):
    """Request logging middleware for monitoring and debugging."""

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log request
        logger.info(f"Request: {request.method} {request.url}")

        try:
            response = await call_next(request)

            # Calculate processing time
            process_time = time.time() - start_time

            # Log response
            logger.info(
                f"Response: {response.status_code} "
                f"Time: {process_time:.3f}s "
                f"Path: {request.url}"
            )

            # Add processing time header
            response.headers["X-Process-Time"] = str(process_time)

            return response

        except Exception as exc:
            # Log exceptions
            process_time = time.time() - start_time
            logger.error(
                f"Exception: {type(exc).__name__} "
                f"Time: {process_time:.3f}s "
                f"Path: {request.url} - {str(exc)}"
            )
            raise


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers to responses."""

    def __init__(self, app: Callable):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self'"

        # Add API versioning header
        response.headers["X-API-Version"] = "v1"

        return response

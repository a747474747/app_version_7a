"""
FastAPI middleware for Clerk authentication integration.

This module provides middleware classes for integrating Clerk
authentication with FastAPI applications.
"""

import os
import time
from typing import Optional, Callable, Dict, Any
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
import requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


class ClerkAuthMiddleware(BaseHTTPMiddleware):
    """Middleware for Clerk JWT token validation."""

    def __init__(self, app: Callable, exclude_paths: Optional[list] = None):
        super().__init__(app)
        self.exclude_paths = exclude_paths or ["/health", "/docs", "/openapi.json", "/redoc"]
        self.clerk_publishable_key = os.getenv("CLERK_PUBLISHABLE_KEY")
        self.clerk_secret_key = os.getenv("CLERK_SECRET_KEY")

        # Extract frontend API URL from publishable key
        # Format: pk_test_XXXXX or pk_live_XXXXX where XXXXX is the instance ID
        if self.clerk_publishable_key and self.clerk_publishable_key.startswith("pk_test_"):
            instance_id = self.clerk_publishable_key.split('_')[2]  # Get instance ID after pk_test
            self.frontend_api_url = f"https://{instance_id}.clerk.accounts.dev"
        elif self.clerk_publishable_key and self.clerk_publishable_key.startswith("pk_live_"):
            instance_id = self.clerk_publishable_key.split('_')[2]  # Get instance ID after pk_live
            self.frontend_api_url = f"https://{instance_id}.clerk.accounts.dev"
        else:
            self.frontend_api_url = None

        self.jwks_url = f"{self.frontend_api_url}/.well-known/jwks.json" if self.frontend_api_url else None
        self.jwks_cache = None
        self.jwks_cache_time = 0
        self.jwks_cache_ttl = 3600  # 1 hour

    def _get_jwks(self) -> Dict[str, Any]:
        """Fetch and cache JWKS from Clerk."""
        current_time = time.time()

        # Return cached JWKS if still valid
        if self.jwks_cache and (current_time - self.jwks_cache_time) < self.jwks_cache_ttl:
            return self.jwks_cache

        if not self.jwks_url:
            raise Exception("JWKS URL not configured")

        try:
            response = requests.get(self.jwks_url, timeout=10)
            response.raise_for_status()
            self.jwks_cache = response.json()
            self.jwks_cache_time = current_time
            return self.jwks_cache
        except Exception as e:
            raise Exception(f"Failed to fetch JWKS: {str(e)}")

    def _get_public_key(self, kid: str) -> str:
        """Get RSA public key from JWKS by key ID."""
        jwks = self._get_jwks()

        for key in jwks.get("keys", []):
            if key.get("kid") == kid and key.get("kty") == "RSA":
                # Convert JWKS key to PEM format
                n = key.get("n")
                e = key.get("e")

                if not n or not e:
                    continue

                # Decode base64url and convert to PEM
                import base64

                # Base64url decode
                n_bytes = base64.urlsafe_b64decode(n + '=' * (4 - len(n) % 4))
                e_bytes = base64.urlsafe_b64decode(e + '=' * (4 - len(e) % 4))

                # Convert to integers
                n_int = int.from_bytes(n_bytes, byteorder='big')
                e_int = int.from_bytes(e_bytes, byteorder='big')

                # Create RSA public key
                from cryptography.hazmat.primitives.asymmetric import rsa
                public_key = rsa.RSAPublicNumbers(e_int, n_int).public_key(default_backend())

                # Serialize to PEM
                pem = public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )

                return pem.decode('utf-8')

        raise Exception(f"Public key with kid '{kid}' not found")

    async def dispatch(self, request: Request, call_next):
        # Skip authentication for excluded paths (exact match or prefix match)
        path = request.url.path
        if path in self.exclude_paths:
            return await call_next(request)
        # Check for prefix matches (e.g., "/debug" matches "/debug/trace-logs")
        for excluded_path in self.exclude_paths:
            if path.startswith(excluded_path):
                return await call_next(request)

        # In development mode without Clerk keys, skip authentication
        if not self.clerk_secret_key:
            # Add dummy user info for development
            request.state.user_clerk_id = "dev-user-123"
            request.state.user_email = "dev@example.com"
            request.state.user_role = "CLIENT"
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
            # Decode header to get key ID (kid)
            header = jwt.get_unverified_header(token)
            kid = header.get("kid")

            if not kid:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "JWT token missing key ID"}
                )

            # Get public key for this token
            public_key_pem = self._get_public_key(kid)

            # Verify and decode JWT token
            payload = jwt.decode(
                token,
                public_key_pem,
                algorithms=["RS256"],
                audience=["clerk"]  # Clerk tokens have this audience
            )

            # Add user info to request state
            request.state.user_clerk_id = payload.get("sub")
            request.state.user_email = payload.get("email")
            request.state.user_first_name = payload.get("given_name")
            request.state.user_last_name = payload.get("family_name")
            request.state.user_role = payload.get("role", "CLIENT")
            request.state.user_org_id = payload.get("org_id")
            request.state.user_permissions = payload.get("permissions", {})

        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Token has expired"}
            )
        except jwt.InvalidTokenError as e:
            return JSONResponse(
                status_code=401,
                content={"detail": f"Invalid JWT token: {str(e)}"}
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
        if self.allow_origins == ["*"]:
            response.headers["Access-Control-Allow-Origin"] = "*"
        else:
            response.headers["Access-Control-Allow-Origin"] = ", ".join(self.allow_origins)
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
        response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type, *"

        return response

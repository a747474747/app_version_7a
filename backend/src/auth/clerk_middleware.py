"""
Clerk authentication middleware for Four-Engine Architecture.

This module provides FastAPI middleware for Clerk authentication,
JWT token validation, and role-based access control.
"""

import os
import time
import base64
from typing import Optional, Dict, Any, List
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt
import requests
from functools import wraps
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

# Clerk configuration
CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")
CLERK_PUBLISHABLE_KEY = os.getenv("CLERK_PUBLISHABLE_KEY")

# Build JWKS URL from publishable key if available
def _build_jwks_url(publishable_key: Optional[str]) -> Optional[str]:
    """Build JWKS URL from Clerk publishable key."""
    if not publishable_key:
        return None
    # Extract instance ID from publishable key (format: pk_test_XXXXX or pk_live_XXXXX)
    if publishable_key.startswith("pk_test_") or publishable_key.startswith("pk_live_"):
        instance_id = publishable_key.split('_')[2]  # Get instance ID after pk_test/pk_live
        return f"https://{instance_id}.clerk.accounts.dev/.well-known/jwks.json"
    return None

CLERK_JWKS_URL = _build_jwks_url(CLERK_PUBLISHABLE_KEY)


class ClerkUser(BaseModel):
    """Clerk user information extracted from JWT token."""
    clerk_id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str = "CLIENT"  # Default role
    organization_id: Optional[str] = None
    permissions: Dict[str, Any] = {}
    token_type: Optional[str] = "session_token"  # session_token or oauth_token
    scopes: Optional[List[str]] = []  # OAuth token scopes (if applicable)


class ClerkAuth:
    """Clerk authentication handler."""

    def __init__(self):
        # Allow development mode without CLERK_SECRET_KEY
        if not CLERK_SECRET_KEY:
            print("WARNING: CLERK_SECRET_KEY not set - using development mode with dummy authentication")
            self.jwks_url = None
            self.dev_mode = True
        else:
            self.jwks_url = CLERK_JWKS_URL
            self.dev_mode = False

        # JWKS cache
        self.jwks_cache = None
        self.jwks_cache_time = 0
        self.jwks_cache_ttl = 3600  # 1 hour

        self.security = HTTPBearer()

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

                # Base64url decode
                n_bytes = base64.urlsafe_b64decode(n + '=' * (4 - len(n) % 4))
                e_bytes = base64.urlsafe_b64decode(e + '=' * (4 - len(e) % 4))

                # Convert to integers
                n_int = int.from_bytes(n_bytes, byteorder='big')
                e_int = int.from_bytes(e_bytes, byteorder='big')

                # Create RSA public key
                public_key = rsa.RSAPublicNumbers(e_int, n_int).public_key(default_backend())

                # Serialize to PEM
                pem = public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )

                return pem.decode('utf-8')

        raise Exception(f"Public key with kid '{kid}' not found")

    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> ClerkUser:
        """Extract and validate user from JWT token."""
        token = credentials.credentials

        # Development mode: return dummy user
        if self.dev_mode:
            return ClerkUser(
                clerk_id="dev-user-123",
                email="dev@example.com",
                first_name="Dev",
                last_name="User",
                role="CLIENT",
                organization_id=None,
                permissions={}
            )

        try:
            # Decode header to get key ID (kid)
            header = jwt.get_unverified_header(token)
            kid = header.get("kid")

            if not kid:
                raise HTTPException(status_code=401, detail="JWT token missing key ID")

            # Get public key for this token from JWKS
            public_key_pem = self._get_public_key(kid)

            # Decode JWT token (Clerk uses RS256)
            # Note: Clerk tokens can be session_token or oauth_token
            # Both use RS256 and audience=["clerk"]
            payload = jwt.decode(
                token,
                public_key_pem,
                algorithms=["RS256"],
                audience=["clerk"]
            )

            # Extract token type from claims (if present)
            # Clerk OAuth tokens may have different claim structures
            token_type = payload.get("token_type") or "session_token"  # Default to session_token
            
            # Extract user information from payload
            clerk_id = payload.get("sub")
            email = payload.get("email")
            first_name = payload.get("given_name")
            last_name = payload.get("family_name")

            # Extract custom claims (roles, permissions, organization)
            role = payload.get("role", "CLIENT")
            organization_id = payload.get("org_id")
            permissions = payload.get("permissions", {})
            
            # For OAuth tokens, check scopes if needed
            # OAuth tokens may have 'scope' claim (space-separated) or 'scopes' (array)
            scopes = payload.get("scopes") or (payload.get("scope", "").split() if payload.get("scope") else [])

            if not clerk_id or not email:
                raise HTTPException(status_code=401, detail="Invalid token payload")

            return ClerkUser(
                clerk_id=clerk_id,
                email=email,
                first_name=first_name,
                last_name=last_name,
                role=role,
                organization_id=organization_id,
                permissions=permissions,
                token_type=token_type,
                scopes=scopes if isinstance(scopes, list) else list(scopes) if scopes else []
            )

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    async def require_role(self, required_role: str):
        """Dependency to require a specific role."""
        def role_checker(user: ClerkUser = Depends(self.get_current_user)):
            role_hierarchy = {
                "CLIENT": 1,
                "ADVISER": 2,
                "COMPLIANCE_OFFICER": 3,
                "ADMIN": 4
            }

            user_level = role_hierarchy.get(user.role, 0)
            required_level = role_hierarchy.get(required_role, 999)

            if user_level < required_level:
                raise HTTPException(
                    status_code=403,
                    detail=f"Insufficient permissions. Required: {required_role}, Have: {user.role}"
                )
            return user
        return role_checker

    async def require_permission(self, permission: str):
        """Dependency to require a specific permission."""
        def permission_checker(user: ClerkUser = Depends(self.get_current_user)):
            if not user.permissions.get(permission, False):
                raise HTTPException(
                    status_code=403,
                    detail=f"Missing required permission: {permission}"
                )
            return user
        return permission_checker


# Global auth instance
clerk_auth = ClerkAuth()


# Convenience dependencies for common use cases
async def get_current_user(user: ClerkUser = Depends(clerk_auth.get_current_user)) -> ClerkUser:
    """Get current authenticated user."""
    return user


async def require_adviser(user: ClerkUser = Depends(clerk_auth.require_role("ADVISER"))) -> ClerkUser:
    """Require adviser role or higher."""
    return user


async def require_compliance_officer(user: ClerkUser = Depends(clerk_auth.require_role("COMPLIANCE_OFFICER"))) -> ClerkUser:
    """Require compliance officer role or higher."""
    return user


async def require_admin(user: ClerkUser = Depends(clerk_auth.require_role("ADMIN"))) -> ClerkUser:
    """Require admin role."""
    return user


def require_permission(permission: str):
    """Factory function to create permission dependencies."""
    async def permission_dependency(user: ClerkUser = Depends(clerk_auth.require_permission(permission))) -> ClerkUser:
        return user
    return permission_dependency


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[ClerkUser]:
    """
    Get current authenticated user, but return None if no auth provided.
    Useful for debug endpoints that should work without auth in dev mode.
    """
    if not credentials:
        # No auth provided - return dummy user in dev mode, None otherwise
        if clerk_auth.dev_mode:
            return ClerkUser(
                clerk_id="dev-user-123",
                email="dev@example.com",
                first_name="Dev",
                last_name="User",
                role="CLIENT",
                organization_id=None,
                permissions={},
                token_type="session_token",
                scopes=[]
            )
        return None
    
    # Auth provided - use normal flow
    return await clerk_auth.get_current_user(credentials)

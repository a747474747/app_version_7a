"""
Clerk authentication middleware for Four-Engine Architecture.

This module provides FastAPI middleware for Clerk authentication,
JWT token validation, and role-based access control.
"""

import os
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt
import requests
from functools import wraps

# Clerk configuration
CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")
CLERK_PUBLISHABLE_KEY = os.getenv("CLERK_PUBLISHABLE_KEY")
CLERK_JWKS_URL = f"https://{CLERK_PUBLISHABLE_KEY.split('_')[1]}.clerk.accounts.dev/.well-known/jwks.json" if CLERK_PUBLISHABLE_KEY else None


class ClerkUser(BaseModel):
    """Clerk user information extracted from JWT token."""
    clerk_id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str = "CLIENT"  # Default role
    organization_id: Optional[str] = None
    permissions: Dict[str, Any] = {}


class ClerkAuth:
    """Clerk authentication handler."""

    def __init__(self):
        if not CLERK_SECRET_KEY:
            raise ValueError("CLERK_SECRET_KEY environment variable is required")

        self.secret_key = CLERK_SECRET_KEY
        self.jwks_url = CLERK_JWKS_URL
        self.security = HTTPBearer()

    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> ClerkUser:
        """Extract and validate user from JWT token."""
        token = credentials.credentials

        try:
            # Decode JWT token (Clerk uses RS256)
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=["RS256"],
                audience=["clerk"]
            )

            # Extract user information from payload
            clerk_id = payload.get("sub")
            email = payload.get("email")
            first_name = payload.get("given_name")
            last_name = payload.get("family_name")

            # Extract custom claims (roles, permissions, organization)
            role = payload.get("role", "CLIENT")
            organization_id = payload.get("org_id")
            permissions = payload.get("permissions", {})

            if not clerk_id or not email:
                raise HTTPException(status_code=401, detail="Invalid token payload")

            return ClerkUser(
                clerk_id=clerk_id,
                email=email,
                first_name=first_name,
                last_name=last_name,
                role=role,
                organization_id=organization_id,
                permissions=permissions
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

"""
Clerk authentication using official Clerk Python SDK.

This module provides FastAPI authentication using Clerk's official SDK,
following Clerk's best practices for token verification.

Reference: https://github.com/clerk/clerk-sdk-python
"""

import os
from typing import Optional, Dict, Any, List
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from clerk_backend_api import Clerk
from clerk_backend_api.security import authenticate_request
from clerk_backend_api.security.types import AuthenticateRequestOptions
import httpx

# Clerk configuration
CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")
CLERK_PUBLISHABLE_KEY = os.getenv("CLERK_PUBLISHABLE_KEY")


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


class ClerkSDKAuth:
    """Clerk authentication handler using official SDK."""

    def __init__(self):
        # Allow development mode without CLERK_SECRET_KEY
        if not CLERK_SECRET_KEY:
            print("WARNING: CLERK_SECRET_KEY not set - using development mode with dummy authentication")
            self.sdk = None
            self.dev_mode = True
        else:
            # Initialize Clerk SDK with secret key
            self.sdk = Clerk(bearer_auth=CLERK_SECRET_KEY)
            self.dev_mode = False

        self.security = HTTPBearer()

    def _convert_request(self, request: Request) -> httpx.Request:
        """Convert FastAPI Request to httpx.Request for Clerk SDK."""
        # Extract headers
        headers = dict(request.headers)
        
        # Create httpx request
        return httpx.Request(
            method=request.method,
            url=str(request.url),
            headers=headers,
        )

    async def get_current_user(
        self, 
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
        request: Optional[Request] = None
    ) -> ClerkUser:
        """
        Extract and validate user from JWT token using Clerk SDK.
        
        This follows Clerk's best practices:
        https://github.com/clerk/clerk-sdk-python#request-authentication
        """
        # Development mode: return dummy user
        if self.dev_mode:
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

        if not self.sdk:
            raise HTTPException(status_code=500, detail="Clerk SDK not initialized")

        try:
            # Convert FastAPI request to httpx request for SDK
            # Note: We need the full request object, but FastAPI dependency injection
            # only gives us the credentials. We'll need to pass request separately.
            # For now, we'll use a simpler approach with just the token.
            
            # Create a mock request with the Authorization header
            mock_request = httpx.Request(
                method="GET",
                url="http://localhost",
                headers={"Authorization": f"Bearer {credentials.credentials}"}
            )
            
            # Authenticate using Clerk SDK
            # Accept both session_token and oauth_token (following Next.js example)
            request_state = self.sdk.authenticate_request(
                mock_request,
                AuthenticateRequestOptions(
                    accepts_token=['session_token', 'oauth_token']
                )
            )

            if not request_state.is_signed_in:
                reason = getattr(request_state, 'reason', 'Unknown authentication error')
                raise HTTPException(
                    status_code=401, 
                    detail=f"Authentication failed: {reason}"
                )

            # Extract payload from request state
            payload = request_state.payload
            if not payload:
                raise HTTPException(status_code=401, detail="Invalid token payload")

            # Extract user information from payload
            clerk_id = payload.get("sub")
            email = payload.get("email")
            first_name = payload.get("given_name")
            last_name = payload.get("family_name")

            # Extract custom claims (roles, permissions, organization)
            role = payload.get("role", "CLIENT")
            organization_id = payload.get("org_id")
            permissions = payload.get("permissions", {})

            # Determine token type from request state
            token_type = getattr(request_state, 'token_type', 'session_token')
            
            # Extract scopes for OAuth tokens
            scopes = []
            if token_type == 'oauth_token':
                # OAuth tokens may have 'scope' claim (space-separated) or 'scopes' (array)
                scopes = payload.get("scopes") or (
                    payload.get("scope", "").split() if payload.get("scope") else []
                )

            if not clerk_id:
                raise HTTPException(status_code=401, detail="Invalid token payload: missing user ID")

            return ClerkUser(
                clerk_id=clerk_id,
                email=email or "unknown@example.com",  # Email might not be in all token types
                first_name=first_name,
                last_name=last_name,
                role=role,
                organization_id=organization_id,
                permissions=permissions,
                token_type=token_type,
                scopes=scopes if isinstance(scopes, list) else list(scopes) if scopes else []
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=401, 
                detail=f"Authentication error: {str(e)}"
            )

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

    def require_scope(self, required_scope: str):
        """Dependency to require a specific OAuth scope."""
        def scope_checker(user: ClerkUser = Depends(self.get_current_user)):
            if user.token_type != 'oauth_token':
                raise HTTPException(
                    status_code=403,
                    detail="OAuth token required for this endpoint"
                )
            if required_scope not in user.scopes:
                raise HTTPException(
                    status_code=403,
                    detail=f"Missing required scope: {required_scope}"
                )
            return user
        return scope_checker


# Global auth instance
clerk_sdk_auth = ClerkSDKAuth()


# Convenience dependencies for common use cases
async def get_current_user(user: ClerkUser = Depends(clerk_sdk_auth.get_current_user)) -> ClerkUser:
    """Get current authenticated user using Clerk SDK."""
    return user


async def require_adviser(user: ClerkUser = Depends(clerk_sdk_auth.require_role("ADVISER"))) -> ClerkUser:
    """Require adviser role or higher."""
    return user


async def require_compliance_officer(user: ClerkUser = Depends(clerk_sdk_auth.require_role("COMPLIANCE_OFFICER"))) -> ClerkUser:
    """Require compliance officer role or higher."""
    return user


async def require_admin(user: ClerkUser = Depends(clerk_sdk_auth.require_role("ADMIN"))) -> ClerkUser:
    """Require admin role."""
    return user


def require_permission(permission: str):
    """Factory function to create permission dependencies."""
    async def permission_dependency(user: ClerkUser = Depends(clerk_sdk_auth.require_permission(permission))) -> ClerkUser:
        return user
    return permission_dependency


def require_scope(scope: str):
    """Factory function to create OAuth scope dependencies."""
    async def scope_dependency(user: ClerkUser = Depends(clerk_sdk_auth.require_scope(scope))) -> ClerkUser:
        return user
    return scope_dependency



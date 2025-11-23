"""
Authentication module for Four-Engine Architecture.

This package provides Clerk authentication integration, middleware,
and authorization utilities for the FastAPI backend.
"""

from .clerk_middleware import (
    ClerkAuth,
    ClerkUser,
    clerk_auth,
    get_current_user,
    get_current_user_optional,
    require_adviser,
    require_compliance_officer,
    require_admin,
    require_permission,
)

from .middleware import (
    ClerkAuthMiddleware,
    CORSMiddleware,
)

# Export all authentication components
__all__ = [
    # Clerk authentication
    "ClerkAuth",
    "ClerkUser",
    "clerk_auth",
    "get_current_user",
    "get_current_user_optional",
    "require_adviser",
    "require_compliance_officer",
    "require_admin",
    "require_permission",

    # Middleware
    "ClerkAuthMiddleware",
    "CORSMiddleware",
]

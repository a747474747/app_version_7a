"""
User profile database model for Four-Engine Architecture.

This module defines the UserProfile model for user management,
roles, and permissions in the multi-user financial advice system.
"""

from typing import Optional, Literal
from sqlalchemy import Column, String, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel


class UserProfile(BaseModel):
    """User profile with role-based access control."""

    __tablename__ = "user_profiles"

    # Clerk authentication integration
    clerk_id = Column(String(255), unique=True, nullable=False, index=True)

    # Basic profile information
    email = Column(String(255), unique=True, nullable=False, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    display_name = Column(String(200))

    # Role-based access control
    role = Column(String(50), nullable=False, default="CLIENT")  # CLIENT, ADVISER, COMPLIANCE_OFFICER, ADMIN
    is_active = Column(Boolean, default=True, nullable=False)

    # Organization/Practice management (for advisers)
    organization_id = Column(String(255), index=True)  # Links to practice/organization
    organization_name = Column(String(255))

    # Professional credentials
    afsl_number = Column(String(50))  # Australian Financial Services Licence
    aflp_number = Column(String(50))  # Australian Financial Licence for Advisers
    certification_expiry = Column(String(10))  # YYYY-MM-DD format

    # Permissions and settings
    permissions = Column(JSON, default=dict)  # Flexible permission structure
    preferences = Column(JSON, default=dict)  # User preferences and settings

    # Audit fields
    last_login_at = Column(String(25))  # ISO timestamp
    created_by_clerk_id = Column(String(255))  # Who created this profile

    # Relationships
    scenarios = relationship("Scenario", back_populates="user_profile", cascade="all, delete-orphan")

    def has_permission(self, permission: str) -> bool:
        """Check if user has a specific permission."""
        return self.permissions.get(permission, False)

    def is_adviser(self) -> bool:
        """Check if user is an adviser."""
        return self.role in ["ADVISER", "ADMIN"]

    def is_compliance_officer(self) -> bool:
        """Check if user is a compliance officer."""
        return self.role in ["COMPLIANCE_OFFICER", "ADMIN"]

    @property
    def full_name(self) -> str:
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.display_name or self.email

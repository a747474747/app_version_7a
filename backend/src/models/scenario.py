"""
Scenario database model for Four-Engine Architecture.

This module defines the Scenario model for storing financial scenarios,
assumptions, and strategy choices.
"""

from typing import Optional, Dict, Any
from sqlalchemy import Column, String, Text, JSON, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .base import BaseModel


class Scenario(BaseModel):
    """Financial scenario with assumptions and strategy choices."""

    __tablename__ = "scenarios"

    # Identity
    scenario_id = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)

    # Ownership
    user_profile_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False, index=True)

    # Scenario state
    status = Column(String(50), nullable=False, default="DRAFT")  # DRAFT, ACTIVE, ARCHIVED, DELETED
    version = Column(String(20), nullable=False, default="1.0")

    # Financial data (stored as JSON for flexibility)
    calculation_state = Column(JSON)  # Complete CalculationState snapshot
    assumption_set = Column(JSON)     # AssumptionSet configuration

    # Strategy configuration
    strategy_config = Column(JSON)    # Strategy model configuration

    # Execution mode (from workflows_and_modes.md)
    mode = Column(String(100), nullable=False, default="MODE-FACT-CHECK")

    # Results and caching
    projection_output = Column(JSON)  # Cached ProjectionOutput
    last_calculated_at = Column(String(25))  # ISO timestamp

    # Metadata
    tags = Column(JSON, default=list)  # List of tags for organization
    scenario_metadata = Column(JSON, default=dict)  # Additional metadata

    # Audit trail
    created_by_clerk_id = Column(String(255), nullable=False)
    updated_by_clerk_id = Column(String(255))

    # Relationships
    user_profile = relationship("UserProfile", back_populates="scenarios")
    advice_outcomes = relationship("AdviceOutcome", back_populates="scenario", cascade="all, delete-orphan")

    def is_active(self) -> bool:
        """Check if scenario is active."""
        return self.status == "ACTIVE"

    def has_calculation_results(self) -> bool:
        """Check if scenario has cached calculation results."""
        return self.projection_output is not None

    def get_assumption_value(self, key: str, default: Any = None) -> Any:
        """Get a specific assumption value."""
        if self.assumption_set:
            return self.assumption_set.get(key, default)
        return default

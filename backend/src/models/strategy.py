"""
Strategy database model for Four-Engine Architecture.

This module defines the Strategy model for optimization templates
and constraints used by the Strategy Engine.
"""

from typing import Optional, Dict, Any, Literal
from sqlalchemy import Column, String, Text, JSON, Boolean

from .base import BaseModel


class Strategy(BaseModel):
    """Optimization template and constraints for Strategy Engine."""

    __tablename__ = "strategies"

    # Identity
    strategy_id = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)

    # Domain and scope
    domain = Column(String(50), nullable=False)  # DEBT, SUPER, TAX, INVESTMENT, RETIREMENT
    target_metric = Column(String(50), nullable=False)  # NET_WEALTH, CASHFLOW_SURPLUS, RETIREMENT_AGE

    # Configuration
    constraints = Column(JSON, default=dict)  # Strategy constraints and limits
    parameters = Column(JSON, default=dict)  # Tunable parameters for optimization

    # Status and availability
    is_active = Column(Boolean, default=True, nullable=False)
    is_template = Column(Boolean, default=True, nullable=False)  # True for reusable templates

    # Metadata
    version = Column(String(20), nullable=False, default="1.0")
    tags = Column(JSON, default=list)  # Categorization tags

    # Audit
    created_by_clerk_id = Column(String(255), nullable=False)
    updated_by_clerk_id = Column(String(255))

    def is_available(self) -> bool:
        """Check if strategy is available for use."""
        return self.is_active

    def get_constraint(self, key: str, default: Any = None) -> Any:
        """Get a specific constraint value."""
        if self.constraints:
            return self.constraints.get(key, default)
        return default

    def get_parameter(self, key: str, default: Any = None) -> Any:
        """Get a specific parameter value."""
        if self.parameters:
            return self.parameters.get(key, default)
        return default

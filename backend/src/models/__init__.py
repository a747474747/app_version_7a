"""
Database models for Four-Engine Architecture.

This package provides SQLAlchemy models for the PostgreSQL database,
organized by domain: user profiles, scenarios, strategies, and advice outcomes.
"""

from .base import Base, BaseModel
from .user_profile import UserProfile
from .scenario import Scenario
from .strategy import Strategy
from .advice_outcome import AdviceOutcome

# Export all models
__all__ = [
    "Base",
    "BaseModel",
    "UserProfile",
    "Scenario",
    "Strategy",
    "AdviceOutcome",
]

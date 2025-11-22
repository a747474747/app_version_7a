"""
Advice outcome database model for Four-Engine Architecture.

This module defines the AdviceOutcome model for storing regulatory
compliance checking results from the Advice Engine.
"""

from typing import Optional, List, Dict, Any
from sqlalchemy import Column, String, Text, JSON, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .base import BaseModel


class AdviceOutcome(BaseModel):
    """Regulatory compliance checking results from Advice Engine."""

    __tablename__ = "advice_outcomes"

    # Identity
    advice_outcome_id = Column(String(255), unique=True, nullable=False, index=True)

    # Link to scenario
    scenario_id = Column(Integer, ForeignKey("scenarios.id"), nullable=False, index=True)

    # Compliance assessment
    best_interest_duty_passed = Column(String(10), nullable=False)  # "PASS", "FAIL", "REVIEW"
    compliance_warnings = Column(JSON, default=list)  # List of compliance warning messages
    regulatory_citations = Column(JSON, default=list)  # List of regulatory reference document IDs

    # Risk assessment
    risk_warnings = Column(JSON, default=list)  # List of risk warning messages
    suitability_score = Column(Float)  # 0.0 to 1.0 suitability score

    # Strategy recommendations
    approved_strategies = Column(JSON, default=list)  # List of approved strategy IDs
    rejected_strategies = Column(JSON, default=dict)  # Dict of strategy_id -> rejection_reason

    # Detailed assessment data
    assessment_details = Column(JSON, default=dict)  # Detailed compliance assessment data

    # Metadata
    assessed_by_clerk_id = Column(String(255), nullable=False)
    assessment_version = Column(String(20), nullable=False, default="1.0")

    # Relationships
    scenario = relationship("Scenario", back_populates="advice_outcomes")

    def compliance_passed(self) -> bool:
        """Check if advice outcome passed compliance checks."""
        return self.best_interest_duty_passed == "PASS"

    def requires_review(self) -> bool:
        """Check if advice outcome requires manual review."""
        return self.best_interest_duty_passed == "REVIEW"

    def has_warnings(self) -> bool:
        """Check if advice outcome has any warnings."""
        return len(self.compliance_warnings) > 0 or len(self.risk_warnings) > 0

    def get_rejection_reason(self, strategy_id: str) -> Optional[str]:
        """Get rejection reason for a specific strategy."""
        if self.rejected_strategies:
            return self.rejected_strategies.get(strategy_id)
        return None

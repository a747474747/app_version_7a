"""
Orchestration schemas for Four-Engine Architecture.

This module defines TraceLog, Strategy, AdviceOutcome models and
other orchestration-related schemas for engine coordination.
"""

from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional, Any, Literal
from pydantic import BaseModel, Field


class TraceEntry(BaseModel):
    """Audit trail entry for explainability."""
    calc_id: str
    entity_id: Optional[str]
    field: str
    explanation: str
    metadata: Dict[str, Any]
    reference_document_id: Optional[str] = None  # Foreign key to regulatory sources


class TraceLog(BaseModel):
    """Complete audit trail for a calculation session."""
    scenario_id: str
    entries: List[TraceEntry] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    version: str = "1.0"


class Strategy(BaseModel):
    """Optimization template and constraints."""
    id: str
    name: str
    domain: Literal["DEBT", "SUPER", "TAX", "INVESTMENT", "RETIREMENT"]

    # Tunable parameters for the Strategy Engine
    target_metric: Literal["NET_WEALTH", "CASHFLOW_SURPLUS", "RETIREMENT_AGE"]
    constraints: Dict[str, Any] = Field(default_factory=dict, description="e.g. {'min_cash_buffer': 20000}")

    # Flags
    is_active: bool = True


class AdviceOutcome(BaseModel):
    """The result of regulatory compliance checking (Advice Engine)."""
    id: str
    scenario_id: str
    generated_at: datetime

    # Compliance results
    best_interest_duty_passed: bool
    compliance_warnings: List[str] = Field(default_factory=list)
    regulatory_citations: List[str] = Field(default_factory=list)  # Reference document IDs

    # Risk assessments
    risk_warnings: List[str] = Field(default_factory=list)
    suitability_score: Optional[float] = Field(None, ge=0.0, le=1.0)

    # Recommendations
    approved_strategies: List[str] = Field(default_factory=list)  # Strategy IDs
    rejected_strategies: Dict[str, str] = Field(default_factory=dict)  # Strategy ID -> rejection reason

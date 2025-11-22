from __future__ import annotations

from typing import Any, Dict, Optional

from calculation_engine.schemas.calculation import CalculationState
from calculation_engine.schemas.orchestration import TraceEntry, TraceSeverity


def add_trace(
    state: CalculationState,
    *,
    calc_id: str,
    entity_id: Optional[str] = None,
    field: Optional[str] = None,
    severity: TraceSeverity = "info",
    year_index: Optional[int] = None,
    explanation: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Append a trace entry to the state's intermediates.trace_log.

    Typical usage inside a CAL function:
        add_trace(
            state,
            calc_id="CAL-PIT-001",
            entity_id=person_id,
            field="net_tax_payable",
            severity="decision_point",
            year_index=0,
            explanation="Applied Stage 3 tax bracket tier 4.",
            metadata={"taxable_income": taxable_income, "bracket_rate": 0.45},
        )
    """

    entry = TraceEntry(
        calc_id=calc_id,
        entity_id=entity_id,
        field=field,
        year_index=year_index,
        severity=severity,
        explanation=explanation,
        metadata=metadata or {},
    )
    state.intermediates.trace_log.append(entry)


# Convenience wrappers if you want them:

def trace_info(
    state: CalculationState,
    *,
    calc_id: str,
    entity_id: Optional[str] = None,
    field: Optional[str] = None,
    year_index: Optional[int] = None,
    explanation: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> None:
    add_trace(
        state,
        calc_id=calc_id,
        entity_id=entity_id,
        field=field,
        severity="info",
        year_index=year_index,
        explanation=explanation,
        metadata=metadata,
    )


def trace_decision(
    state: CalculationState,
    *,
    calc_id: str,
    entity_id: Optional[str] = None,
    field: Optional[str] = None,
    year_index: Optional[int] = None,
    explanation: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> None:
    """
    For key branching points (e.g. which CGT method, which tax bracket).
    """
    add_trace(
        state,
        calc_id=calc_id,
        entity_id=entity_id,
        field=field,
        severity="decision_point",
        year_index=year_index,
        explanation=explanation,
        metadata=metadata,
    )


def trace_warning(
    state: CalculationState,
    *,
    calc_id: str,
    entity_id: Optional[str] = None,
    field: Optional[str] = None,
    year_index: Optional[int] = None,
    explanation: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> None:
    add_trace(
        state,
        calc_id=calc_id,
        entity_id=entity_id,
        field=field,
        severity="warning",
        year_index=year_index,
        explanation=explanation,
        metadata=metadata,
    )

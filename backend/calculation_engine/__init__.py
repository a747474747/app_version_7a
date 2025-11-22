"""
Calculation Engine - Core deterministic calculations for Four-Engine Architecture.

This module provides a unified interface to CAL-* functions that perform pure mathematical
calculations on CalculationState inputs, maintaining separation from AI probabilistic logic.

All calculation functions are now organized in domain modules and accessed via the Registry.
"""

from decimal import Decimal
from typing import Optional, Any
from calculation_engine.schemas.calculation import CalculationState
from calculation_engine.schemas.orchestration import TraceEntry
from .registry import run_calculation as _run_calculation

# Import calculation result schema for backward compatibility
# TODO: This should be moved to shared/schemas once defined
class CalculationResult:
    """Result of a CAL execution."""
    def __init__(self, success: bool, value: Optional[Decimal], trace_entries: list[TraceEntry], error_message: Optional[str] = None):
        self.success = success
        self.value = value
        self.trace_entries = trace_entries
        self.error_message = error_message


def run_calculation(cal_id: str, *args, **kwargs) -> Any:
    """
    Run a calculation by its CAL-ID.

    This is the main entry point for running any calculation function.
    The function delegates to the Registry which maps CAL-IDs to their implementations.

    Args:
        cal_id: The calculation identifier (e.g., "CAL-PIT-001")
        *args: Positional arguments to pass to the calculation function
        **kwargs: Keyword arguments to pass to the calculation function

    Returns:
        The result of the calculation (typically a CalculationResult)

    Raises:
        KeyError: If the CAL-ID is not registered
    """
    return _run_calculation(cal_id, *args, **kwargs)


# For backward compatibility, expose individual functions via delegation
def run_CAL_PIT_001(*args, **kwargs):
    """Calculate PAYG tax for residents."""
    return run_calculation("CAL-PIT-001", *args, **kwargs)

def run_CAL_PIT_002(*args, **kwargs):
    """Calculate Medicare levy."""
    return run_calculation("CAL-PIT-002", *args, **kwargs)

def run_CAL_PIT_004(*args, **kwargs):
    """Aggregate tax offsets."""
    return run_calculation("CAL-PIT-004", *args, **kwargs)

def run_CAL_PIT_005(*args, **kwargs):
    """Calculate net tax payable/refund."""
    return run_calculation("CAL-PIT-005", *args, **kwargs)

def run_CAL_CGT_001(*args, **kwargs):
    """Calculate capital gain/loss on asset disposal."""
    return run_calculation("CAL-CGT-001", *args, **kwargs)

def run_CAL_CGT_002(*args, **kwargs):
    """Apply CGT discount for individuals."""
    return run_calculation("CAL-CGT-002", *args, **kwargs)

def run_CAL_SUP_002(*args, **kwargs):
    """Calculate total concessional contributions."""
    return run_calculation("CAL-SUP-002", *args, **kwargs)

def run_CAL_SUP_003(*args, **kwargs):
    """Check concessional contributions cap utilisation."""
    return run_calculation("CAL-SUP-003", *args, **kwargs)

def run_CAL_SUP_007(*args, **kwargs):
    """Calculate contributions tax inside super."""
    return run_calculation("CAL-SUP-007", *args, **kwargs)

def run_CAL_SUP_008(*args, **kwargs):
    """Calculate Division 293 additional tax."""
    return run_calculation("CAL-SUP-008", *args, **kwargs)

def run_CAL_SUP_009(*args, **kwargs):
    """Calculate net contribution added to balance."""
    return run_calculation("CAL-SUP-009", *args, **kwargs)

def run_CAL_PFL_104(*args, **kwargs):
    """Calculate negative gearing tax benefit."""
    return run_calculation("CAL-PFL-104", *args, **kwargs)

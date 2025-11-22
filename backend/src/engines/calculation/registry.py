"""
Calculation Registry - Maps CAL-IDs to calculation functions.

This module implements the Registry pattern to decouple calculation callers
from specific function implementations. The registry maps CAL-* IDs to their
corresponding functions, enabling modular organization and dynamic lookup.
"""

from typing import Dict, Callable, Any
from shared.schemas.calculation import CalculationState

# Import all domain modules
from .domains import tax_personal, cgt, superannuation, property

# Registry of all calculation functions
CALCULATION_REGISTRY: Dict[str, Callable[..., Any]] = {
    # Personal Income Tax (CAL-PIT-*)
    "CAL-PIT-001": tax_personal.run_CAL_PIT_001,
    "CAL-PIT-002": tax_personal.run_CAL_PIT_002,
    "CAL-PIT-004": tax_personal.run_CAL_PIT_004,
    "CAL-PIT-005": tax_personal.run_CAL_PIT_005,

    # Capital Gains Tax (CAL-CGT-*)
    "CAL-CGT-001": cgt.run_CAL_CGT_001,
    "CAL-CGT-002": cgt.run_CAL_CGT_002,

    # Superannuation (CAL-SUP-*)
    "CAL-SUP-002": superannuation.run_CAL_SUP_002,
    "CAL-SUP-003": superannuation.run_CAL_SUP_003,
    "CAL-SUP-007": superannuation.run_CAL_SUP_007,
    "CAL-SUP-008": superannuation.run_CAL_SUP_008,
    "CAL-SUP-009": superannuation.run_CAL_SUP_009,

    # Property (CAL-PFL-*)
    "CAL-PFL-104": property.run_CAL_PFL_104,
}


def get_calculation(cal_id: str) -> Callable[..., Any]:
    """
    Get a calculation function by its CAL-ID.

    Args:
        cal_id: The calculation identifier (e.g., "CAL-PIT-001")

    Returns:
        The corresponding calculation function

    Raises:
        KeyError: If the CAL-ID is not registered
    """
    if cal_id not in CALCULATION_REGISTRY:
        available_ids = list(CALCULATION_REGISTRY.keys())
        raise KeyError(
            f"Calculation '{cal_id}' not found in registry. "
            f"Available calculations: {available_ids}"
        )

    return CALCULATION_REGISTRY[cal_id]


def register_calculation(cal_id: str, func: Callable[..., Any]) -> None:
    """
    Register a calculation function in the registry.

    Args:
        cal_id: The calculation identifier (e.g., "CAL-PIT-001")
        func: The calculation function to register
    """
    if cal_id in CALCULATION_REGISTRY:
        raise ValueError(f"Calculation '{cal_id}' is already registered")

    CALCULATION_REGISTRY[cal_id] = func


def run_calculation(cal_id: str, *args, **kwargs) -> Any:
    """
    Run a calculation by its CAL-ID.

    This is a convenience function that looks up the calculation function
    and calls it with the provided arguments.

    Args:
        cal_id: The calculation identifier
        *args: Positional arguments to pass to the calculation function
        **kwargs: Keyword arguments to pass to the calculation function

    Returns:
        The result of the calculation
    """
    func = get_calculation(cal_id)
    return func(*args, **kwargs)


def get_registered_calculations() -> Dict[str, Callable[..., Any]]:
    """
    Get a copy of all registered calculations.

    Returns:
        Dictionary mapping CAL-IDs to their functions
    """
    return CALCULATION_REGISTRY.copy()

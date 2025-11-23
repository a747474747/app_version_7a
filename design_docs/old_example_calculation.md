1. Minimal CAL-PIT-001 – base tax on taxable income

Goal:
Given:

taxable_income already computed (e.g. by CAL-PIT-012), and

tax_brackets in state.global_context

compute:

base_tax for that entity, and

(optionally) net_tax_payable if you want this CAL to act as a golden simple tax calc for early MVP.

Save as e.g. backend/calculation_engine/domains/tax_personal.py.

```python

from __future__ import annotations

from typing import List

from ..models.calculation_state import (
    CalculationState,
    TaxBracket,
    TaxResults,
)
from ..services.calculation_trace import trace_decision


def _select_brackets_for_entity(state: CalculationState, entity_id: str) -> List[TaxBracket]:
    """
    Choose the correct tax bracket set based on residency.
    For now: use the same tax brackets for all entities.
    In future versions, this could distinguish between resident/non-resident brackets.
    """
    # Currently, global_context only defines tax_brackets (assumed to be resident brackets)
    # Future enhancement: add separate resident_brackets and non_resident_brackets fields
    return state.global_context.tax_brackets


def _compute_base_tax_from_brackets(
    taxable_income: float,
    brackets: List[TaxBracket],
) -> float:
    """
    Apply stepped bracket tax calculation.

    Assumes brackets are sorted ascending by 'threshold', where each bracket
    defines: tax = base + (taxable_income - threshold) * rate
    for incomes >= threshold.
    """
    if taxable_income <= 0:
        return 0.0

    # Pick the highest bracket where taxable_income >= threshold
    applicable = None
    for bracket in brackets:
        if taxable_income >= bracket.threshold:
            applicable = bracket
        else:
            break

    if applicable is None:
        return 0.0

    return applicable.base + (taxable_income - applicable.threshold) * applicable.rate


def _get_or_create_tax_results(state: CalculationState, entity_id: str) -> TaxResults:
    """
    Ensure state.intermediates.results[entity_id].tax exists and return it.
    """
    entity_results = state.intermediates.results.get(entity_id)
    if entity_results is None:
        # Import here to avoid circular imports if you reorganise modules.
        from ..models.calculation_state import EntityResults

        entity_results = EntityResults()
        state.intermediates.results[entity_id] = entity_results

    return entity_results.tax


def cal_pit_001_base_tax_for_entity(
    state: CalculationState,
    entity_id: str,
    year_index: int | None = None,
) -> None:
    """
    CAL-PIT-001:
      PAYG income tax on taxable income (resident/non-resident).

    Precondition:
      - taxable_income has already been computed and stored in
        state.intermediates.results[entity_id].tax.taxable_income

    Postcondition:
      - state.intermediates.results[entity_id].tax.base_tax is populated.
      - Optionally, net_tax_payable may be set to base_tax if no other
        CALs have set Medicare, offsets, etc. yet.
    """

    tax_results = _get_or_create_tax_results(state, entity_id)

    taxable_income = tax_results.taxable_income
    if taxable_income is None:
        # Nothing to do if we don't yet know taxable income.
        # You might also log a warning trace here.
        return

    brackets = _select_brackets_for_entity(state, entity_id)
    base_tax = _compute_base_tax_from_brackets(taxable_income, brackets)

    tax_results.base_tax = base_tax

    # In a minimal MVP you may choose to set net_tax_payable = base_tax here
    # and later CALs (Medicare, offsets, etc.) can refine it.
    if tax_results.net_tax_payable is None:
        tax_results.net_tax_payable = base_tax

    # Add a trace so the LLM can explain what happened.
    trace_decision(
        state,
        calc_id="CAL-PIT-001",
        entity_id=entity_id,
        field="base_tax",
        year_index=year_index,
        explanation="Calculated base income tax using marginal tax brackets.",
        metadata={
            "taxable_income": taxable_income,
            "base_tax": base_tax,
            "bracket_count": len(brackets),
        },
    )


def cal_pit_001_base_tax_for_all_people(
    state: CalculationState,
    year_index: int | None = None,
) -> None:
    """
    Convenience function: run CAL-PIT-001 for every person in the scenario.
    """
    for person_id in state.entity_context.people.keys():
        cal_pit_001_base_tax_for_entity(
            state,
            entity_id=person_id,
            year_index=year_index,
        )


```

How you’d use this in a pipeline

In a simple “single year” run:

```python

# 1. Build CalculationState from client inputs.
state = build_state_from_inputs(...)

# 2. Run CALs that derive taxable_income (not shown here).
#    e.g., CAL-PIT-011 aggregate assessable income, CAL-PIT-012 -> taxable_income.

# 3. Run base tax for all people.
cal_pit_001_base_tax_for_all_people(state)

# 4. Read results:
for pid, results in state.intermediates.results.items():
    print(pid, results.tax.taxable_income, results.tax.base_tax, results.tax.net_tax_payable)


````

Later you add:

CAL-PIT-002 (Medicare levy)

CAL-PIT-003 (MLS)

CAL-PIT-004 (offset aggregation)

CAL-PIT-005 (final net_tax_payable)

All writing into TaxResults on the same structure.
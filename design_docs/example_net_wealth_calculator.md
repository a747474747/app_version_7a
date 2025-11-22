2. Net wealth calculator (per person + household)

This demonstrates:

Using Asset.ownership (with shares)

Using Loan.borrower_entity_ids

Handling smsf_member_balance without double-counting underlying SMSF assets.

Save as backend/src/services/net_wealth.py.

```python

from __future__ import annotations

from typing import Iterable, Dict

from ..models.calculation_state import CalculationState, Asset, Loan


def _ownership_share_for_entity(asset: Asset, entity_id: str) -> float:
    """
    Find the ownership share of a given entity in an asset.
    Returns 0.0 if not an owner.
    """
    return next(
        (o.share for o in asset.ownership if o.entity_id == entity_id),
        0.0,
    )


def _loan_share_for_entity(loan: Loan, entity_id: str) -> float:
    """
    Simple assumption: if an entity is one of the borrower_entity_ids,
    the loan is split equally among them.

    You can refine this later to support custom split ratios.
    """
    if entity_id not in loan.borrower_entity_ids:
        return 0.0

    count = len(loan.borrower_entity_ids)
    if count <= 0:
        return 0.0

    return 1.0 / count


def calculate_net_wealth_for_entity(
    state: CalculationState,
    entity_id: str,
) -> float:
    """
    Net wealth = sum(share of asset values) - sum(share of liabilities)
    for a single entity (person or other entity).

    - For SMSF member balances, we rely on assets of type 'smsf_member_balance'
      owned by the person (as defined in the Pydantic skeleton).
    - Underlying SMSF assets are not directly attributed to the person,
      so we avoid double counting.
    """
    total_assets = 0.0
    total_liabilities = 0.0

    # Assets
    for asset in state.position_context.assets.values():
        share = _ownership_share_for_entity(asset, entity_id)
        if share <= 0.0:
            continue

        value = asset.current_valuation.amount * share
        total_assets += value

    # Liabilities
    for loan in state.position_context.liabilities.values():
        share = _loan_share_for_entity(loan, entity_id)
        if share <= 0.0:
            continue

        liability_amount = loan.principal_outstanding * share
        total_liabilities += liability_amount

    return total_assets - total_liabilities


def calculate_household_net_wealth(
    state: CalculationState,
    person_ids: Iterable[str],
) -> float:
    """
    Household net wealth: sum of individual net wealth for given person_ids.

    This is a simple approach that:
      - counts each person's share of assets and liabilities,
      - does NOT double-count jointly owned assets because each person
        only claims their share (e.g. 0.5 + 0.5).

    If you want a "whole-of-household" view that counts the full property
    value for the couple, you would instead:
      - include the full asset amount if ANY of the household members is
        an owner, and ignore ownership shares.
    """
    person_ids = list(person_ids)
    total = 0.0
    for pid in person_ids:
        total += calculate_net_wealth_for_entity(state, pid)
    return total


def calculate_household_net_wealth_whole_property(
    state: CalculationState,
    person_ids: Iterable[str],
) -> float:
    """
    Alternative: Whole-of-household net wealth, counting 100% of each
    jointly-owned asset if any member of the household owns any share.

    Useful for client-facing 'what is our household worth?' views.
    """
    person_ids = set(person_ids)
    assets_total = 0.0
    liabilities_total = 0.0

    # Assets: if any owner is in the household, include full asset value once
    for asset in state.position_context.assets.values():
        owner_ids = {o.entity_id for o in asset.ownership}
        if owner_ids & person_ids:  # intersection not empty
            assets_total += asset.current_valuation.amount

    # Liabilities: if any borrower is in household, include full liability
    for loan in state.position_context.liabilities.values():
        borrower_ids = set(loan.borrower_entity_ids)
        if borrower_ids & person_ids:
            liabilities_total += loan.principal_outstanding

    return assets_total - liabilities_total

```

Example usage

```python

from ..services.net_wealth import (
    calculate_net_wealth_for_entity,
    calculate_household_net_wealth,
    calculate_household_net_wealth_whole_property,
)

# Assume you have a state already populated.
state = build_state_from_inputs(...)

primary_id = "person_primary"
partner_id = "person_partner"

primary_nw = calculate_net_wealth_for_entity(state, primary_id)
partner_nw = calculate_net_wealth_for_entity(state, partner_id)

household_nw_shares = calculate_household_net_wealth(state, [primary_id, partner_id])
household_nw_whole = calculate_household_net_wealth_whole_property(
    state, [primary_id, partner_id]
)

print("Primary net wealth:", primary_nw)
print("Partner net wealth:", partner_nw)
print("Household net wealth (by shares):", household_nw_shares)
print("Household net wealth (whole-of-household):", household_nw_whole)

```
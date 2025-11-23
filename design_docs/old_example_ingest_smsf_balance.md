3. Sketch: ingesting SMSF member balances as smsf_member_balance assets

Here’s how you might convert raw client data into:

an SMSFEntity, plus

one Asset per member of type "smsf_member_balance".

Assume you’ve already created a CalculationState and you’re filling entity_context and position_context.


```python

from datetime import date
from typing import List, Dict

from ..models.calculation_state import (
    CalculationState,
    SMSFEntity,
    Asset,
    AssetType,
    Ownership,
    ValuationSnapshot,
)


def ingest_smsf_from_raw(
    state: CalculationState,
    *,
    smsf_id: str,
    smsf_name: str,
    as_at: date,
    member_balances: List[Dict],
) -> None:
    """
    Ingest one SMSF and its members' balances.

    member_balances: list of dicts like:
        {
            "member_person_id": "person_1",
            "balance": 350000.0,
            "taxable_component": 320000.0,
            "tax_free_component": 30000.0,
        }
    """

    # 1. Create or update the SMSF entity
    smsf = SMSFEntity(
        id=smsf_id,
        name=smsf_name,
        # You can set taxable_income_ordinary/NALI/etc separately from tax data
    )
    state.entity_context.smsfs[smsf_id] = smsf

    # 2. For each member, create an smsf_member_balance Asset
    for idx, mb in enumerate(member_balances):
        person_id = mb["member_person_id"]
        balance = float(mb["balance"])

        asset_id = f"{smsf_id}_member_{idx+1}"

        asset = Asset(
            id=asset_id,
            asset_type="smsf_member_balance",
            ownership=[
                Ownership(entity_id=person_id, share=1.0)
            ],
            valuations=[
                ValuationSnapshot(
                    amount=balance,
                    effective_date=as_at,
                    source="client_estimate",  # or provider_feed if you have it
                )
            ],
            linked_entity_id=smsf_id,
        )

        state.position_context.assets[asset_id] = asset

        # Optional: you might also stash tax components in metadata if needed
        # asset.extra_fields... (Config extra="allow" lets you add them later)

```

Typical pipeline for a client with SMSF:

Create people in entity_context.people (with DOB, residency, etc).

Call ingest_smsf_from_raw with:

smsf_id = "smsf_001"

member_balances matching each person’s member interest.

Net wealth views will:

Sum Asset valuations (including "smsf_member_balance"), weighted by ownership.share.

SMSF analytics (NALI, ECPI, etc.) will:

Use state.entity_context.smsfs[smsf_id] and any additional SMSF-specific data you ingest.
"""
Calculation Engine Domains - Domain-driven calculation modules.

This package contains domain-specific calculation functions organized by financial domain:
- tax_personal: Personal income tax calculations (CAL-PIT-*)
- cgt: Capital gains tax calculations (CAL-CGT-*)
- superannuation: Superannuation calculations (CAL-SUP-*)
- property: Property investment calculations (CAL-PFL-*)
"""

from . import tax_personal, cgt, superannuation, property

__all__ = ["tax_personal", "cgt", "superannuation", "property"]
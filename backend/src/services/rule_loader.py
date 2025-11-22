"""
Rule Loader Service - Loads calculation parameters from external configuration files.

This service hydrates Calculation Engine parameters from YAML/JSON config files
rather than hardcoding values, enabling dynamic rule updates and compliance.
"""

import os
import json
import yaml
from typing import Dict, Any, Optional, List
from pathlib import Path
from decimal import Decimal
from dataclasses import dataclass


@dataclass
class TaxRuleSet:
    """Container for tax calculation rules."""
    brackets: List[Dict[str, Any]]
    medicare_levy_rate: Decimal
    medicare_levy_thresholds: Dict[str, Decimal]
    lito_parameters: Dict[str, Decimal]


@dataclass
class SuperRuleSet:
    """Container for superannuation calculation rules."""
    concessional_cap: Decimal
    contributions_tax_rate: Decimal
    division_293_threshold: Decimal
    division_293_rate: Decimal


@dataclass
class CapitalGainsRuleSet:
    """Container for capital gains tax rules."""
    individual_discount_rate: Decimal


@dataclass
class PropertyRuleSet:
    """Container for property investment rules."""
    marginal_tax_rate: Decimal


@dataclass
class CalculationRules:
    """Complete set of calculation rules for all domains."""
    tax: TaxRuleSet
    superannuation: SuperRuleSet
    capital_gains: CapitalGainsRuleSet
    property: PropertyRuleSet


class RuleLoader:
    """
    Service for loading calculation rules from external configuration files.

    Supports YAML and JSON formats for rule definitions.
    """

    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize RuleLoader with configuration directory.

        Args:
            config_dir: Directory containing rule configuration files.
                       Defaults to 'config/rules' relative to backend/src.
        """
        if config_dir is None:
            # Default to config/rules relative to this file
            current_dir = Path(__file__).parent
            config_dir = current_dir / ".." / ".." / "config" / "rules"

        self.config_dir = Path(config_dir)
        self._rules_cache: Optional[CalculationRules] = None
        self._cache_timestamp: Optional[float] = None

    def load_rules(self, force_reload: bool = False) -> CalculationRules:
        """
        Load calculation rules from configuration files.

        Args:
            force_reload: If True, reload from disk even if cached

        Returns:
            CalculationRules containing all rule sets

        Raises:
            FileNotFoundError: If required configuration files are missing
            ValueError: If configuration data is invalid
        """
        # Check if we have cached rules and they're still valid
        if not force_reload and self._rules_cache is not None:
            config_modified = self._check_config_modified()
            if not config_modified:
                return self._rules_cache

        # Load rules from files
        tax_rules = self._load_tax_rules()
        super_rules = self._load_super_rules()
        cgt_rules = self._load_cgt_rules()
        property_rules = self._load_property_rules()

        self._rules_cache = CalculationRules(
            tax=tax_rules,
            superannuation=super_rules,
            capital_gains=cgt_rules,
            property=property_rules
        )

        # Update cache timestamp
        self._cache_timestamp = self._get_latest_modification_time()

        return self._rules_cache

    def _load_tax_rules(self) -> TaxRuleSet:
        """Load tax calculation rules from tax-rules.yaml/json."""
        config_file = self._find_config_file("tax-rules")
        config_data = self._load_config_file(config_file)

        # Validate required fields
        if "brackets" not in config_data:
            raise ValueError("Tax rules must contain 'brackets' configuration")
        if "medicare_levy" not in config_data:
            raise ValueError("Tax rules must contain 'medicare_levy' configuration")

        # Parse tax brackets
        brackets = []
        for bracket in config_data["brackets"]:
            brackets.append({
                "min": Decimal(str(bracket.get("min", 0))),
                "max": Decimal(str(bracket.get("max", "inf"))) if bracket.get("max") else None,
                "rate": Decimal(str(bracket["rate"]))
            })

        # Parse Medicare levy settings
        medicare_config = config_data["medicare_levy"]
        medicare_levy_rate = Decimal(str(medicare_config["rate"]))
        thresholds = {
            key: Decimal(str(value))
            for key, value in medicare_config.get("thresholds", {}).items()
        }

        # Parse LITO parameters
        lito_config = config_data.get("lito", {})
        lito_parameters = {
            "max_offset": Decimal(str(lito_config.get("max_offset", 700))),
            "income_limit": Decimal(str(lito_config.get("income_limit", 37500))),
            "phase_out_start": Decimal(str(lito_config.get("phase_out_start", 37500))),
            "phase_out_end": Decimal(str(lito_config.get("phase_out_end", 67500))),
            "phase_out_rate": Decimal(str(lito_config.get("phase_out_rate", 0.05)))
        }

        return TaxRuleSet(
            brackets=brackets,
            medicare_levy_rate=medicare_levy_rate,
            medicare_levy_thresholds=thresholds,
            lito_parameters=lito_parameters
        )

    def _load_super_rules(self) -> SuperRuleSet:
        """Load superannuation calculation rules."""
        config_file = self._find_config_file("super-rules")
        config_data = self._load_config_file(config_file)

        return SuperRuleSet(
            concessional_cap=Decimal(str(config_data.get("concessional_cap", 11000))),
            contributions_tax_rate=Decimal(str(config_data.get("contributions_tax_rate", 0.15))),
            division_293_threshold=Decimal(str(config_data.get("division_293_threshold", 250000))),
            division_293_rate=Decimal(str(config_data.get("division_293_rate", 0.15)))
        )

    def _load_cgt_rules(self) -> CapitalGainsRuleSet:
        """Load capital gains tax rules."""
        config_file = self._find_config_file("cgt-rules")
        config_data = self._load_config_file(config_file)

        return CapitalGainsRuleSet(
            individual_discount_rate=Decimal(str(config_data.get("individual_discount_rate", 0.5)))
        )

    def _load_property_rules(self) -> PropertyRuleSet:
        """Load property investment rules."""
        config_file = self._find_config_file("property-rules")
        config_data = self._load_config_file(config_file)

        return PropertyRuleSet(
            marginal_tax_rate=Decimal(str(config_data.get("marginal_tax_rate", 0.32)))
        )

    def _find_config_file(self, base_name: str) -> Path:
        """Find configuration file, trying YAML first then JSON."""
        yaml_file = self.config_dir / f"{base_name}.yaml"
        json_file = self.config_dir / f"{base_name}.json"

        if yaml_file.exists():
            return yaml_file
        elif json_file.exists():
            return json_file
        else:
            raise FileNotFoundError(
                f"Configuration file not found: {base_name}.yaml or {base_name}.json "
                f"in {self.config_dir}"
            )

    def _load_config_file(self, file_path: Path) -> Dict[str, Any]:
        """Load and parse configuration file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            if file_path.suffix.lower() == '.yaml':
                return yaml.safe_load(f)
            else:  # JSON
                return json.load(f)

    def _check_config_modified(self) -> bool:
        """Check if any configuration files have been modified since last load."""
        if self._cache_timestamp is None:
            return True

        latest_modification = self._get_latest_modification_time()
        return latest_modification > self._cache_timestamp

    def _get_latest_modification_time(self) -> float:
        """Get the latest modification time of any configuration file."""
        latest_time = 0.0

        if not self.config_dir.exists():
            return latest_time

        for config_file in self.config_dir.glob("*"):
            if config_file.is_file() and config_file.suffix in ['.yaml', '.json']:
                file_time = config_file.stat().st_mtime
                latest_time = max(latest_time, file_time)

        return latest_time

    def get_tax_brackets(self) -> List[Dict[str, Any]]:
        """Get tax brackets for progressive tax calculations."""
        rules = self.load_rules()
        return rules.tax.brackets

    def get_medicare_levy_rate(self) -> Decimal:
        """Get Medicare levy rate."""
        rules = self.load_rules()
        return rules.tax.medicare_levy_rate

    def get_medicare_levy_thresholds(self) -> Dict[str, Decimal]:
        """Get Medicare levy thresholds."""
        rules = self.load_rules()
        return rules.tax.medicare_levy_thresholds

    def get_lito_parameters(self) -> Dict[str, Decimal]:
        """Get LITO calculation parameters."""
        rules = self.load_rules()
        return rules.tax.lito_parameters

    def get_concessional_cap(self) -> Decimal:
        """Get super concessional contributions cap."""
        rules = self.load_rules()
        return rules.superannuation.concessional_cap

    def get_contributions_tax_rate(self) -> Decimal:
        """Get super contributions tax rate."""
        rules = self.load_rules()
        return rules.superannuation.contributions_tax_rate

    def get_division_293_threshold(self) -> Decimal:
        """Get Division 293 threshold."""
        rules = self.load_rules()
        return rules.superannuation.division_293_threshold

    def get_division_293_rate(self) -> Decimal:
        """Get Division 293 additional tax rate."""
        rules = self.load_rules()
        return rules.superannuation.division_293_rate

    def get_cgt_discount_rate(self) -> Decimal:
        """Get CGT discount rate for individuals."""
        rules = self.load_rules()
        return rules.capital_gains.individual_discount_rate

    def get_marginal_tax_rate(self) -> Decimal:
        """Get default marginal tax rate for property calculations."""
        rules = self.load_rules()
        return rules.property.marginal_tax_rate


# Global rule loader instance
rule_loader = RuleLoader()

"""
Privacy Filtering Module

This module provides utilities for filtering and redacting Personally Identifiable Information (PII)
before sending data to external LLM services in the Four-Engine Architecture.

Key Responsibilities:
- Detect and redact sensitive personal information
- Maintain data utility while ensuring privacy
- Support configurable privacy levels
- Provide audit trails for redaction actions
- Comply with privacy regulations and best practices

Author: AI Assistant
Created: 2025-11-22
Timezone: Australia/Brisbane (UTC+10)
"""

import logging
import re
from typing import Any, Dict, List, Optional, Set, Union
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class PrivacyLevel(Enum):
    """Privacy filtering levels."""
    MINIMAL = "minimal"  # Only redact obvious PII
    STANDARD = "standard"  # Redact common PII categories
    STRICT = "strict"  # Redact all potentially sensitive information
    MAXIMUM = "maximum"  # Redact everything except calculation results


class PIIType(Enum):
    """Types of Personally Identifiable Information."""
    NAME = "name"
    EMAIL = "email"
    PHONE = "phone"
    ADDRESS = "address"
    TAX_ID = "tax_id"
    DOB = "date_of_birth"
    SSN = "social_security_number"
    PASSPORT = "passport_number"
    DRIVERS_LICENSE = "drivers_license"
    BANK_ACCOUNT = "bank_account"
    CREDIT_CARD = "credit_card"
    MEDICAL_INFO = "medical_information"
    FINANCIAL_ID = "financial_identifiers"


@dataclass
class PrivacyFilterResult:
    """Result of privacy filtering operation."""
    filtered_text: str
    redacted_items: List[Dict[str, Any]] = field(default_factory=list)
    privacy_level: PrivacyLevel = PrivacyLevel.STANDARD
    confidence_score: float = 1.0
    audit_trail: List[str] = field(default_factory=list)


@dataclass
class PIIPattern:
    """Pattern for detecting PII."""
    pii_type: PIIType
    regex: str
    replacement: str
    description: str
    privacy_levels: Set[PrivacyLevel]


class PrivacyFilter:
    """
    Advanced privacy filtering system for LLM data sanitization.

    This class provides comprehensive PII detection and redaction capabilities
    with configurable privacy levels and audit trails.
    """

    def __init__(self, privacy_level: PrivacyLevel = PrivacyLevel.STANDARD):
        """
        Initialize the privacy filter.

        Args:
            privacy_level: Default privacy filtering level
        """
        self.default_privacy_level = privacy_level
        self._patterns = self._initialize_patterns()

    def _initialize_patterns(self) -> List[PIIPattern]:
        """Initialize PII detection patterns."""
        return [
            # Names (common patterns)
            PIIPattern(
                pii_type=PIIType.NAME,
                regex=r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b',
                replacement="[REDACTED_NAME]",
                description="Full names (First Last)",
                privacy_levels={PrivacyLevel.STANDARD, PrivacyLevel.STRICT, PrivacyLevel.MAXIMUM}
            ),

            # Email addresses
            PIIPattern(
                pii_type=PIIType.EMAIL,
                regex=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                replacement="[REDACTED_EMAIL]",
                description="Email addresses",
                privacy_levels={PrivacyLevel.STANDARD, PrivacyLevel.STRICT, PrivacyLevel.MAXIMUM}
            ),

            # Phone numbers (various formats)
            PIIPattern(
                pii_type=PIIType.PHONE,
                regex=r'\b(?:\+?61|0)[4-5]\d{2}[\s-]?\d{3}[\s-]?\d{3}\b',
                replacement="[REDACTED_PHONE_AU]",
                description="Australian phone numbers",
                privacy_levels={PrivacyLevel.STANDARD, PrivacyLevel.STRICT, PrivacyLevel.MAXIMUM}
            ),

            # Addresses (simplified pattern)
            PIIPattern(
                pii_type=PIIType.ADDRESS,
                regex=r'\b\d+\s+[A-Za-z0-9\s,.-]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Way|Place|Pl|Court|Ct)\b',
                replacement="[REDACTED_ADDRESS]",
                description="Street addresses",
                privacy_levels={PrivacyLevel.STRICT, PrivacyLevel.MAXIMUM}
            ),

            # Tax File Numbers (Australian)
            PIIPattern(
                pii_type=PIIType.TAX_ID,
                regex=r'\b\d{3}\s?\d{3}\s?\d{3}\b',
                replacement="[REDACTED_TFN]",
                description="Tax File Numbers (TFN)",
                privacy_levels={PrivacyLevel.STRICT, PrivacyLevel.MAXIMUM}
            ),

            # Dates of birth
            PIIPattern(
                pii_type=PIIType.DOB,
                regex=r'\b(?:19|20)\d{2}[-/](?:0[1-9]|1[0-2])[-/](?:0[1-9]|[12]\d|3[01])\b',
                replacement="[REDACTED_DOB]",
                description="Dates of birth",
                privacy_levels={PrivacyLevel.STRICT, PrivacyLevel.MAXIMUM}
            ),

            # Bank account numbers (simplified)
            PIIPattern(
                pii_type=PIIType.BANK_ACCOUNT,
                regex=r'\b\d{6,10}\b',
                replacement="[REDACTED_ACCOUNT]",
                description="Bank account numbers",
                privacy_levels={PrivacyLevel.STRICT, PrivacyLevel.MAXIMUM}
            ),

            # Medical information keywords
            PIIPattern(
                pii_type=PIIType.MEDICAL_INFO,
                regex=r'\b(?:diagnosis|condition|treatment|medication|doctor|hospital|clinic)\b',
                replacement="[REDACTED_MEDICAL]",
                description="Medical information references",
                privacy_levels={PrivacyLevel.MAXIMUM}
            ),
        ]

    def filter_text(
        self,
        text: str,
        privacy_level: Optional[PrivacyLevel] = None,
        context_hints: Optional[List[str]] = None
    ) -> PrivacyFilterResult:
        """
        Filter PII from text based on privacy level.

        Args:
            text: Input text to filter
            privacy_level: Privacy level to apply (uses default if None)
            context_hints: Additional context for smarter filtering

        Returns:
            PrivacyFilterResult with filtered text and audit information
        """
        level = privacy_level or self.default_privacy_level
        filtered_text = text
        redacted_items = []
        audit_trail = [f"Applied privacy level: {level.value}"]

        # Apply patterns based on privacy level
        applicable_patterns = [
            pattern for pattern in self._patterns
            if level in pattern.privacy_levels
        ]

        for pattern in applicable_patterns:
            matches = list(re.finditer(pattern.regex, filtered_text, re.IGNORECASE))
            if matches:
                for match in matches:
                    # Create redaction record
                    redaction = {
                        "type": pattern.pii_type.value,
                        "original": match.group(),
                        "replacement": pattern.replacement,
                        "position": match.span(),
                        "description": pattern.description,
                        "confidence": self._calculate_match_confidence(match.group(), pattern, context_hints)
                    }
                    redacted_items.append(redaction)

                    # Apply replacement
                    filtered_text = filtered_text[:match.start()] + pattern.replacement + filtered_text[match.end():]

                audit_trail.append(f"Redacted {len(matches)} instances of {pattern.pii_type.value}")

        # Calculate overall confidence
        avg_confidence = (
            sum(item["confidence"] for item in redacted_items) / len(redacted_items)
            if redacted_items else 1.0
        )

        return PrivacyFilterResult(
            filtered_text=filtered_text,
            redacted_items=redacted_items,
            privacy_level=level,
            confidence_score=avg_confidence,
            audit_trail=audit_trail
        )

    def filter_calculation_state(
        self,
        calculation_state: Dict[str, Any],
        privacy_level: Optional[PrivacyLevel] = None
    ) -> PrivacyFilterResult:
        """
        Filter PII from CalculationState data structure.

        Args:
            calculation_state: CalculationState as dictionary
            privacy_level: Privacy level to apply

        Returns:
            PrivacyFilterResult with filtered state
        """
        # Convert to JSON string for processing
        state_json = str(calculation_state)

        # Filter the JSON representation
        filter_result = self.filter_text(state_json, privacy_level)

        # Try to parse back to dict (may fail if redaction broke JSON structure)
        try:
            # This is a simplified approach - in production you'd want more sophisticated
            # JSON-aware filtering that preserves structure
            filtered_state = calculation_state.copy()

            # Apply filtering to string fields that might contain PII
            if "entity_context" in filtered_state:
                entities = filtered_state["entity_context"].get("entities", [])
                for entity in entities:
                    if "name" in entity:
                        name_result = self.filter_text(entity["name"], privacy_level)
                        entity["name"] = name_result.filtered_text

            return PrivacyFilterResult(
                filtered_text=str(filtered_state),
                redacted_items=filter_result.redacted_items,
                privacy_level=filter_result.privacy_level,
                confidence_score=filter_result.confidence_score,
                audit_trail=filter_result.audit_trail + ["Filtered CalculationState structure"]
            )

        except Exception as e:
            logger.warning(f"Failed to filter CalculationState structure: {str(e)}")
            return filter_result

    def add_custom_pattern(
        self,
        pii_type: PIIType,
        regex: str,
        replacement: str,
        description: str,
        privacy_levels: Set[PrivacyLevel]
    ) -> None:
        """
        Add a custom PII detection pattern.

        Args:
            pii_type: Type of PII this pattern detects
            regex: Regular expression pattern
            replacement: Replacement text for redaction
            description: Human-readable description
            privacy_levels: Privacy levels where this pattern applies
        """
        pattern = PIIPattern(
            pii_type=pii_type,
            regex=regex,
            replacement=replacement,
            description=description,
            privacy_levels=privacy_levels
        )
        self._patterns.append(pattern)

    def _calculate_match_confidence(
        self,
        matched_text: str,
        pattern: PIIPattern,
        context_hints: Optional[List[str]]
    ) -> float:
        """
        Calculate confidence score for a PII match.

        Args:
            matched_text: The text that matched the pattern
            pattern: The pattern that matched
            context_hints: Context hints for better confidence scoring

        Returns:
            Confidence score between 0.0 and 1.0
        """
        base_confidence = 0.8  # Default confidence for regex matches

        # Adjust based on pattern type
        type_multipliers = {
            PIIType.EMAIL: 0.95,
            PIIType.PHONE: 0.90,
            PIIType.TAX_ID: 0.98,
            PIIType.NAME: 0.75,  # Names can be ambiguous
            PIIType.ADDRESS: 0.85,
            PIIType.DOB: 0.95,
        }

        confidence = base_confidence * type_multipliers.get(pattern.pii_type, 0.8)

        # Adjust based on context hints
        if context_hints:
            context_boost = 0.0
            for hint in context_hints:
                if hint.lower() in ["personal", "client", "customer", "individual"]:
                    context_boost = max(context_boost, 0.1)
                elif hint.lower() in ["company", "business", "corporate"]:
                    context_boost = max(context_boost, -0.1)  # Reduce confidence for business context

            confidence += context_boost

        return max(0.0, min(1.0, confidence))

    def get_available_patterns(self, privacy_level: Optional[PrivacyLevel] = None) -> List[Dict[str, Any]]:
        """
        Get information about available PII patterns.

        Args:
            privacy_level: Filter patterns by privacy level

        Returns:
            List of pattern information
        """
        patterns = self._patterns
        if privacy_level:
            patterns = [p for p in patterns if privacy_level in p.privacy_levels]

        return [
            {
                "type": pattern.pii_type.value,
                "description": pattern.description,
                "replacement": pattern.replacement,
                "privacy_levels": [level.value for level in pattern.privacy_levels]
            }
            for pattern in patterns
        ]


# Global filter instances for different privacy levels
_privacy_filters = {}

def get_privacy_filter(privacy_level: PrivacyLevel = PrivacyLevel.STANDARD) -> PrivacyFilter:
    """
    Get or create a privacy filter for the specified level.

    Args:
        privacy_level: Privacy level for the filter

    Returns:
        PrivacyFilter instance
    """
    if privacy_level not in _privacy_filters:
        _privacy_filters[privacy_level] = PrivacyFilter(privacy_level)
    return _privacy_filters[privacy_level]


# Convenience functions
def filter_text_for_llm(
    text: str,
    privacy_level: PrivacyLevel = PrivacyLevel.STANDARD
) -> str:
    """
    Convenience function to filter text for LLM consumption.

    Args:
        text: Text to filter
        privacy_level: Privacy level to apply

    Returns:
        Filtered text safe for LLM consumption
    """
    filter_instance = get_privacy_filter(privacy_level)
    result = filter_instance.filter_text(text)
    return result.filtered_text


def scrub_pii(text: str) -> str:
    """
    Legacy function for backward compatibility.
    Simple PII scrubbing with standard privacy level.

    Args:
        text: Text to scrub

    Returns:
        Scrubbed text
    """
    return filter_text_for_llm(text, PrivacyLevel.STANDARD)

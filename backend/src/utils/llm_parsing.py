"""
LLM Response Parsing and Validation Utilities.

This module provides utilities for parsing, validating, and processing
LLM responses across the four-engine architecture.
"""

import json
import re
import logging
from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel, ValidationError, validator

from services.openrouter_client import ChatCompletionResponse, ChatMessage


logger = logging.getLogger(__name__)


class ParsingError(Exception):
    """Exception raised when LLM response parsing fails."""
    pass


class ValidationError(Exception):
    """Exception raised when LLM response validation fails."""
    pass


class ResponseFormat(str, Enum):
    """Supported response formats from LLM."""
    JSON = "json"
    MARKDOWN = "markdown"
    PLAIN_TEXT = "plain_text"
    STRUCTURED = "structured"


@dataclass
class ParsedLLMResponse:
    """Container for parsed LLM response data."""
    format: ResponseFormat
    content: Any
    raw_response: str
    confidence_score: float = 1.0
    validation_errors: List[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.validation_errors is None:
            self.validation_errors = []
        if self.metadata is None:
            self.metadata = {}


class JSONSchemaValidator:
    """
    Validator for JSON responses against expected schemas.

    Supports validation of LLM-generated JSON against Pydantic models
    and custom validation rules.
    """

    @staticmethod
    def validate_json_response(
        response_text: str,
        schema_model: Optional[type[BaseModel]] = None,
        required_fields: Optional[List[str]] = None,
        field_validators: Optional[Dict[str, callable]] = None
    ) -> Tuple[bool, List[str], Dict[str, Any]]:
        """
        Validate a JSON response against schema and custom rules.

        Args:
            response_text: Raw JSON string from LLM
            schema_model: Pydantic model to validate against
            required_fields: List of fields that must be present
            field_validators: Dict of field_name -> validator_function

        Returns:
            Tuple of (is_valid, error_messages, parsed_data)
        """
        errors = []
        parsed_data = {}

        try:
            # Parse JSON
            parsed_data = json.loads(response_text)
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON: {str(e)}")
            return False, errors, parsed_data

        # Validate against Pydantic schema
        if schema_model:
            try:
                validated = schema_model(**parsed_data)
                parsed_data = validated.dict()
            except ValidationError as e:
                for error in e.errors():
                    field_path = ".".join(str(x) for x in error["loc"])
                    errors.append(f"Schema validation failed for {field_path}: {error['msg']}")

        # Check required fields
        if required_fields:
            for field in required_fields:
                if not JSONSchemaValidator._has_nested_field(parsed_data, field):
                    errors.append(f"Required field missing: {field}")

        # Apply custom field validators
        if field_validators:
            for field_path, validator_func in field_validators.items():
                try:
                    field_value = JSONSchemaValidator._get_nested_field(parsed_data, field_path)
                    if field_value is not None:
                        validator_func(field_value)
                except Exception as e:
                    errors.append(f"Field validation failed for {field_path}: {str(e)}")

        return len(errors) == 0, errors, parsed_data

    @staticmethod
    def _has_nested_field(data: Dict, field_path: str) -> bool:
        """Check if a nested field exists in the data structure."""
        keys = field_path.split(".")
        current = data

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return False
        return True

    @staticmethod
    def _get_nested_field(data: Dict, field_path: str) -> Any:
        """Get a nested field value from the data structure."""
        keys = field_path.split(".")
        current = data

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        return current


class MarkdownParser:
    """
    Parser for markdown-formatted LLM responses.

    Extracts structured data from markdown content including code blocks,
    tables, lists, and formatted sections.
    """

    @staticmethod
    def parse_markdown_response(response_text: str) -> ParsedLLMResponse:
        """
        Parse a markdown-formatted response.

        Args:
            response_text: Markdown text from LLM

        Returns:
            Parsed response with extracted content
        """
        content = {
            "sections": MarkdownParser._extract_sections(response_text),
            "code_blocks": MarkdownParser._extract_code_blocks(response_text),
            "tables": MarkdownParser._extract_tables(response_text),
            "lists": MarkdownParser._extract_lists(response_text),
        }

        return ParsedLLMResponse(
            format=ResponseFormat.MARKDOWN,
            content=content,
            raw_response=response_text,
            metadata={"parser": "markdown"}
        )

    @staticmethod
    def _extract_sections(text: str) -> Dict[str, str]:
        """Extract sections from markdown headers."""
        sections = {}
        lines = text.split("\n")
        current_section = None
        current_content = []

        for line in lines:
            if line.startswith("#"):
                # Save previous section
                if current_section:
                    sections[current_section] = "\n".join(current_content).strip()

                # Start new section
                header_match = re.match(r"^(#{1,6})\s+(.+)$", line)
                if header_match:
                    current_section = header_match.group(2).strip()
                    current_content = []
                else:
                    current_section = line.strip("# ").strip()
                    current_content = []
            elif current_section:
                current_content.append(line)

        # Save last section
        if current_section:
            sections[current_section] = "\n".join(current_content).strip()

        return sections

    @staticmethod
    def _extract_code_blocks(text: str) -> List[Dict[str, str]]:
        """Extract code blocks with language information."""
        code_blocks = []
        pattern = r"```(\w+)?\n(.*?)\n```"
        matches = re.findall(pattern, text, re.DOTALL)

        for language, code in matches:
            code_blocks.append({
                "language": language or "text",
                "code": code.strip()
            })

        return code_blocks

    @staticmethod
    def _extract_tables(text: str) -> List[List[List[str]]]:
        """Extract tables from markdown."""
        tables = []
        lines = text.split("\n")
        current_table = []
        in_table = False

        for line in lines:
            if "|" in line and not in_table:
                in_table = True
                current_table = []

            if in_table:
                if "|" in line:
                    # Parse table row
                    cells = [cell.strip() for cell in line.split("|")[1:-1]]
                    current_table.append(cells)
                elif line.strip() == "" and current_table:
                    # End of table
                    if len(current_table) > 1:  # Must have header + at least one data row
                        tables.append(current_table)
                    current_table = []
                    in_table = False

        # Handle table at end of text
        if current_table and len(current_table) > 1:
            tables.append(current_table)

        return tables

    @staticmethod
    def _extract_lists(text: str) -> Dict[str, List[str]]:
        """Extract ordered and unordered lists."""
        lines = text.split("\n")
        unordered_lists = []
        ordered_lists = []
        current_list = []
        current_type = None

        for line in lines:
            if re.match(r"^\s*[-*+]\s+", line):
                if current_type == "ordered":
                    if current_list:
                        ordered_lists.append(current_list)
                    current_list = []

                current_type = "unordered"
                item = re.sub(r"^\s*[-*+]\s+", "", line).strip()
                current_list.append(item)

            elif re.match(r"^\s*\d+\.\s+", line):
                if current_type == "unordered":
                    if current_list:
                        unordered_lists.append(current_list)
                    current_list = []

                current_type = "ordered"
                item = re.sub(r"^\s*\d+\.\s+", "", line).strip()
                current_list.append(item)

            elif line.strip() == "" and current_list:
                # End current list
                if current_type == "unordered":
                    unordered_lists.append(current_list)
                elif current_type == "ordered":
                    ordered_lists.append(current_list)
                current_list = []
                current_type = None

        # Handle list at end of text
        if current_list:
            if current_type == "unordered":
                unordered_lists.append(current_list)
            elif current_type == "ordered":
                ordered_lists.append(current_list)

        return {
            "unordered": unordered_lists,
            "ordered": ordered_lists
        }


class StructuredDataParser:
    """
    Parser for structured data responses from LLM.

    Handles responses that contain specific data structures like
    calculations, recommendations, or configuration data.
    """

    @staticmethod
    def parse_calculation_response(response_text: str) -> ParsedLLMResponse:
        """
        Parse a response containing calculation data.

        Args:
            response_text: Response text with calculation data

        Returns:
            Parsed response with calculation structure
        """
        # Extract calculation IDs and results
        calc_pattern = r"CAL-([A-Z]+)-(\d+)"
        calculations = {}

        for match in re.finditer(calc_pattern, response_text):
            calc_id = f"CAL-{match.group(1)}-{match.group(2)}"
            # Extract surrounding context as explanation
            start = max(0, match.start() - 100)
            end = min(len(response_text), match.end() + 200)
            context = response_text[start:end]
            calculations[calc_id] = {
                "found": True,
                "context": context.strip()
            }

        return ParsedLLMResponse(
            format=ResponseFormat.STRUCTURED,
            content={"calculations": calculations},
            raw_response=response_text,
            metadata={"data_type": "calculations"}
        )

    @staticmethod
    def parse_recommendation_response(response_text: str) -> ParsedLLMResponse:
        """
        Parse a response containing recommendations.

        Args:
            response_text: Response text with recommendations

        Returns:
            Parsed response with recommendation structure
        """
        # Extract recommendations using common patterns
        recommendations = []

        # Look for numbered or bulleted recommendations
        rec_patterns = [
            r"(\d+)\.\s*(.+?)(?=\d+\.|$)",
            r"[-*]\s*(.+?)(?=[-*]|$)",
        ]

        for pattern in rec_patterns:
            matches = re.findall(pattern, response_text, re.MULTILINE | re.DOTALL)
            for match in matches:
                if isinstance(match, tuple):
                    recommendations.append(match[1].strip())
                else:
                    recommendations.append(match.strip())

        return ParsedLLMResponse(
            format=ResponseFormat.STRUCTURED,
            content={"recommendations": recommendations},
            raw_response=response_text,
            metadata={"data_type": "recommendations"}
        )


class LLMResponseParser:
    """
    Main parser for LLM responses with automatic format detection
    and validation.
    """

    def __init__(self):
        self.json_validator = JSONSchemaValidator()
        self.markdown_parser = MarkdownParser()
        self.structured_parser = StructuredDataParser()

    def parse_response(
        self,
        response: Union[str, ChatCompletionResponse],
        expected_format: Optional[ResponseFormat] = None,
        schema_model: Optional[type[BaseModel]] = None,
        validation_rules: Optional[Dict[str, Any]] = None
    ) -> ParsedLLMResponse:
        """
        Parse an LLM response with automatic format detection.

        Args:
            response: Raw response string or ChatCompletionResponse
            expected_format: Expected response format (auto-detected if None)
            schema_model: Pydantic model for JSON validation
            validation_rules: Additional validation rules

        Returns:
            Parsed and validated response

        Raises:
            ParsingError: If parsing fails
            ValidationError: If validation fails
        """
        # Extract text content
        if isinstance(response, ChatCompletionResponse):
            if response.choices and len(response.choices) > 0:
                response_text = response.choices[0].message.content
            else:
                raise ParsingError("No content in ChatCompletionResponse")
        else:
            response_text = str(response)

        # Auto-detect format if not specified
        if expected_format is None:
            detected_format = self._detect_format(response_text)
        else:
            detected_format = expected_format

        # Parse based on format
        try:
            if detected_format == ResponseFormat.JSON:
                parsed = self._parse_json_response(response_text, schema_model, validation_rules)
            elif detected_format == ResponseFormat.MARKDOWN:
                parsed = self.markdown_parser.parse_markdown_response(response_text)
            elif detected_format == ResponseFormat.STRUCTURED:
                parsed = self._parse_structured_response(response_text)
            else:
                parsed = ParsedLLMResponse(
                    format=ResponseFormat.PLAIN_TEXT,
                    content=response_text,
                    raw_response=response_text
                )

            # Apply validation rules
            if validation_rules:
                self._apply_validation_rules(parsed, validation_rules)

            return parsed

        except Exception as e:
            logger.error(f"Failed to parse response: {str(e)}")
            raise ParsingError(f"Response parsing failed: {str(e)}") from e

    def _detect_format(self, response_text: str) -> ResponseFormat:
        """Auto-detect the response format."""
        response_text = response_text.strip()

        # Check for JSON
        if response_text.startswith("{") and response_text.endswith("}"):
            try:
                json.loads(response_text)
                return ResponseFormat.JSON
            except json.JSONDecodeError:
                pass

        # Check for markdown features
        if any(marker in response_text for marker in ["# ", "## ", "- ", "* ", "```", "|"]):
            return ResponseFormat.MARKDOWN

        # Check for structured data patterns
        if any(pattern in response_text.upper() for pattern in ["CAL-", "RECOMMEND", "ADVICE"]):
            return ResponseFormat.STRUCTURED

        return ResponseFormat.PLAIN_TEXT

    def _parse_json_response(
        self,
        response_text: str,
        schema_model: Optional[type[BaseModel]] = None,
        validation_rules: Optional[Dict[str, Any]] = None
    ) -> ParsedLLMResponse:
        """Parse and validate JSON response."""
        required_fields = validation_rules.get("required_fields", []) if validation_rules else []
        field_validators = validation_rules.get("field_validators", {}) if validation_rules else {}

        is_valid, errors, parsed_data = self.json_validator.validate_json_response(
            response_text, schema_model, required_fields, field_validators
        )

        parsed = ParsedLLMResponse(
            format=ResponseFormat.JSON,
            content=parsed_data,
            raw_response=response_text,
            validation_errors=errors if not is_valid else []
        )

        if not is_valid:
            logger.warning(f"JSON validation failed: {errors}")

        return parsed

    def _parse_structured_response(self, response_text: str) -> ParsedLLMResponse:
        """Parse structured response based on content type."""
        # Try different structured parsers
        if "CAL-" in response_text.upper():
            return self.structured_parser.parse_calculation_response(response_text)
        elif any(word in response_text.lower() for word in ["recommend", "suggest", "advice"]):
            return self.structured_parser.parse_recommendation_response(response_text)
        else:
            # Fallback to plain text
            return ParsedLLMResponse(
                format=ResponseFormat.STRUCTURED,
                content={"text": response_text},
                raw_response=response_text
            )

    def _apply_validation_rules(self, parsed: ParsedLLMResponse, rules: Dict[str, Any]) -> None:
        """Apply custom validation rules to parsed response."""
        # Content length validation
        if "max_length" in rules:
            content_str = str(parsed.content)
            if len(content_str) > rules["max_length"]:
                parsed.validation_errors.append(
                    f"Content exceeds maximum length: {len(content_str)} > {rules['max_length']}"
                )

        # Required keywords
        if "required_keywords" in rules:
            content_str = parsed.raw_response.lower()
            for keyword in rules["required_keywords"]:
                if keyword.lower() not in content_str:
                    parsed.validation_errors.append(f"Required keyword missing: {keyword}")

        # Confidence scoring based on validation
        if parsed.validation_errors:
            parsed.confidence_score = max(0.1, 1.0 - (len(parsed.validation_errors) * 0.2))


# Global parser instance
_response_parser = LLMResponseParser()


def parse_llm_response(
    response: Union[str, ChatCompletionResponse],
    expected_format: Optional[ResponseFormat] = None,
    **kwargs
) -> ParsedLLMResponse:
    """
    Convenience function to parse LLM responses.

    Args:
        response: Response to parse
        expected_format: Expected format
        **kwargs: Additional parsing options

    Returns:
        Parsed response
    """
    return _response_parser.parse_response(response, expected_format, **kwargs)

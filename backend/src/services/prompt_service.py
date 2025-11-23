"""
Prompt Service for LLM Prompt Management

This service provides utilities for loading and managing LLM prompts from the
specs/001-four-engine-architecture/llm-prompts/ directory structure.

CRITICAL: This service loads prompt text from files, never embeds prompt text directly.
All prompts must be maintained in separate files and loaded dynamically.

Author: AI Assistant
Created: 2025-11-22
Timezone: Australia/Brisbane (UTC+10)
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PromptMetadata:
    """Metadata for a prompt from the catalog."""
    prompt_id: str
    title: str
    description: str
    mode_id: Optional[int]
    category: str
    version: str
    file_path: str
    related_files: List[str]
    created_date: str
    last_updated: str


class PromptService:
    """
    Service for loading and managing LLM prompts from the prompt catalog.

    This service provides:
    - Loading prompt text from files based on prompt_id
    - Accessing prompt metadata from the catalog
    - Validating prompt existence and integrity
    - Caching loaded prompts for performance
    """

    def __init__(self, specs_base_path: Optional[Path] = None):
        """
        Initialize the prompt service.

        Args:
            specs_base_path: Base path to specs directory. Defaults to project root + specs.
        """
        if specs_base_path is None:
            # Default to project root + specs
            self.specs_base = Path(__file__).parent.parent.parent.parent / "specs"
        else:
            self.specs_base = specs_base_path

        self.prompts_base = self.specs_base / "001-four-engine-architecture" / "llm-prompts"
        self.catalog_path = self.prompts_base / "catalog.json"

        # Cache for loaded prompts
        self._prompt_cache: Dict[str, str] = {}
        self._catalog_cache: Optional[List[Dict[str, Any]]] = None
        self._catalog_loaded_at: Optional[datetime] = None

    def _load_catalog(self, force_reload: bool = False) -> List[Dict[str, Any]]:
        """
        Load the prompt catalog from disk.

        Args:
            force_reload: If True, reload catalog even if cached.

        Returns:
            List of catalog entries.

        Raises:
            FileNotFoundError: If catalog.json doesn't exist.
            json.JSONDecodeError: If catalog.json is invalid JSON.
        """
        if not force_reload and self._catalog_cache is not None:
            return self._catalog_cache

        if not self.catalog_path.exists():
            raise FileNotFoundError(f"Prompt catalog not found at {self.catalog_path}")

        with open(self.catalog_path, 'r', encoding='utf-8') as f:
            self._catalog_cache = json.load(f)
            self._catalog_loaded_at = datetime.now()

        return self._catalog_cache

    def get_prompt_metadata(self, prompt_id: str) -> PromptMetadata:
        """
        Get metadata for a prompt from the catalog.

        Args:
            prompt_id: Unique identifier for the prompt.

        Returns:
            PromptMetadata object with catalog information.

        Raises:
            ValueError: If prompt_id is not found in catalog.
        """
        catalog = self._load_catalog()

        for entry in catalog:
            if entry["prompt_id"] == prompt_id:
                return PromptMetadata(
                    prompt_id=entry["prompt_id"],
                    title=entry["title"],
                    description=entry["description"],
                    mode_id=entry.get("mode_id"),
                    category=entry["category"],
                    version=entry["version"],
                    file_path=entry["file_path"],
                    related_files=entry.get("related_files", []),
                    created_date=entry["created_date"],
                    last_updated=entry["last_updated"]
                )

        raise ValueError(f"Prompt '{prompt_id}' not found in catalog")

    def load_prompt(self, prompt_id: str, use_cache: bool = True) -> str:
        """
        Load prompt text from file based on prompt_id.

        Args:
            prompt_id: Unique identifier for the prompt.
            use_cache: If True, return cached prompt if available.

        Returns:
            The full prompt text as a string.

        Raises:
            ValueError: If prompt_id is not found in catalog.
            FileNotFoundError: If prompt file doesn't exist.
            IOError: If prompt file cannot be read.
        """
        if use_cache and prompt_id in self._prompt_cache:
            return self._prompt_cache[prompt_id]

        # Get metadata to find the file path
        metadata = self.get_prompt_metadata(prompt_id)
        prompt_file_path = self.prompts_base / metadata.file_path

        if not prompt_file_path.exists():
            raise FileNotFoundError(f"Prompt file not found at {prompt_file_path}")

        try:
            with open(prompt_file_path, 'r', encoding='utf-8') as f:
                prompt_text = f.read()
        except IOError as e:
            raise IOError(f"Failed to read prompt file {prompt_file_path}: {e}")

        # Cache the loaded prompt
        if use_cache:
            self._prompt_cache[prompt_id] = prompt_text

        return prompt_text

    def get_available_prompts(self, category: Optional[str] = None) -> List[PromptMetadata]:
        """
        Get list of all available prompts, optionally filtered by category.

        Args:
            category: Optional category filter ("core_orchestrator", "mode_prompt", "shared_utility").

        Returns:
            List of PromptMetadata objects for available prompts.
        """
        catalog = self._load_catalog()
        prompts = []

        for entry in catalog:
            if category is None or entry["category"] == category:
                prompts.append(PromptMetadata(
                    prompt_id=entry["prompt_id"],
                    title=entry["title"],
                    description=entry["description"],
                    mode_id=entry.get("mode_id"),
                    category=entry["category"],
                    version=entry["version"],
                    file_path=entry["file_path"],
                    related_files=entry.get("related_files", []),
                    created_date=entry["created_date"],
                    last_updated=entry["last_updated"]
                ))

        return prompts

    def get_mode_prompts(self) -> Dict[int, PromptMetadata]:
        """
        Get all mode-specific prompts indexed by mode_id.

        Returns:
            Dictionary mapping mode_id (1-26) to PromptMetadata.
        """
        mode_prompts = {}
        catalog = self._load_catalog()

        for entry in catalog:
            if entry["category"] == "mode_prompt" and entry.get("mode_id") is not None:
                mode_id = entry["mode_id"]
                mode_prompts[mode_id] = PromptMetadata(
                    prompt_id=entry["prompt_id"],
                    title=entry["title"],
                    description=entry["description"],
                    mode_id=mode_id,
                    category=entry["category"],
                    version=entry["version"],
                    file_path=entry["file_path"],
                    related_files=entry.get("related_files", []),
                    created_date=entry["created_date"],
                    last_updated=entry["last_updated"]
                )

        return mode_prompts

    def clear_cache(self):
        """Clear all cached prompts and force reload of catalog on next access."""
        self._prompt_cache.clear()
        self._catalog_cache = None
        self._catalog_loaded_at = None

    def validate_prompt_integrity(self, prompt_id: str) -> bool:
        """
        Validate that a prompt exists in catalog and file is readable.

        Args:
            prompt_id: Unique identifier for the prompt.

        Returns:
            True if prompt is valid and accessible.

        Raises:
            ValueError: If prompt_id is not found in catalog.
            FileNotFoundError: If prompt file doesn't exist.
            IOError: If prompt file cannot be read.
        """
        # This will raise exceptions if prompt is not found or file issues
        self.load_prompt(prompt_id, use_cache=False)
        return True


# Global service instance for convenience
prompt_service = PromptService()


def load_prompt(prompt_id: str) -> str:
    """
    Convenience function to load a prompt using the global service instance.

    Args:
        prompt_id: Unique identifier for the prompt.

    Returns:
        The full prompt text as a string.
    """
    return prompt_service.load_prompt(prompt_id)


def get_prompt_metadata(prompt_id: str) -> PromptMetadata:
    """
    Convenience function to get prompt metadata using the global service instance.

    Args:
        prompt_id: Unique identifier for the prompt.

    Returns:
        PromptMetadata object with catalog information.
    """
    return prompt_service.get_prompt_metadata(prompt_id)

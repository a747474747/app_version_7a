#!/usr/bin/env python3
"""
Python Scripts Rule Validation Tool

Validates compliance with the Python Scripts Rule (.cursor/rules/python-scripts.mdc):
- Backend Python scripts must be in /backend folder and have tracking entries
- Frontend Python scripts must be in /frontend folder and have tracking entries
- All scripts must have valid tracking entries in script_tracking.json
- Tracking file must be valid JSON with proper structure
- Validates required fields and data formats
"""

import os
import sys
import json
import glob
from pathlib import Path
from typing import Dict, List, Set, Tuple
from datetime import datetime


class PythonRuleValidator:
    """Validator for Python Scripts Rule compliance."""

    def __init__(self, backend_root: str = None):
        if backend_root is None:
            # Find backend root from script location
            script_dir = Path(__file__).parent
            if script_dir.name == 'backend':
                self.backend_root = script_dir
            else:
                self.backend_root = script_dir / 'backend'
        else:
            self.backend_root = Path(backend_root)

        self.project_root = self.backend_root.parent
        self.tracking_file = self.backend_root / 'script_tracking.json'
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self) -> bool:
        """Run all validation checks. Returns True if all pass."""
        print("🔍 Validating Python Scripts Rule compliance...")

        self.errors = []
        self.warnings = []

        self._validate_python_files_location()
        self._validate_tracking_file_exists()
        self._validate_tracking_file_json()
        self._validate_tracking_completeness()
        self._validate_tracking_structure()
        self._validate_tracking_duplicates()
        self._validate_interacts_with_paths()

        # Report results
        if self.errors:
            print(f"❌ {len(self.errors)} errors found:")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print(f"⚠️  {len(self.warnings)} warnings:")
            for warning in self.warnings:
                print(f"  - {warning}")

        if not self.errors:
            print("✅ All Python Scripts Rule validations passed!")
            return True
        else:
            print("❌ Python Scripts Rule violations found!")
            return False

    def _validate_python_files_location(self):
        """Check that Python files are in allowed locations (backend or frontend)."""
        print("  Checking Python file locations...")

        # Find all Python files in the project
        python_files = []
        for py_file in glob.glob("**/*.py", root_dir=self.project_root, recursive=True):
            # Skip files in common directories that shouldn't contain engine scripts
            if not any(skip in py_file for skip in [
                '__pycache__',
                'node_modules',
                '.git',
                'alembic/versions/',  # These are generated
                'build/',
                'dist/'
            ]):
                python_files.append(py_file)

        # Check for Python files outside allowed locations (backend or frontend)
        violations = []
        for py_file in python_files:
            if not (py_file.startswith('backend/') or py_file.startswith('frontend/')):
                violations.append(py_file)

        if violations:
            self.errors.append(
                f"Found {len(violations)} Python files outside allowed locations (/backend or /frontend): {', '.join(violations[:5])}{'...' if len(violations) > 5 else ''}"
            )

        # Check for potentially misplaced frontend scripts (4-engine logic in frontend)
        frontend_scripts = [f for f in python_files if f.startswith('frontend/')]
        for script in frontend_scripts:
            script_path = self.project_root / script
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    # Check for 4-engine related keywords that shouldn't be in frontend
                    engine_keywords = ['calculation_engine', 'llm_orchestrator', 'strategy_engine', 'advice_engine', 'cal-p', 'cal-c', 'cal-s', 'cal-a']
                    if any(keyword in content for keyword in engine_keywords):
                        self.warnings.append(f"Frontend script '{script}' appears to contain 4-engine architecture logic (should be in backend)")
            except Exception:
                pass  # Skip files that can't be read

    def _validate_tracking_file_exists(self):
        """Check that the tracking file exists."""
        print("  Checking tracking file existence...")
        if not self.tracking_file.exists():
            self.errors.append(f"Tracking file not found: {self.tracking_file}")
            return

        if not self.tracking_file.is_file():
            self.errors.append(f"Tracking file is not a regular file: {self.tracking_file}")

    def _validate_tracking_file_json(self):
        """Check that the tracking file is valid JSON."""
        print("  Validating tracking file JSON...")
        if not self.tracking_file.exists():
            return

        try:
            with open(self.tracking_file, 'r') as f:
                self.tracking_data = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"Tracking file is not valid JSON: {e}")
            return
        except Exception as e:
            self.errors.append(f"Error reading tracking file: {e}")
            return

        if not isinstance(self.tracking_data, list):
            self.errors.append("Tracking file must contain a JSON array")
            return

    def _validate_tracking_completeness(self):
        """Check that all Python files (backend and frontend) have tracking entries."""
        print("  Checking tracking completeness...")

        if not hasattr(self, 'tracking_data'):
            return

        # Get all Python files in backend
        backend_py_files = []
        for py_file in glob.glob("**/*.py", root_dir=self.backend_root, recursive=True):
            if not any(skip in py_file for skip in ['__pycache__', '.git']):
                backend_py_files.append(py_file)

        # Get all Python files in frontend
        frontend_py_files = []
        frontend_dir = self.project_root / 'frontend'
        if frontend_dir.exists():
            for py_file in glob.glob("**/*.py", root_dir=frontend_dir, recursive=True):
                if not any(skip in py_file for skip in ['__pycache__', '.git', 'node_modules']):
                    frontend_py_files.append(f"frontend/{py_file}")

        # Get tracked script names
        tracked_scripts = {entry.get('script_name') for entry in self.tracking_data if isinstance(entry, dict)}

        # Check for untracked files
        untracked = []
        for py_file in backend_py_files + frontend_py_files:
            if py_file not in tracked_scripts:
                untracked.append(py_file)

        if untracked:
            self.errors.append(
                f"Found {len(untracked)} Python files without tracking entries: {', '.join(untracked[:5])}{'...' if len(untracked) > 5 else ''}"
            )

    def _validate_tracking_structure(self):
        """Check that tracking entries have required fields and correct formats."""
        print("  Validating tracking entry structure...")

        if not hasattr(self, 'tracking_data'):
            return

        required_fields = [
            'script_name', 'description', 'created_date',
            'created_timezone', 'engine', 'interacts_with', 'purpose'
        ]

        valid_engines = ['llm_orchestrator', 'calculation_engine', 'strategy_engine', 'advice_engine', 'shared', 'frontend']
        required_timezone = 'Australia/Brisbane'

        for i, entry in enumerate(self.tracking_data):
            if not isinstance(entry, dict):
                self.errors.append(f"Entry {i} is not a JSON object")
                continue

            # Check required fields
            missing_fields = []
            for field in required_fields:
                if field not in entry:
                    missing_fields.append(field)

            if missing_fields:
                self.errors.append(f"Entry {i} ({entry.get('script_name', 'unknown')}) missing required fields: {missing_fields}")
                continue

            # Validate field formats
            script_name = entry['script_name']

            # Validate created_date format
            try:
                datetime.strptime(entry['created_date'], '%Y-%m-%d')
            except ValueError:
                self.errors.append(f"Entry {i} ({script_name}) has invalid created_date format (must be YYYY-MM-DD)")

            # Validate timezone
            if entry['created_timezone'] != required_timezone:
                self.errors.append(f"Entry {i} ({script_name}) has invalid timezone (must be '{required_timezone}')")

            # Validate engine
            if entry['engine'] not in valid_engines:
                self.errors.append(f"Entry {i} ({script_name}) has invalid engine (must be one of {valid_engines})")

            # Validate interacts_with is array
            if not isinstance(entry['interacts_with'], list):
                self.errors.append(f"Entry {i} ({script_name}) interacts_with must be an array")

            # Validate description length
            if len(entry['description']) > 100:
                self.warnings.append(f"Entry {i} ({script_name}) description exceeds 100 characters")

    def _validate_tracking_duplicates(self):
        """Check for duplicate script_name entries."""
        print("  Checking for duplicate tracking entries...")

        if not hasattr(self, 'tracking_data'):
            return

        script_names = {}
        for i, entry in enumerate(self.tracking_data):
            if isinstance(entry, dict) and 'script_name' in entry:
                script_name = entry['script_name']
                if script_name in script_names:
                    self.errors.append(f"Duplicate script_name '{script_name}' found in entries {script_names[script_name]} and {i}")
                else:
                    script_names[script_name] = i

    def _validate_interacts_with_paths(self):
        """Check that all interacts_with paths are valid."""
        print("  Validating interacts_with paths...")

        if not hasattr(self, 'tracking_data'):
            return

        # Get all valid script names (including external references)
        valid_scripts = {entry.get('script_name') for entry in self.tracking_data if isinstance(entry, dict) and 'script_name' in entry}

        # Add common external references that are allowed
        valid_external_refs = {
            'external/tax_rules_api.py',
            'external/bank_feed_api.py',
            # Add more as needed
        }

        for i, entry in enumerate(self.tracking_data):
            if not isinstance(entry, dict):
                continue

            script_name = entry.get('script_name', 'unknown')
            interacts_with = entry.get('interacts_with', [])

            for dep in interacts_with:
                if not isinstance(dep, str):
                    self.errors.append(f"Entry {i} ({script_name}) has non-string dependency: {dep}")
                    continue

                # Allow external references
                if dep.startswith('external/'):
                    if dep not in valid_external_refs:
                        self.warnings.append(f"Entry {i} ({script_name}) references unknown external dependency: {dep}")
                    continue

                # Check if it's a valid relative path
                if not dep.startswith(('src/', 'calculation_engine/', 'shared/', 'tests/', 'alembic/')):
                    self.warnings.append(f"Entry {i} ({script_name}) dependency '{dep}' doesn't follow expected path patterns")
                    continue

                # For now, just warn about paths we can't validate (would need more complex path resolution)
                # In a full implementation, we'd resolve relative paths from the script location


def main():
    """Main entry point for validation script."""
    # Change to project root if running from elsewhere
    script_dir = Path(__file__).parent
    if script_dir.name == 'backend':
        os.chdir(script_dir.parent)
    elif script_dir.parent.name == 'backend':
        os.chdir(script_dir.parent.parent)

    validator = PythonRuleValidator()
    success = validator.validate()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

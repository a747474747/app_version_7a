#!/usr/bin/env python3
"""
Script Tracking Entry Generator

Automatically generates tracking entries for Python scripts to comply with
the Python Scripts Rule (.cursor/rules/python-scripts.mdc).

Usage:
    python3 create_script_tracking.py <script_path> [--description "Description"] [--engine engine_name]
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class TrackingEntryGenerator:
    """Generates tracking entries for Python scripts."""

    def __init__(self, backend_root: Path = None):
        if backend_root is None:
            script_dir = Path(__file__).parent
            if script_dir.name == 'backend':
                self.backend_root = script_dir
            else:
                self.backend_root = script_dir / 'backend'
        else:
            self.backend_root = Path(backend_root)

        self.tracking_file = self.backend_root / 'script_tracking.json'

    def generate_entry(self, script_path: str, description: str = None, engine: str = None) -> Dict:
        """Generate a tracking entry for a script."""

        script_path = Path(script_path)

        # Validate script exists
        if not script_path.exists():
            raise ValueError(f"Script not found: {script_path}")

        # Validate script is in allowed location (backend or frontend)
        script_str = str(script_path)
        if not (script_str.startswith(str(self.backend_root)) or script_str.startswith(str(self.backend_root.parent / 'frontend'))):
            raise ValueError(f"Script must be within backend or frontend directory: {script_path}")

        # Get relative path
        if script_str.startswith(str(self.backend_root)):
            relative_path = script_path.relative_to(self.backend_root)
        elif script_str.startswith(str(self.backend_root.parent / 'frontend')):
            # For frontend scripts, keep the full frontend/ path
            relative_path = script_path.relative_to(self.backend_root.parent)
        else:
            raise ValueError(f"Unable to determine relative path for: {script_path}")

        # Auto-detect engine from path
        if engine is None:
            engine = self._detect_engine_from_path(relative_path)

        # Auto-generate description if not provided
        if description is None:
            description = self._generate_description(script_path, relative_path)

        # Analyze dependencies
        interacts_with = self._analyze_dependencies(script_path, relative_path)

        # Create entry
        entry = {
            "script_name": str(relative_path),
            "description": description[:100],  # Limit to 100 chars
            "created_date": datetime.now().strftime('%Y-%m-%d'),
            "created_timezone": "Australia/Brisbane",
            "engine": engine,
            "interacts_with": interacts_with,
            "purpose": self._generate_purpose(script_path, relative_path, engine)
        }

        return entry

    def add_entry_to_tracking_file(self, entry: Dict):
        """Add entry to the tracking file."""

        # Load existing tracking data
        if self.tracking_file.exists():
            try:
                with open(self.tracking_file, 'r') as f:
                    tracking_data = json.load(f)
            except json.JSONDecodeError:
                print("Warning: Tracking file is not valid JSON, creating new one")
                tracking_data = []
        else:
            tracking_data = []

        # Check for duplicates
        existing_scripts = {item.get('script_name') for item in tracking_data if isinstance(item, dict)}
        if entry['script_name'] in existing_scripts:
            raise ValueError(f"Script '{entry['script_name']}' already has a tracking entry")

        # Add new entry
        tracking_data.append(entry)

        # Write back to file
        with open(self.tracking_file, 'w') as f:
            json.dump(tracking_data, f, indent=2)

        print(f"✅ Added tracking entry for {entry['script_name']}")

    def _detect_engine_from_path(self, relative_path: Path) -> str:
        """Detect engine from script path."""

        path_str = str(relative_path)

        # Frontend scripts
        if path_str.startswith('frontend/'):
            return 'frontend'

        # Backend scripts
        if path_str.startswith('calculation_engine/'):
            return 'calculation_engine'
        elif path_str.startswith('llm_orchestrator/') or path_str.startswith('src/engines/llm/'):
            return 'llm_orchestrator'
        elif path_str.startswith('strategy_engine/') or path_str.startswith('src/engines/strategy/'):
            return 'strategy_engine'
        elif path_str.startswith('advice_engine/') or path_str.startswith('src/engines/advice/'):
            return 'advice_engine'
        elif path_str.startswith(('shared/', 'src/', 'tests/', 'alembic/')):
            return 'shared'
        else:
            return 'shared'  # Default

    def _generate_description(self, script_path: Path, relative_path: Path) -> str:
        """Generate a description for the script."""

        # Try to read the file and extract docstring or class/function names
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read(1000)  # Read first 1000 chars

            # Look for module docstring
            lines = content.split('\n')[:10]  # First 10 lines
            in_docstring = False
            docstring_lines = []

            for line in lines:
                line = line.strip()
                if line.startswith('"""') or line.startswith("'''"):
                    if in_docstring:
                        break
                    in_docstring = True
                    # Remove opening quotes
                    line = line[3:].strip()
                    if line:
                        docstring_lines.append(line)
                elif in_docstring and (line.endswith('"""') or line.endswith("'''")):
                    # Remove closing quotes
                    line = line[:-3].strip()
                    if line:
                        docstring_lines.append(line)
                    break
                elif in_docstring:
                    docstring_lines.append(line)

            if docstring_lines:
                return docstring_lines[0][:100]

        except Exception:
            pass

        # Fallback descriptions based on file type/location
        filename = script_path.name
        dirname = relative_path.parent.name if relative_path.parent.name != '.' else ''

        if filename.endswith('_test.py') or dirname == 'tests':
            return f"Test script for {dirname or 'backend'} functionality"
        elif 'router' in filename or 'api' in filename:
            return f"API endpoints for {dirname or 'backend'} services"
        elif 'service' in filename:
            return f"Business logic service for {dirname or 'backend'} operations"
        elif 'model' in filename:
            return f"Database models for {dirname or 'backend'} entities"
        elif 'config' in filename:
            return f"Configuration settings for {dirname or 'backend'}"
        elif 'util' in filename or 'helper' in filename:
            return f"Utility functions for {dirname or 'backend'} operations"
        else:
            return f"Python script for {dirname or 'backend'} functionality"

    def _analyze_dependencies(self, script_path: Path, relative_path: Path) -> List[str]:
        """Analyze script dependencies."""

        dependencies = []

        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Look for import statements
            lines = content.split('\n')
            for line in lines:
                line = line.strip()

                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue

                # Handle different import types
                if line.startswith('from ') and 'import' in line:
                    # from module import item
                    parts = line.split()
                    if len(parts) >= 4 and parts[0] == 'from':
                        module = parts[1]
                        if module.startswith('.'):
                            # Relative import - try to resolve
                            dependencies.extend(self._resolve_relative_import(module, relative_path))
                        else:
                            # Absolute import within backend
                            dependencies.extend(self._resolve_absolute_import(module))

                elif line.startswith('import '):
                    # import module
                    parts = line.split()
                    if len(parts) >= 2:
                        module = parts[1].split('.')[0]  # Get root module
                        dependencies.extend(self._resolve_absolute_import(module))

        except Exception as e:
            print(f"Warning: Could not analyze dependencies for {script_path}: {e}")

        # Remove duplicates and sort
        return sorted(list(set(dependencies)))

    def _resolve_relative_import(self, module: str, current_path: Path) -> List[str]:
        """Resolve relative imports to script paths."""
        # This is a simplified implementation
        # A full implementation would need proper Python import resolution

        dependencies = []

        # Convert relative import to path
        if module.startswith('..'):
            # Go up directories
            up_levels = module.count('..')
            remaining = module[up_levels * 3:]  # Remove the .. and dots

            # Navigate up
            target_path = current_path
            for _ in range(up_levels):
                target_path = target_path.parent

            # Add remaining path
            if remaining:
                remaining = remaining.lstrip('.')
                target_path = target_path / remaining.replace('.', '/')
            target_path = target_path.with_suffix('.py')

            if target_path.exists():
                # Convert to relative path from backend
                try:
                    rel_path = target_path.relative_to(self.backend_root)
                    dependencies.append(str(rel_path))
                except ValueError:
                    pass

        return dependencies

    def _resolve_absolute_import(self, module: str) -> List[str]:
        """Resolve absolute imports within backend."""

        # Map common modules to script paths
        module_mappings = {
            'engines.calculation': ['calculation_engine/__init__.py'],
            'engines.calculation.registry': ['calculation_engine/registry.py'],
            'engines.calculation.domains': ['calculation_engine/domains/__init__.py'],
            'models': ['src/models/__init__.py'],
            'services': ['src/services/__init__.py'],
            'routers': ['src/routers/__init__.py'],
            'auth': ['src/auth/__init__.py'],
            'config': ['src/config/__init__.py'],
        }

        if module in module_mappings:
            return module_mappings[module]

        # Try to find the module file
        possible_paths = [
            f"src/{module.replace('.', '/')}.py",
            f"src/{module.replace('.', '/')}/__init__.py",
            f"{module.replace('.', '/')}.py",
            f"{module.replace('.', '/')}/__init__.py",
        ]

        for path_str in possible_paths:
            path = self.backend_root / path_str
            if path.exists():
                try:
                    rel_path = path.relative_to(self.backend_root)
                    return [str(rel_path)]
                except ValueError:
                    pass

        return []

    def _generate_purpose(self, script_path: Path, relative_path: Path, engine: str) -> str:
        """Generate a detailed purpose description."""

        filename = script_path.name
        dirname = str(relative_path.parent)

        # Engine-specific purposes
        if engine == 'calculation_engine':
            if 'domain' in dirname:
                return f"Implements calculation logic for {filename.replace('.py', '').replace('_', ' ')} in the financial calculation engine"
            elif 'registry' in filename:
                return "Maintains registry of all CAL-* calculation functions and provides access by CAL-ID"
            elif 'projection' in filename:
                return "Executes multi-year financial projections using registered calculation functions"
            else:
                return f"Core calculation engine functionality for {filename.replace('.py', '').replace('_', ' ')}"

        elif engine == 'llm_orchestrator':
            return f"LLM orchestration logic for {filename.replace('.py', '').replace('_', ' ')}"

        elif engine == 'strategy_engine':
            return f"Investment strategy optimization logic for {filename.replace('.py', '').replace('_', ' ')}"

        elif engine == 'advice_engine':
            return f"Financial advice generation logic for {filename.replace('.py', '').replace('_', ' ')}"

        else:  # shared
            if 'router' in filename or 'api' in filename:
                return f"API endpoints and routing for {dirname} services"
            elif 'service' in filename:
                return f"Business logic and data operations for {dirname} functionality"
            elif 'model' in filename:
                return f"Database models and schemas for {dirname} entities"
            elif 'config' in filename:
                return f"Configuration management for {dirname} settings"
            elif 'middleware' in filename:
                return f"Request/response middleware for {dirname} operations"
            else:
                return f"Shared utility and support functionality for {filename.replace('.py', '').replace('_', ' ')}"


def main():
    parser = argparse.ArgumentParser(description='Generate script tracking entry')
    parser.add_argument('script_path', help='Path to the Python script')
    parser.add_argument('--description', '-d', help='Custom description (auto-generated if not provided)')
    parser.add_argument('--engine', '-e', help='Engine type (auto-detected if not provided)')
    parser.add_argument('--add-to-tracking', '-a', action='store_true',
                       help='Add the entry to script_tracking.json')

    args = parser.parse_args()

    generator = TrackingEntryGenerator()

    try:
        entry = generator.generate_entry(
            args.script_path,
            description=args.description,
            engine=args.engine
        )

        print("📝 Generated tracking entry:")
        print(json.dumps(entry, indent=2))

        if args.add_to_tracking:
            generator.add_entry_to_tracking_file(entry)
        else:
            print("\n💡 Use --add-to-tracking to add this entry to the tracking file")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

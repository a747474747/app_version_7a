#!/usr/bin/env python3
"""
Simple test script to check if the minimal server can import.
"""

import sys
import os

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), '..')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

try:
    from shared.minimal_server import app
    print("SUCCESS: Server imports successfully!")
    print(f"Routes: {len(app.routes)}")
    print(f"Title: {app.title}")

    # Test if we can access calculation functions
    try:
        from shared.minimal_server import CALC_ENGINE_AVAILABLE
        print(f"Calc Engine Available: {CALC_ENGINE_AVAILABLE}")
        if CALC_ENGINE_AVAILABLE:
            from shared.minimal_server import get_registered_calculations
            print(f"Functions: {len(get_registered_calculations())}")
    except ImportError as e:
        print(f"Calc engine import failed: {e}")

except ImportError as e:
    print(f"Server import failed: {e}")
    sys.exit(1)

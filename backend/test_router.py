#!/usr/bin/env python3
"""
Test script to check router imports and registration.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    print("Testing router imports...")

    # Test modes router import
    from src.routers.modes import router as modes_router
    print("Modes router imported with {} routes".format(len(modes_router.routes)))

    # Test API router import
    from src.routers.api import router as api_router
    print("API router imported with {} routes".format(len(api_router.routes)))

    # Check modes routes
    modes_routes = [route for route in api_router.routes if hasattr(route, 'path') and 'modes' in str(route.path)]
    print("Modes routes in API router: {}".format(len(modes_routes)))

    for route in modes_routes:
        print("  - {} {}".format(route.methods, route.path))

    print("\nAll routers imported successfully!")

except Exception as e:
    print("Error: {}".format(e))
    import traceback
    traceback.print_exc()

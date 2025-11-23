#!/usr/bin/env python3
"""
Simple script to start the server for testing.
"""

import sys
import os
from pathlib import Path

if __name__ == '__main__':
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)

    # Add src to path
    sys.path.insert(0, 'src')

    # Load environment variables from project root
    try:
        from dotenv import load_dotenv
        project_root = Path(__file__).parent.parent
        load_dotenv(project_root / '.env')
        load_dotenv(project_root / '.env.local')
        print("Environment variables loaded from project root")
    except ImportError:
        print("python-dotenv not available, using system environment")

    # Verify Clerk keys
    clerk_secret = os.getenv('CLERK_SECRET_KEY')
    clerk_pub = os.getenv('NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY') or os.getenv('CLERK_PUBLISHABLE_KEY')
    if clerk_secret and clerk_secret.startswith('sk_test_') and clerk_pub and clerk_pub.startswith('pk_test_'):
        print("SUCCESS: Clerk authentication ENABLED")
    else:
        print("WARNING: Clerk authentication DISABLED (dummy mode)")

    try:
        # Import as module from src package
        from src.main import app
        import uvicorn

        print("Starting server on http://localhost:8000 (without reload to avoid Windows multiprocessing issues)")
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, log_level="info")

    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()

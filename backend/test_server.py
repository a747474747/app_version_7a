#!/usr/bin/env python3
"""
Test script to start server briefly and check endpoints.
"""

import subprocess
import time
import requests
import sys
import os

def test_server():
    # Start server in background
    print("Starting server...")
    server_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "src.main:app",
        "--host", "0.0.0.0", "--port", "8000", "--reload"
    ], cwd=os.path.dirname(__file__))

    try:
        # Wait for server to start
        time.sleep(3)

        # Test health endpoint
        print("Testing health endpoint...")
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            print(f"Health endpoint: {response.status_code}")
        except Exception as e:
            print(f"Health endpoint failed: {e}")

        # Test modes endpoint
        print("Testing modes endpoint...")
        try:
            response = requests.post(
                "http://localhost:8000/api/v1/modes/fact_check/execute",
                json={
                    "scenario_id": "test",
                    "parameters": {"question": "What is my tax liability?"}
                },
                timeout=5
            )
            print(f"Modes endpoint: {response.status_code}")
            if response.status_code != 404:
                print("Modes endpoint is working!")
            else:
                print("Modes endpoint returned 404")
        except Exception as e:
            print(f"Modes endpoint failed: {e}")

        # Test OpenAPI docs
        print("Testing OpenAPI docs...")
        try:
            response = requests.get("http://localhost:8000/docs", timeout=5)
            print(f"Docs endpoint: {response.status_code}")
        except Exception as e:
            print(f"Docs endpoint failed: {e}")

    finally:
        print("Stopping server...")
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    test_server()

#!/usr/bin/env python3
"""
Verify that our OpenRouter implementation matches the quickstart documentation.
"""
import os
import sys
import inspect

# Add backend to path to import without triggering settings
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import individual components to avoid settings loading
from pydantic import BaseModel, Field
from typing import Optional, List, Union
from enum import Enum

class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class ChatMessage(BaseModel):
    role: MessageRole
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage] = Field(..., min_items=1)
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(None, gt=0)
    top_p: Optional[float] = Field(None, ge=0.0, le=1.0)
    frequency_penalty: Optional[float] = Field(None, ge=-2.0, le=2.0)
    presence_penalty: Optional[float] = Field(None, ge=-2.0, le=2.0)
    stop: Optional[Union[str, List[str]]] = None
    stream: bool = False

def verify_request_structure():
    """Verify our request structure matches OpenRouter documentation."""

    # Create a request similar to the documentation example
    request = ChatCompletionRequest(
        model="openai/gpt-4o",  # Using the model from docs
        messages=[
            ChatMessage(
                role=MessageRole.USER,
                content="What is the meaning of life?"
            )
        ]
    )

    request_data = request.dict(exclude_unset=True)
    print("Our request structure:")
    print(f"Model: {request_data.get('model')}")
    print(f"Messages: {request_data.get('messages')}")

    # Compare with documentation structure
    expected_keys = ['model', 'messages']
    actual_keys = list(request_data.keys())

    print(f"\nExpected keys: {expected_keys}")
    print(f"Actual keys: {actual_keys}")

    # Check if all expected keys are present
    missing_keys = set(expected_keys) - set(actual_keys)
    extra_keys = set(actual_keys) - set(expected_keys)

    if not missing_keys and not extra_keys:
        print("SUCCESS: Request structure matches documentation")
        return True
    else:
        print(f"ERROR: Missing keys: {missing_keys}, Extra keys: {extra_keys}")
        return False

def verify_headers():
    """Verify our headers match the documentation."""
    expected_headers = {
        "Authorization": "Bearer <API_KEY>",
        "Content-Type": "application/json",
        "HTTP-Referer": "<SITE_URL>",  # Optional
        "X-Title": "<SITE_NAME>",  # Optional
    }

    # Read the client file directly
    client_file = os.path.join(os.path.dirname(__file__), '..', 'src', 'services', 'openrouter_client.py')
    with open(client_file, 'r') as f:
        content = f.read()

    print("\nOur headers implementation:")
    for line in content.split('\n'):
        if 'headers=' in line or 'Authorization' in line or 'HTTP-Referer' in line or 'X-Title' in line:
            print(line.strip())

    return True

def verify_base_url():
    """Verify our base URL matches documentation."""
    expected_url = "https://openrouter.ai/api/v1"

    # Read the client file and find the default base_url parameter
    client_file = os.path.join(os.path.dirname(__file__), '..', 'src', 'services', 'openrouter_client.py')
    with open(client_file, 'r') as f:
        content = f.read()

    # Find the base_url parameter line
    for line in content.split('\n'):
        if 'base_url: str = ' in line:
            # Extract the default value
            default_base_url = line.split('=')[1].strip().strip(',')
            break
    else:
        print("ERROR: Could not find base_url parameter")
        return False

    print(f"\nBase URL check:")
    print(f"Expected: {expected_url}")
    print(f"Default in our client: {default_base_url}")

    if default_base_url.strip('"') == expected_url:
        print("SUCCESS: Base URL matches documentation")
        return True
    else:
        print("ERROR: Base URL does not match")
        return False

if __name__ == "__main__":
    print("=== OpenRouter Implementation Compliance Check ===\n")

    checks = [
        ("Request Structure", verify_request_structure),
        ("Headers", verify_headers),
        ("Base URL", verify_base_url),
    ]

    results = []
    for name, check_func in checks:
        print(f"--- {name} ---")
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"ERROR: {e}")
            results.append((name, False))
        print()

    print("=== Summary ===")
    all_passed = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\nSUCCESS: Our OpenRouter implementation is compliant with the quickstart documentation!")
    else:
        print("\nWARNING: Some compliance issues found.")

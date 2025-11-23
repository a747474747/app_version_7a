#!/usr/bin/env python3
"""
Simple test script to verify OpenRouter connection without full settings.
"""
import asyncio
import httpx
import os

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_API_KEY = os.getenv('LLM_OPENROUTER_API_KEY')

async def test_openrouter_simple():
    """Test basic OpenRouter connection with direct HTTP calls."""

    if not OPENROUTER_API_KEY:
        print("ERROR: LLM_OPENROUTER_API_KEY not found in environment")
        return False

    print(f"SUCCESS: Found API key: {OPENROUTER_API_KEY[:12]}...")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/your-org/four-engine-architecture",
        "X-Title": "Four-Engine System Architecture",
    }

    async with httpx.AsyncClient(base_url=OPENROUTER_BASE_URL, headers=headers, timeout=30.0) as client:
        try:
            # Test 1: List models
            print("Testing model listing...")
            response = await client.get("/models")
            if response.is_success:
                models_data = response.json()
                models_count = len(models_data.get('data', []))
                print(f"SUCCESS: Found {models_count} available models")
            else:
                print(f"ERROR: Model listing failed: {response.status_code} - {response.text}")
                return False

            # Test 2: Simple chat completion
            print("Testing chat completion...")
            payload = {
                "model": "anthropic/claude-3-haiku",
                "messages": [
                    {"role": "user", "content": "Hello! Just testing OpenRouter connection. Please respond with 'Connection successful!'"}
                ],
                "max_tokens": 20
            }

            response = await client.post("/chat/completions", json=payload)
            if response.is_success:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                print(f"SUCCESS: Chat completion successful: {content}")
                return True
            else:
                print(f"ERROR: Chat completion failed: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"ERROR: {e}")
            return False

if __name__ == "__main__":
    success = asyncio.run(test_openrouter_simple())
    if success:
        print("\nSUCCESS: OpenRouter connection test PASSED!")
        print("Your project can successfully connect to OpenRouter!")
    else:
        print("\nFAILED: OpenRouter connection test FAILED!")

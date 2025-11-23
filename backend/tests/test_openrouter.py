#!/usr/bin/env python3
"""
Simple test script to verify OpenRouter connection.
"""
import asyncio
import os
from backend.src.services.openrouter_client import OpenRouterClient, ChatMessage, ChatCompletionRequest, MessageRole

async def test_openrouter_connection():
    """Test basic OpenRouter connection."""
    api_key = os.getenv('LLM_OPENROUTER_API_KEY')
    if not api_key:
        print("ERROR: LLM_OPENROUTER_API_KEY not found in environment")
        return False

    print(f"SUCCESS: Found API key: {api_key[:12]}...")

    try:
        async with OpenRouterClient(api_key=api_key) as client:
            print("SUCCESS: OpenRouter client initialized")

            # Test listing models
            print("Testing model listing...")
            models = await client.list_models()
            print(f"SUCCESS: Found {len(models.get('data', []))} available models")

            # Test a simple chat completion
            print("Testing chat completion...")
            request = ChatCompletionRequest(
                model="anthropic/claude-3-haiku",
                messages=[
                    ChatMessage(role=MessageRole.USER, content="Hello, can you confirm this is working?")
                ],
                max_tokens=50
            )

            response = await client.create_chat_completion(request)
            print(f"SUCCESS: Chat completion successful: {response.choices[0].message.content[:50]}...")

            return True

    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_openrouter_connection())
    if success:
        print("\nSUCCESS: OpenRouter connection test PASSED!")
    else:
        print("\nFAILED: OpenRouter connection test FAILED!")

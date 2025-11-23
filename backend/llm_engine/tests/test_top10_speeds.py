#!/usr/bin/env python3
"""
Test response speeds for top 10 curated models from OpenRouter.
"""
import asyncio
import time
import os
import json
from typing import List, Dict, Any

from backend.src.services.openrouter_client import OpenRouterClient
from backend.src.services.openrouter_client import ChatMessage, MessageRole

# Top 10 models from curated list
TOP_10_MODELS = [
    "deepseek/deepseek-r1",
    "deepseek/deepseek-r1-0528",
    "moonshotai/kimi-linear-48b-a3b-instruct",
    "minimax/minimax-m1",
    "qwen/qwen-turbo",
    "qwen/qwen-plus-2025-07-28",
    "deepseek/deepseek-v3.2-exp",
    "moonshotai/kimi-k2-thinking",
    "qwen/qwen3-235b-a22b-thinking-2507",
    "microsoft/mai-ds-r1"
]

TEST_PROMPT = "Hello! Just testing response speed. Count to 3."

async def test_model_speed(model_id: str, client: OpenRouterClient) -> Dict[str, Any]:
    """Test response speed for a single model."""
    try:
        start_time = time.time()

        messages = [ChatMessage(role=MessageRole.USER, content=TEST_PROMPT)]

        response = await client.create_chat_completion(
            model=model_id,
            messages=messages,
            max_tokens=10,  # Very short response
            temperature=0.1
        )

        end_time = time.time()
        response_time = end_time - start_time

        content = response.choices[0].message.content if response.choices else ""
        tokens_used = response.usage.total_tokens if response.usage else 0

        return {
            "model": model_id,
            "success": True,
            "response_time_seconds": round(response_time, 3),
            "tokens_used": tokens_used,
            "response_preview": content[:50] + "..." if len(content) > 50 else content,
            "error": None
        }

    except Exception as e:
        return {
            "model": model_id,
            "success": False,
            "response_time_seconds": None,
            "tokens_used": None,
            "response_preview": None,
            "error": str(e)
        }

async def main():
    """Test all top 10 models."""
    print("🧪 Testing Response Speeds for Top 10 Curated Models")
    print("=" * 60)
    print(f"Test prompt: '{TEST_PROMPT}'")
    print("Max tokens: 10, Temperature: 0.1")
    print()

    # Check API key
    api_key = os.getenv('LLM_OPENROUTER_API_KEY')
    if not api_key:
        print("❌ ERROR: LLM_OPENROUTER_API_KEY not found in environment")
        print("Please set your OpenRouter API key:")
        print("export LLM_OPENROUTER_API_KEY='your-api-key-here'")
        return

    print(f"✅ API key found: {api_key[:12]}...")
    print()

    # Initialize client
    client = OpenRouterClient()

    results = []

    for i, model_id in enumerate(TOP_10_MODELS, 1):
        print(f"Testing {i}/10: {model_id}")

        result = await test_model_speed(model_id, client)
        results.append(result)

        if result["success"]:
            print(f"  ✅ {result['response_time_seconds']}s, {result['tokens_used']} tokens")
            print(f"     Preview: {result['response_preview']}")
        else:
            print(f"  ❌ Failed: {result['error']}")
        print()

    # Summary
    print("📊 SUMMARY")
    print("-" * 40)

    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    if successful:
        times = [r["response_time_seconds"] for r in successful]
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)

        print(f"✅ Successful tests: {len(successful)}/10")
        print(f"⏱️  Average response time: {avg_time:.3f}s")
        print(f"🏃 Fastest: {min_time:.3f}s")
        print(f"🐌 Slowest: {max_time:.3f}s")
        print()

        print("🏆 FASTEST MODELS:")
        fastest_sorted = sorted(successful, key=lambda x: x["response_time_seconds"])
        for i, result in enumerate(fastest_sorted[:5], 1):
            print(f"  {i}. {result['model']}: {result['response_time_seconds']}s")

    if failed:
        print(f"❌ Failed tests: {len(failed)}/10")
        for result in failed:
            print(f"  - {result['model']}: {result['error']}")

if __name__ == "__main__":
    asyncio.run(main())

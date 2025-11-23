#!/usr/bin/env python3
"""
Simple test for top 10 curated models response speeds.
Bypasses the full settings system for easier testing.
"""
import asyncio
import time
import os
import httpx
import json

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

async def test_model_speed_simple(model_id: str, api_key: str) -> dict:
    """Test response speed using direct HTTP calls."""
    try:
        start_time = time.time()

        payload = {
            "model": model_id,
            "messages": [{"role": "user", "content": TEST_PROMPT}],
            "max_tokens": 10,
            "temperature": 0.1
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/your-org/four-engine-architecture",
            "X-Title": "Four-Engine System Architecture"
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json=payload,
                headers=headers
            )

            if response.status_code == 200:
                data = response.json()
                end_time = time.time()
                response_time = end_time - start_time

                content = data["choices"][0]["message"]["content"] if data.get("choices") else ""
                tokens_used = data.get("usage", {}).get("total_tokens", 0)

                return {
                    "model": model_id,
                    "success": True,
                    "response_time_seconds": round(response_time, 3),
                    "tokens_used": tokens_used,
                    "response_preview": content[:50] + "..." if len(content) > 50 else content,
                    "error": None
                }
            else:
                return {
                    "model": model_id,
                    "success": False,
                    "response_time_seconds": None,
                    "tokens_used": None,
                    "response_preview": None,
                    "error": f"HTTP {response.status_code}: {response.text}"
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
    """Test all top 10 models in parallel."""
    print("Testing Response Speeds for Top 10 Curated Models (PARALLEL)")
    print("=" * 60)
    print(f"Test prompt: '{TEST_PROMPT}'")
    print("Max tokens: 10, Temperature: 0.1")
    print("All tests run concurrently for accurate speed comparison")
    print()

    # Check API key
    api_key = os.getenv('LLM_OPENROUTER_API_KEY')
    if not api_key:
        print("ERROR: LLM_OPENROUTER_API_KEY not found in environment")
        print()
        print("To run this test:")
        print("1. Get your OpenRouter API key from https://openrouter.ai/keys")
        print("2. Set the environment variable:")
        print("   $env:LLM_OPENROUTER_API_KEY = 'your-api-key-here'")
        print("3. Run: python test_top10_speeds_simple.py")
        print()
        print("WARNING: This will make 10 concurrent API calls and cost ~$0.001-0.01")
        return

    print(f"API key found: {api_key[:12]}...")
    print("This will make 10 concurrent API calls. Estimated cost: $0.001-0.01")
    print("Proceeding with test...")
    print()

    print("Starting parallel tests for all 10 models...")
    print()

    # Run all tests concurrently
    start_time = time.time()
    tasks = [test_model_speed_simple(model_id, api_key) for model_id in TOP_10_MODELS]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    total_time = time.time() - start_time

    # Process results
    processed_results = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            # Handle exceptions from gather
            processed_results.append({
                "model": TOP_10_MODELS[i],
                "success": False,
                "response_time_seconds": None,
                "tokens_used": None,
                "response_preview": None,
                "error": str(result)
            })
        else:
            processed_results.append(result)

    # Sort results by response time for display
    successful = [r for r in processed_results if r["success"]]
    failed = [r for r in processed_results if not r["success"]]

    # Display results in order of completion
    print("RESULTS (in order of completion):")
    print("-" * 50)

    for i, result in enumerate(processed_results, 1):
        model_name = result["model"].split("/")[-1]  # Short name for display
        if result["success"]:
            print(f"{i:2d}. {model_name:<30} | {result['response_time_seconds']:>5.3f}s | {result['tokens_used']:>3d} tokens")
        else:
            print(f"{i:2d}. {model_name:<30} | FAILED")

    print()
    print("DETAILED RESULTS:")
    print("-" * 50)

    for result in processed_results:
        print(f"Model: {result['model']}")
        if result["success"]:
            print(f"  Time: {result['response_time_seconds']:.3f}s")
            print(f"  Tokens: {result['tokens_used']}")
            print(f"  Preview: {result['response_preview']}")
        else:
            print(f"  Error: {result['error']}")
        print()

    # Summary
    print("SUMMARY")
    print("-" * 40)
    print(f"Total test time: {total_time:.3f}s")

    if successful:
        times = [r["response_time_seconds"] for r in successful]
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)

        print(f"Successful tests: {len(successful)}/10")
        print(f"Average response time: {avg_time:.3f}s")
        print(f"Fastest model: {min_time:.3f}s")
        print(f"Slowest model: {max_time:.3f}s")
        print()

        print("FASTEST MODELS (by response time):")
        fastest_sorted = sorted(successful, key=lambda x: x["response_time_seconds"])
        for i, result in enumerate(fastest_sorted, 1):
            model_name = result["model"].split("/")[-1]
            print(f"  {i}. {model_name}: {result['response_time_seconds']:.3f}s")

        print()
        print("TOKENS USED:")
        token_sorted = sorted(successful, key=lambda x: x["tokens_used"])
        for i, result in enumerate(token_sorted, 1):
            model_name = result["model"].split("/")[-1]
            print(f"  {i}. {model_name}: {result['tokens_used']} tokens")

    if failed:
        print(f"Failed tests: {len(failed)}/10")
        for result in failed:
            model_name = result["model"].split("/")[-1]
            print(f"  - {model_name}: {result['error']}")

if __name__ == "__main__":
    asyncio.run(main())

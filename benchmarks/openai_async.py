"""
Async OpenAI API client for high-throughput contradiction detection.

This module provides async/await based OpenAI API calls with:
- Concurrent request pipelining (5-10x faster than sync)
- Semaphore-based rate limiting
- Exponential backoff retry logic
- Memory-efficient request batching
"""

import asyncio
import json
import time
from typing import List, Tuple, Optional, Dict, Any
import os

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False

__all__ = ["AsyncOpenAIClient", "run_async_benchmark"]


class AsyncOpenAIClient:
    """Async OpenAI client with concurrent request handling."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini", 
                 max_concurrent: int = 8, base_url: str = None):
        if not HTTPX_AVAILABLE:
            raise ImportError("Install httpx for async support: pip install httpx")
            
        self.api_key = (api_key or 
                       os.getenv("OPENAI_API_KEY") or 
                       "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")
        if not self.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY env var or pass api_key")
        
        # Auto-detect OpenRouter API
        if self.api_key.startswith("sk-or-"):
            self.base_url = base_url or "https://openrouter.ai/api/v1"
            # OpenRouter requires model prefix
            self.model = f"openai/{model}" if not model.startswith("openai/") else model
        else:
            self.base_url = base_url or "https://api.openai.com/v1"
            self.model = model
            
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        
        # HTTP client configuration
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            timeout=30.0
        )
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def detect_contradiction_async(self, text1: str, text2: str, 
                                       max_retries: int = 3) -> Tuple[bool, float, str, float]:
        """
        Async contradiction detection with retry logic.
        
        Returns:
            Tuple of (is_contradiction, confidence, reasoning, latency_ms)
        """
        prompt = f"""Analyze these two statements for logical contradiction:

Statement A: "{text1}"
Statement B: "{text2}"

Question: Do these statements contradict each other?

Respond with JSON only:
{{
    "contradiction": true/false,
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation"
}}"""

        async with self.semaphore:  # Rate limiting
            for attempt in range(max_retries):
                try:
                    start_time = time.perf_counter()
                    
                    response = await self.client.post(
                        "/chat/completions",
                        json={
                            "model": self.model,
                            "messages": [{"role": "user", "content": prompt}],
                            "temperature": 0.1,
                            "max_tokens": 200
                        }
                    )
                    
                    latency_ms = (time.perf_counter() - start_time) * 1000
                    
                    if response.status_code == 429:  # Rate limit
                        wait_time = 2 ** attempt
                        await asyncio.sleep(wait_time)
                        continue
                    
                    response.raise_for_status()
                    
                    content = response.json()["choices"][0]["message"]["content"].strip()
                    
                    # Parse JSON response
                    try:
                        result = json.loads(content)
                        return (
                            bool(result["contradiction"]),
                            float(result["confidence"]),
                            str(result["reasoning"]),
                            latency_ms
                        )
                    except (json.JSONDecodeError, KeyError) as e:
                        # Fallback parsing for malformed JSON
                        is_contra = "true" in content.lower() or "contradiction" in content.lower()
                        return is_contra, 0.5, f"Parsed from: {content[:100]}", latency_ms
                
                except httpx.HTTPStatusError as e:
                    if e.response.status_code == 429 and attempt < max_retries - 1:
                        wait_time = 2 ** attempt
                        await asyncio.sleep(wait_time)
                        continue
                    raise
                
                except (httpx.RequestError, asyncio.TimeoutError) as e:
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt
                        await asyncio.sleep(wait_time)
                        continue
                    raise
            
            # If all retries failed
            raise Exception(f"Failed after {max_retries} attempts")


async def run_async_benchmark(test_pairs: List[Tuple[str, str]], 
                            api_key: Optional[str] = None,
                            model: str = "gpt-4o-mini",
                            max_concurrent: int = 8) -> Dict[str, Any]:
    """
    Run async benchmark on a list of text pairs.
    
    Args:
        test_pairs: List of (text1, text2) tuples to test
        api_key: OpenAI API key
        model: Model to use
        max_concurrent: Maximum concurrent requests
    
    Returns:
        Dictionary with results and performance stats
    """
    print(f"🚀 Running async benchmark with {max_concurrent} concurrent requests")
    
    async with AsyncOpenAIClient(api_key, model, max_concurrent) as client:
        start_time = time.perf_counter()
        
        # Create tasks for all pairs
        tasks = [
            client.detect_contradiction_async(text1, text2)
            for text1, text2 in test_pairs
        ]
        
        # Run all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        total_time = time.perf_counter() - start_time
        
        # Process results
        successful_results = []
        failed_count = 0
        total_latency = 0
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                failed_count += 1
                print(f"  ❌ Pair {i} failed: {result}")
                # Add dummy result for failed requests
                successful_results.append({
                    "pair_id": i,
                    "text1": test_pairs[i][0],
                    "text2": test_pairs[i][1],
                    "contradiction": False,
                    "confidence": 0.0,
                    "reasoning": f"Failed: {result}",
                    "latency_ms": 0.0
                })
            else:
                is_contra, conf, reason, latency = result
                total_latency += latency
                successful_results.append({
                    "pair_id": i,
                    "text1": test_pairs[i][0],
                    "text2": test_pairs[i][1],
                    "contradiction": is_contra,
                    "confidence": conf,
                    "reasoning": reason,
                    "latency_ms": latency
                })
        
        # Calculate stats
        successful_count = len(test_pairs) - failed_count
        avg_latency = total_latency / successful_count if successful_count > 0 else 0
        
        return {
            "results": successful_results,
            "stats": {
                "total_time_s": round(total_time, 2),
                "avg_time_per_pair_ms": round((total_time / len(test_pairs)) * 1000, 2),
                "avg_api_latency_ms": round(avg_latency, 2),
                "contradictions_found": sum(1 for r in successful_results if r["contradiction"]),
                "avg_confidence": round(sum(r["confidence"] for r in successful_results) / len(test_pairs), 3),
                "successful_requests": successful_count,
                "failed_requests": failed_count,
                "max_concurrent": max_concurrent,
                "mode": "async"
            }
        }


def create_async_tasks(test_pairs: List[Tuple[str, str]], 
                      client: AsyncOpenAIClient) -> List[asyncio.Task]:
    """Create async tasks for a batch of test pairs."""
    return [
        asyncio.create_task(client.detect_contradiction_async(text1, text2))
        for text1, text2 in test_pairs
    ]


async def process_batch_async(batch_pairs: List[Tuple[str, str]], 
                            client: AsyncOpenAIClient) -> List[Dict]:
    """Process a batch of pairs asynchronously."""
    tasks = create_async_tasks(batch_pairs, client)
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    batch_results = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            batch_results.append({
                "contradiction": False,
                "confidence": 0.0,
                "reasoning": f"Error: {result}",
                "latency_ms": 0.0
            })
        else:
            is_contra, conf, reason, latency = result
            batch_results.append({
                "contradiction": is_contra,
                "confidence": conf,
                "reasoning": reason,
                "latency_ms": latency
            })
    
    return batch_results
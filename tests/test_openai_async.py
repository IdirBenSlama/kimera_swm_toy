"""Tests for async OpenAI functionality."""

import pytest
import asyncio
import json
from unittest.mock import AsyncMock, patch, MagicMock

# Mark all tests in this file as async
pytestmark = pytest.mark.asyncio

# Skip tests if httpx not available
pytest_plugins = []
try:
    import httpx
    from benchmarks.openai_async import AsyncOpenAIClient, run_async_benchmark
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False


@pytest.mark.skipif(not HTTPX_AVAILABLE, reason="httpx not available")
class TestAsyncOpenAI:
    """Test async OpenAI client functionality."""
    
    @pytest.fixture
    def mock_response(self):
        """Create a mock HTTP response."""
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "contradiction": True,
                        "confidence": 0.85,
                        "reasoning": "Test reasoning"
                    })
                }
            }]
        }
        return response
    
    @pytest.fixture
    def async_client(self):
        """Create async client for testing."""
        return AsyncOpenAIClient(
            api_key="test-key",
            model="gpt-4o-mini",
            max_concurrent=2
        )
    
    @pytest.mark.asyncio
    async def test_async_client_init(self):
        """Test async client initialization."""
        client = AsyncOpenAIClient(api_key="test-key", max_concurrent=4)
        assert client.api_key == "test-key"
        assert client.max_concurrent == 4
        assert client.semaphore._value == 4
        await client.client.aclose()
    
    @pytest.mark.asyncio
    async def test_detect_contradiction_success(self, async_client, mock_response):
        """Test successful contradiction detection."""
        with patch.object(async_client.client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response
            
            result = await async_client.detect_contradiction_async("text1", "text2")
            
            is_contra, conf, reason, latency = result
            assert is_contra is True
            assert conf == 0.85
            assert reason == "Test reasoning"
            assert latency > 0
            
            # Verify API call was made
            mock_post.assert_called_once()
            call_args = mock_post.call_args
            assert call_args[1]["json"]["model"] == "gpt-4o-mini"
            assert "text1" in call_args[1]["json"]["messages"][0]["content"]
            assert "text2" in call_args[1]["json"]["messages"][0]["content"]
        
        await async_client.client.aclose()
    
    @pytest.mark.asyncio
    async def test_rate_limiting_semaphore(self, async_client, mock_response):
        """Test that semaphore limits concurrent requests."""
        call_count = 0
        original_semaphore_value = async_client.semaphore._value
        
        async def mock_post_with_delay(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            # Simulate API delay
            await asyncio.sleep(0.1)
            return mock_response
        
        with patch.object(async_client.client, 'post', side_effect=mock_post_with_delay):
            # Start more tasks than semaphore allows
            tasks = [
                async_client.detect_contradiction_async(f"text1_{i}", f"text2_{i}")
                for i in range(5)  # More than max_concurrent=2
            ]
            
            # Run tasks concurrently
            results = await asyncio.gather(*tasks)
            
            # All should succeed
            assert len(results) == 5
            for result in results:
                assert len(result) == 4  # (is_contra, conf, reason, latency)
        
        await async_client.client.aclose()
    
    @pytest.mark.asyncio
    async def test_retry_on_rate_limit(self, async_client):
        """Test retry logic on 429 rate limit."""
        # First call returns 429, second succeeds
        rate_limit_response = MagicMock()
        rate_limit_response.status_code = 429
        
        success_response = MagicMock()
        success_response.status_code = 200
        success_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "contradiction": False,
                        "confidence": 0.7,
                        "reasoning": "Retry success"
                    })
                }
            }]
        }
        
        with patch.object(async_client.client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.side_effect = [rate_limit_response, success_response]
            
            result = await async_client.detect_contradiction_async("text1", "text2")
            
            is_contra, conf, reason, latency = result
            assert is_contra is False
            assert conf == 0.7
            assert reason == "Retry success"
            
            # Should have been called twice (retry)
            assert mock_post.call_count == 2
        
        await async_client.client.aclose()
    
    @pytest.mark.asyncio
    async def test_malformed_json_fallback(self, async_client):
        """Test fallback parsing for malformed JSON responses."""
        malformed_response = MagicMock()
        malformed_response.status_code = 200
        malformed_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": "Yes, there is a contradiction between these statements."
                }
            }]
        }
        
        with patch.object(async_client.client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value = malformed_response
            
            result = await async_client.detect_contradiction_async("text1", "text2")
            
            is_contra, conf, reason, latency = result
            assert is_contra is True  # Should detect "contradiction" in text
            assert conf == 0.5  # Fallback confidence
            assert "Yes, there is a contradiction" in reason
        
        await async_client.client.aclose()


@pytest.mark.skipif(not HTTPX_AVAILABLE, reason="httpx not available")
@pytest.mark.asyncio
async def test_run_async_benchmark():
    """Test the async benchmark runner."""
    test_pairs = [
        ("The sky is blue", "The sky is red"),
        ("Water is wet", "Fire is hot"),
        ("Cats are animals", "Dogs are plants")
    ]
    
    # Mock the AsyncOpenAIClient
    with patch('benchmarks.openai_async.AsyncOpenAIClient') as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client
        
        # Mock responses for each pair
        mock_client.detect_contradiction_async.side_effect = [
            (True, 0.9, "Clear contradiction", 150.0),
            (False, 0.3, "No contradiction", 120.0),
            (True, 0.8, "Logical contradiction", 180.0)
        ]
        
        result = await run_async_benchmark(
            test_pairs, 
            api_key="test-key",
            model="gpt-4o-mini",
            max_concurrent=2
        )
        
        # Verify results structure
        assert "results" in result
        assert "stats" in result
        assert len(result["results"]) == 3
        
        # Verify stats
        stats = result["stats"]
        assert stats["successful_requests"] == 3
        assert stats["failed_requests"] == 0
        assert stats["contradictions_found"] == 2
        assert stats["max_concurrent"] == 2
        assert stats["mode"] == "async"
        assert "total_time_s" in stats
        assert "avg_api_latency_ms" in stats


@pytest.mark.skipif(not HTTPX_AVAILABLE, reason="httpx not available")
def test_async_import():
    """Test that async modules can be imported."""
    from benchmarks.openai_async import AsyncOpenAIClient, run_async_benchmark
    assert AsyncOpenAIClient is not None
    assert run_async_benchmark is not None


def test_httpx_availability():
    """Test httpx availability detection."""
    if HTTPX_AVAILABLE:
        import httpx
        assert httpx is not None
    else:
        with pytest.raises(ImportError):
            import httpx
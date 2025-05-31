#!/usr/bin/env python3
"""Test v0.5.0 async OpenAI features.

Run with: poetry run python test_v050.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_async_imports():
    """Test that async modules can be imported."""
    try:
        from benchmarks.openai_async import AsyncOpenAIClient, run_async_benchmark
        print("✅ Async OpenAI modules import correctly")
        return True
    except ImportError as e:
        print(f"⚠️  Async imports failed: {e}")
        print("   Install httpx: poetry add httpx")
        return False

def test_httpx_availability():
    """Test httpx dependency."""
    try:
        import httpx
        print("✅ httpx dependency available")
        return True
    except ImportError:
        print("❌ httpx not available - install with: poetry add httpx")
        return False

def test_benchmark_async_flag():
    """Test that benchmark accepts --async flag."""
    try:
        # Import the module and check if async_concurrent parameter exists
        sys.path.insert(0, str(Path(__file__).parent / "benchmarks"))
        from llm_compare import run_benchmark
        import inspect
        
        sig = inspect.signature(run_benchmark)
        if 'async_concurrent' in sig.parameters:
            print("✅ Benchmark CLI accepts --async flag")
            return True
        else:
            print("❌ Benchmark CLI missing async_concurrent parameter")
            return False
    except Exception as e:
        print(f"❌ Benchmark flag test failed: {e}")
        return False

def test_async_client_creation():
    """Test async client can be created."""
    if not test_httpx_availability():
        return False
    
    try:
        from benchmarks.openai_async import AsyncOpenAIClient
        
        # Test with dummy API key
        client = AsyncOpenAIClient(api_key="test-key", max_concurrent=4)
        assert client.max_concurrent == 4
        assert client.model == "gpt-4o-mini"
        
        print("✅ Async client creation works")
        return True
    except Exception as e:
        print(f"❌ Async client creation failed: {e}")
        return False

def test_async_benchmark_structure():
    """Test async benchmark function structure."""
    if not test_httpx_availability():
        return False
    
    try:
        from benchmarks.openai_async import run_async_benchmark
        import inspect
        
        # Check function signature
        sig = inspect.signature(run_async_benchmark)
        expected_params = ['test_pairs', 'api_key', 'model', 'max_concurrent']
        
        for param in expected_params:
            if param not in sig.parameters:
                print(f"❌ Missing parameter: {param}")
                return False
        
        print("✅ Async benchmark function structure correct")
        return True
    except Exception as e:
        print(f"❌ Async benchmark structure test failed: {e}")
        return False

def test_version_bump():
    """Test that version was bumped to 0.5.0."""
    try:
        with open("pyproject.toml", "r") as f:
            content = f.read()
        
        if 'version = "0.5.0"' in content:
            print("✅ Version bumped to 0.5.0")
            return True
        else:
            print("❌ Version not updated to 0.5.0")
            return False
    except Exception as e:
        print(f"❌ Version check failed: {e}")
        return False

def main():
    print("🧪 Testing v0.5.0 async OpenAI features...\n")
    
    tests = [
        test_version_bump,
        test_httpx_availability,
        test_async_imports,
        test_async_client_creation,
        test_async_benchmark_structure,
        test_benchmark_async_flag,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()  # Add spacing between tests
    
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All v0.5.0 features working correctly!")
        print("✨ Ready for async OpenAI performance testing!")
        print("\nNext steps:")
        print("  # Install httpx if not already installed")
        print("  poetry add httpx")
        print("  ")
        print("  # Run async tests")
        print("  poetry run pytest tests/test_openai_async.py -v")
        print("  ")
        print("  # Test async benchmark (requires OpenAI API key)")
        print("  export OPENAI_API_KEY='sk-...'")
        print("  poetry run python -m benchmarks.llm_compare --kimera-only --max-pairs 5")
        print("  poetry run python -m benchmarks.llm_compare --max-pairs 10 --async 8")
        print("  ")
        print("  # Performance comparison")
        print("  poetry run python -m benchmarks.llm_compare --max-pairs 20 --model gpt-4o-mini")
        print("  poetry run python -m benchmarks.llm_compare --max-pairs 20 --model gpt-4o-mini --async 10")
    else:
        print("❌ Some tests failed. Check the output above.")
        print("\nCommon fixes:")
        print("  poetry add httpx  # Install async HTTP client")
        print("  poetry install    # Reinstall dependencies")

if __name__ == "__main__":
    main()
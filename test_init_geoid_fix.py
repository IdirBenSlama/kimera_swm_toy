#!/usr/bin/env python3
"""
Test the init_geoid signature fix for streaming loader compatibility.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_old_signature():
    """Test the old 3-positional signature still works."""
    print("Testing old signature: init_geoid(text, lang, layers)")
    
    from kimera.geoid import init_geoid
    
    geoid = init_geoid("Hello world", "en", ["default"])
    assert geoid.raw == "Hello world"
    assert geoid.lang_axis == "en"
    assert geoid.context_layers == ["default"]
    print("  [OK] Old signature works")

def test_new_signature():
    """Test the new signature with raw parameter."""
    print("Testing new signature: init_geoid(text, lang, layers, raw=...)")
    
    from kimera.geoid import init_geoid
    
    geoid = init_geoid("Hello world", "en", ["test"], raw="Original text")
    assert geoid.raw == "Original text"
    assert geoid.lang_axis == "en"
    assert geoid.context_layers == ["test"]
    print("  [OK] New signature with raw works")

def test_streaming_signature():
    """Test the streaming loader signature."""
    print("Testing streaming signature: init_geoid(raw=..., lang=..., tags=...)")
    
    from kimera.geoid import init_geoid
    
    # This is how the streaming loader calls it
    geoid = init_geoid(
        raw="Test text from streaming loader",
        lang="en", 
        tags=["benchmark"]
    )
    assert geoid.raw == "Test text from streaming loader"
    assert geoid.lang_axis == "en"
    assert geoid.context_layers == ["benchmark"]
    print("  [OK] Streaming signature works")

def test_minimal_signature():
    """Test minimal signature with defaults."""
    print("Testing minimal signature: init_geoid(text)")
    
    from kimera.geoid import init_geoid
    
    geoid = init_geoid("Minimal test")
    assert geoid.raw == "Minimal test"
    assert geoid.lang_axis == "en"
    assert geoid.context_layers == ["default"]
    print("  [OK] Minimal signature works")

def test_error_cases():
    """Test error cases."""
    print("Testing error cases")
    
    from kimera.geoid import init_geoid
    
    try:
        # Should fail - no text or raw
        geoid = init_geoid()
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"  [OK] Correctly raised error: {e}")

def main():
    """Run all tests."""
    print("Testing init_geoid signature fix")
    print("=" * 40)
    
    tests = [
        test_old_signature,
        test_new_signature, 
        test_streaming_signature,
        test_minimal_signature,
        test_error_cases
    ]
    
    passed = 0
    for test in tests:
        try:
            test()
            passed += 1
            print()
        except Exception as e:
            print(f"  [ERROR] {test.__name__} failed: {e}")
            import traceback
            traceback.print_exc()
            print()
    
    print("=" * 40)
    print(f"Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\n[SUCCESS] All init_geoid signature tests passed!")
        print("The streaming loader should now work correctly.")
        return 0
    else:
        print(f"\n[ERROR] {len(tests) - passed} tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
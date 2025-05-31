#!/usr/bin/env python3
"""
Test the echo-form implementation
"""
import sys
sys.path.insert(0, 'src')

def test_echo_basic():
    """Test basic echo functionality"""
    print("🧪 Testing echo-form implementation...")
    
    from kimera.geoid import init_geoid
    
    # Test basic echo creation
    g1 = init_geoid(text="Hello world", lang="en", tags=["test"])
    print(f"  Raw: '{g1.raw}'")
    print(f"  Echo: '{g1.echo}'")
    print(f"  GID: {g1.gid}")
    
    assert g1.raw == "Hello world"
    assert g1.echo == "Hello world"
    assert len(g1.gid) == 16  # 16-char hex
    print("  ✅ Basic echo works")

def test_echo_trimming():
    """Test that echo trims whitespace"""
    print("\n🧪 Testing echo trimming...")
    
    from kimera.geoid import init_geoid
    
    g1 = init_geoid(text="  Hello world  ", lang="en", tags=["test"])
    g2 = init_geoid(text="Hello world", lang="en", tags=["test"])
    
    print(f"  G1 raw: '{g1.raw}' -> echo: '{g1.echo}' -> gid: {g1.gid}")
    print(f"  G2 raw: '{g2.raw}' -> echo: '{g2.echo}' -> gid: {g2.gid}")
    
    assert g1.raw == "  Hello world  "
    assert g1.echo == "Hello world"
    assert g2.echo == "Hello world"
    assert g1.gid == g2.gid  # Same echo should give same gid
    print("  ✅ Echo trimming works")

def test_stable_hashing():
    """Test that gid is stable and deterministic"""
    print("\n🧪 Testing stable hashing...")
    
    from kimera.geoid import init_geoid
    
    # Same text should always give same gid
    g1 = init_geoid(text="Test text", lang="en", tags=["test"])
    g2 = init_geoid(text="Test text", lang="en", tags=["test"])
    g3 = init_geoid(text="Different text", lang="en", tags=["test"])
    
    print(f"  Same text: {g1.gid} == {g2.gid}")
    print(f"  Different text: {g3.gid}")
    
    assert g1.gid == g2.gid  # Same text -> same gid
    assert g1.gid != g3.gid  # Different text -> different gid
    print("  ✅ Stable hashing works")

def test_cache_integration():
    """Test that cache uses echo for keying"""
    print("\n🧪 Testing cache integration...")
    
    from kimera.geoid import init_geoid
    from kimera.cache import embed_cache
    
    # Clear cache
    embed_cache.clear()
    
    # Create geoid with trimmed text
    g1 = init_geoid(text="  Cache test  ", lang="en", tags=["test"])
    
    # Check if cache has the trimmed version
    cached_vec = embed_cache.get("en", "Cache test")  # Trimmed version
    
    print(f"  Echo: '{g1.echo}'")
    print(f"  Cached vector exists: {cached_vec is not None}")
    
    assert cached_vec is not None, "Cache should use echo (trimmed) as key"
    print("  ✅ Cache integration works")

def main():
    """Run all echo-form tests"""
    print("🔧 Echo-Form Implementation Test")
    print("=" * 35)
    
    tests = [
        test_echo_basic,
        test_echo_trimming,
        test_stable_hashing,
        test_cache_integration
    ]
    
    passed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  ❌ {test.__name__} failed: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n📊 Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 Echo-form implementation working perfectly!")
        print("\n✨ Benefits:")
        print("  • Stable, deterministic geoid hashes")
        print("  • Whitespace-insensitive deduplication")
        print("  • Clean observability in explorer")
        print("  • Cache efficiency improvement")
        return True
    else:
        print("❌ Some tests failed - needs attention")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
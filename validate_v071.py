#!/usr/bin/env python3
"""
Comprehensive validation for Kimera v0.7.1
Tests both echo-form implementation and negation fix
"""
import sys
import os
sys.path.insert(0, 'src')

def test_echo_form():
    """Test echo-form implementation"""
    print("🔧 Testing Echo-Form Implementation...")
    
    try:
        from kimera.geoid import init_geoid
        
        # Test 1: Basic echo functionality
        g = init_geoid(text="Hello world", lang="en", tags=["test"])
        assert hasattr(g, 'echo'), "Geoid should have echo field"
        assert g.echo == "Hello world", f"Expected 'Hello world', got '{g.echo}'"
        assert len(g.gid) == 16, f"Expected 16-char GID, got {len(g.gid)}"
        print("  ✅ Basic echo functionality")
        
        # Test 2: Whitespace trimming
        g1 = init_geoid(text="  Test text  ", lang="en", tags=["test"])
        g2 = init_geoid(text="Test text", lang="en", tags=["test"])
        assert g1.echo == "Test text", f"Expected trimmed echo, got '{g1.echo}'"
        assert g1.gid == g2.gid, "Same echo should produce same GID"
        print("  ✅ Whitespace trimming and stable hashing")
        
        # Test 3: Deterministic hashing
        g3 = init_geoid(text="Test text", lang="en", tags=["test"])
        g4 = init_geoid(text="Test text", lang="en", tags=["test"])
        assert g3.gid == g4.gid, "Same input should always produce same GID"
        print("  ✅ Deterministic hashing")
        
        # Test 4: Different texts produce different GIDs
        g5 = init_geoid(text="Different text", lang="en", tags=["test"])
        assert g3.gid != g5.gid, "Different texts should produce different GIDs"
        print("  ✅ Different texts produce different GIDs")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Echo-form test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_negation_fix():
    """Test negation fix functionality"""
    print("\n🔧 Testing Negation Fix...")
    
    try:
        # Test environment variable control
        os.environ["KIMERA_NEGATION_FIX"] = "0"
        
        # Clear cached modules
        modules_to_clear = [k for k in sys.modules.keys() if k.startswith('kimera')]
        for mod in modules_to_clear:
            del sys.modules[mod]
        
        from kimera.resonance import ENABLE_NEGATION_FIX
        negation_off = ENABLE_NEGATION_FIX
        
        # Test with negation ON
        os.environ["KIMERA_NEGATION_FIX"] = "1"
        
        # Clear cached modules again
        modules_to_clear = [k for k in sys.modules.keys() if k.startswith('kimera')]
        for mod in modules_to_clear:
            del sys.modules[mod]
        
        from kimera.resonance import ENABLE_NEGATION_FIX
        negation_on = ENABLE_NEGATION_FIX
        
        assert negation_off != negation_on, "Environment variable should control negation fix"
        print(f"  ✅ Environment control: OFF={negation_off}, ON={negation_on}")
        
        # Test actual negation behavior
        from kimera.geoid import init_geoid
        from kimera.resonance import resonance
        
        g1 = init_geoid(text="Birds can fly", lang="en", tags=["test"])
        g2 = init_geoid(text="Birds cannot fly", lang="en", tags=["test"])
        
        score = resonance(g1, g2)
        print(f"  ✅ Negation test score: {score:.3f} (negation fix: {ENABLE_NEGATION_FIX})")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Negation fix test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cache_integration():
    """Test cache integration with echo"""
    print("\n🔧 Testing Cache Integration...")
    
    try:
        from kimera.geoid import init_geoid
        from kimera.cache import embed_cache
        
        # Clear cache
        embed_cache.clear()
        
        # Create geoid with whitespace
        g = init_geoid(text="  Cache test  ", lang="en", tags=["test"])
        
        # Check if cache uses echo (trimmed version)
        cached_vec = embed_cache.get("en", "Cache test")
        assert cached_vec is not None, "Cache should use echo (trimmed) as key"
        print("  ✅ Cache uses echo for keying")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Cache integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_benchmark_compatibility():
    """Test that benchmarks work with new implementation"""
    print("\n🔧 Testing Benchmark Compatibility...")
    
    try:
        # Test that benchmark imports work
        from benchmarks.llm_compare import log
        log("Test message")
        print("  ✅ Benchmark logging works")
        
        # Test geoid creation in benchmark context
        from kimera.geoid import init_geoid
        g = init_geoid(text="Benchmark test", lang="en", tags=["benchmark"])
        assert hasattr(g, 'echo'), "Benchmark geoids should have echo"
        print("  ✅ Benchmark geoid creation works")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Benchmark compatibility test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_explorer_compatibility():
    """Test that explorer can handle echo columns"""
    print("\n🔧 Testing Explorer Compatibility...")
    
    try:
        # Check that explorer.html has echo support
        with open("tools/explorer.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        assert "echo1" in content.lower(), "Explorer should support echo1 column"
        assert "echo2" in content.lower(), "Explorer should support echo2 column"
        assert "echo-cell" in content, "Explorer should have echo cell styling"
        print("  ✅ Explorer has echo column support")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Explorer compatibility test failed: {e}")
        return False

def main():
    """Run comprehensive v0.7.1 validation"""
    print("🧪 Kimera v0.7.1 Comprehensive Validation")
    print("=" * 45)
    
    tests = [
        ("Echo-Form Implementation", test_echo_form),
        ("Negation Fix", test_negation_fix),
        ("Cache Integration", test_cache_integration),
        ("Benchmark Compatibility", test_benchmark_compatibility),
        ("Explorer Compatibility", test_explorer_compatibility),
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"\n❌ {name} test crashed: {e}")
    
    print(f"\n📊 Validation Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All v0.7.1 features working perfectly!")
        print("\n✨ Ready for:")
        print("  • Negation fix experiment")
        print("  • Large-scale benchmarking")
        print("  • Enhanced error analysis")
        print("  • Next semantic improvement iteration")
        
        print("\n🚀 Quick start commands:")
        print("  python test_fixes.py                    # Test surgical fixes")
        print("  python focused_experiment.py            # Quick negation test")
        print("  .\\run_negation_experiment.ps1          # Full experiment (PowerShell)")
        print("  poetry run python -m benchmarks.llm_compare --kimera-only --max-pairs 100")
        
        return True
    else:
        print(f"\n❌ {total - passed} tests failed - needs attention")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
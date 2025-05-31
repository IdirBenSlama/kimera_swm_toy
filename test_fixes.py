#!/usr/bin/env python3
"""
Test that our surgical fixes work
"""
import os
import sys
sys.path.insert(0, 'src')

def test_logging_fix():
    """Test that the logging fix works"""
    print("🔧 Testing logging fix...")
    
    try:
        # This should not crash with emoji issues
        from benchmarks.llm_compare import log
        log("📊 Test emoji message")
        print("  ✅ Logging fix works")
        return True
    except Exception as e:
        print(f"  ❌ Logging fix failed: {e}")
        return False

def test_geoid_fix():
    """Test that geoid creation works"""
    print("🔧 Testing geoid creation fix...")
    
    try:
        from kimera.geoid import init_geoid
        from kimera.resonance import resonance
        
        # Create geoids properly
        g1 = init_geoid(text="Birds can fly", lang="en", tags=["test"])
        g2 = init_geoid(text="Birds cannot fly", lang="en", tags=["test"])
        
        # Test resonance
        score = resonance(g1, g2)
        print(f"  ✅ Geoid creation works, score: {score:.3f}")
        return True
    except Exception as e:
        print(f"  ❌ Geoid creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_negation_toggle():
    """Test that negation toggle works"""
    print("🔧 Testing negation toggle...")
    
    try:
        # Test with negation OFF
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
        
        print(f"  Negation OFF: {negation_off}")
        print(f"  Negation ON: {negation_on}")
        
        if negation_off != negation_on:
            print("  ✅ Negation toggle works")
            return True
        else:
            print("  ❌ Negation toggle not working")
            return False
            
    except Exception as e:
        print(f"  ❌ Negation toggle failed: {e}")
        return False

def main():
    """Run all fix tests"""
    print("🧪 Testing Surgical Fixes")
    print("=" * 30)
    
    tests = [
        test_logging_fix,
        test_geoid_fix,
        test_negation_toggle
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All fixes working! Ready for experiment!")
        print("\nRun the experiment:")
        print("  PowerShell: .\\run_negation_experiment.ps1")
        print("  Python: python focused_experiment.py")
    else:
        print("❌ Some fixes need attention")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Run Phase 19.2 tests for CLS lattice integration and time-decay weighting
"""
import sys
import subprocess

def run_test(test_file, description):
    """Run a test file and return success status"""
    print(f"\n🧪 {description}")
    print("=" * (len(description) + 4))
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, cwd=".")
        
        if result.returncode == 0:
            print(result.stdout)
            print(f"✅ {description} - PASSED")
            return True
        else:
            print(result.stdout)
            print(result.stderr)
            print(f"❌ {description} - FAILED")
            return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def main():
    """Run all Phase 19.2 tests"""
    print("🚀 Phase 19.2 Test Suite")
    print("CLS Lattice Write + Time-Decay Weighting")
    print("=" * 50)
    
    tests = [
        ("tests/test_echoform_core.py", "EchoForm Core with Time-Decay"),
        ("tests/test_cls_integration.py", "CLS Integration with Storage"),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_file, description in tests:
        if run_test(test_file, description):
            passed += 1
    
    print(f"\n📊 Phase 19.2 Test Results: {passed}/{total} test suites passed")
    
    if passed == total:
        print("\n🎉 Phase 19.2 Implementation Complete!")
        print("\n✨ Ready for:")
        print("  • CLS lattice forms are now stored and tracked")
        print("  • cls_event terms append on every resonance")
        print("  • Time-decay weighting with τ = 14 days")
        print("  • All tests green - ready for v0.7.3 tag")
        return True
    else:
        print(f"\n❌ {total - passed} test suite(s) failed")
        print("Fix issues before proceeding to v0.7.3")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
#!/usr/bin/env python3
"""
Run SCAR functionality tests
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

def run_scar_test():
    """Run SCAR system tests"""
    print("🔍 RUNNING SCAR TESTS")
    print("=" * 25)
    
    test_results = []
    
    # Test 1: Basic SCAR import
    try:
        from kimera.identity import generate_scar
        test_results.append(("SCAR Import", "PASSED"))
        print("✅ SCAR import successful")
    except Exception as e:
        test_results.append(("SCAR Import", f"FAILED: {e}"))
        print(f"❌ SCAR import failed: {e}")
        return False
    
    # Test 2: Basic SCAR generation
    try:
        scar = generate_scar("test content A", "test content B", "test relationship")
        if scar and len(scar) == 16:
            test_results.append(("SCAR Generation", "PASSED"))
            print(f"✅ SCAR generated: {scar}")
        else:
            test_results.append(("SCAR Generation", f"FAILED: Invalid SCAR format"))
            print(f"❌ Invalid SCAR format: {scar}")
    except Exception as e:
        test_results.append(("SCAR Generation", f"FAILED: {e}"))
        print(f"❌ SCAR generation failed: {e}")
    
    # Test 3: SCAR stability
    try:
        scar1 = generate_scar("content A", "content B", "relationship")
        scar2 = generate_scar("content A", "content B", "relationship")
        if scar1 == scar2:
            test_results.append(("SCAR Stability", "PASSED"))
            print("✅ SCAR generation is stable")
        else:
            test_results.append(("SCAR Stability", "FAILED: Non-deterministic"))
            print(f"❌ SCAR instability: {scar1} != {scar2}")
    except Exception as e:
        test_results.append(("SCAR Stability", f"FAILED: {e}"))
        print(f"❌ SCAR stability test failed: {e}")
    
    # Test 4: Unicode SCAR
    try:
        unicode_scar = generate_scar("测试内容", "тест", "🔗")
        if unicode_scar and len(unicode_scar) == 16:
            test_results.append(("Unicode SCAR", "PASSED"))
            print(f"✅ Unicode SCAR: {unicode_scar}")
        else:
            test_results.append(("Unicode SCAR", "FAILED: Invalid format"))
            print(f"❌ Unicode SCAR failed: {unicode_scar}")
    except Exception as e:
        test_results.append(("Unicode SCAR", f"FAILED: {e}"))
        print(f"❌ Unicode SCAR failed: {e}")
    
    # Summary
    passed = sum(1 for _, result in test_results if result == "PASSED")
    total = len(test_results)
    
    print(f"\n📊 SCAR TEST SUMMARY:")
    print(f"  Tests passed: {passed}/{total}")
    print(f"  Success rate: {(passed/total*100):.1f}%")
    
    for test_name, result in test_results:
        emoji = "✅" if result == "PASSED" else "❌"
        print(f"  {emoji} {test_name}: {result}")
    
    return passed == total

if __name__ == "__main__":
    success = run_scar_test()
    sys.exit(0 if success else 1)
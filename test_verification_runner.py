#!/usr/bin/env python3
"""Quick test runner to verify the system is working."""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_basic_imports():
    """Test basic imports work."""
    print("🧪 Testing basic imports...")
    
    try:
        # Test actual available imports
        from kimera.identity import Identity
        from kimera.echoform import EchoForm
        from kimera.storage import LatticeStorage
        print("✅ Core imports successful")
        
        # Test utils imports
        from kimera.utils.safe_console import safe_print
        print("✅ Utils imports successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality works."""
    print("\n🧪 Testing basic functionality...")
    
    try:
        from kimera.core.identity import IdentityManager
        
        # Test identity manager
        identity_mgr = IdentityManager()
        test_id = identity_mgr.generate_id("test")
        print(f"✅ Generated test ID: {test_id}")
        
        # Test validation
        is_valid = identity_mgr.validate_id(test_id)
        print(f"✅ ID validation: {is_valid}")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def test_pipeline_creation():
    """Test pipeline creation works."""
    print("\n🧪 Testing pipeline creation...")
    
    try:
        from kimera.pipeline.mixed import MixedPipeline
        
        # Test pipeline creation
        pipeline = MixedPipeline()
        print("✅ MixedPipeline created successfully")
        
        # Test basic pipeline methods
        if hasattr(pipeline, 'process'):
            print("✅ Pipeline has process method")
        
        return True
        
    except Exception as e:
        print(f"❌ Pipeline test failed: {e}")
        return False

def main():
    """Run all verification tests."""
    print("🚀 RUNNING QUICK VERIFICATION TESTS")
    print("=" * 50)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Basic Functionality", test_basic_functionality),
        ("Pipeline Creation", test_pipeline_creation)
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {name}: PASSED")
            else:
                print(f"❌ {name}: FAILED")
        except Exception as e:
            print(f"❌ {name}: ERROR - {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("✅ System is working correctly")
    else:
        print(f"⚠️ {total - passed} test(s) failed")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
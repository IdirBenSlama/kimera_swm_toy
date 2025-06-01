#!/usr/bin/env python3
"""
Quick verification test to check if basic functionality is working
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_basic_imports():
    """Test basic imports"""
    print("🔍 Testing basic imports...")
    
    try:
        # Test core imports
        from kimera.geoid import init_geoid
        from kimera.identity import create_geoid_identity
        from kimera.echoform import EchoForm
        from kimera.storage import LatticeStorage
        from kimera.cls import lattice_resolve
        from kimera.entropy import adaptive_tau, decay_factor
        
        print("✅ All basic imports successful")
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_basic_functionality():
    """Test basic functionality"""
    print("\n🔍 Testing basic functionality...")
    
    try:
        from kimera.identity import create_geoid_identity
        from kimera.cls import lattice_resolve
        from kimera.entropy import adaptive_tau
        
        # Create test identities
        identity_a = create_geoid_identity("Test A", tags=["test"])
        identity_b = create_geoid_identity("Test B", tags=["test"])
        
        print(f"✅ Created identities: {identity_a.id[:8]}... and {identity_b.id[:8]}...")
        
        # Test entropy
        entropy_a = identity_a.entropy()
        print(f"✅ Entropy calculation: {entropy_a:.3f}")
        
        # Test adaptive tau
        tau = adaptive_tau(1000, entropy_a)
        print(f"✅ Adaptive tau: {tau:.1f}")
        
        # Test lattice resolve
        intensity = lattice_resolve(identity_a, identity_b)
        print(f"✅ Lattice resolve: {intensity:.3f}")
        
        print("✅ Basic functionality working")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run quick verification"""
    print("🚀 QUICK VERIFICATION TEST")
    print("=" * 40)
    
    tests = [
        test_basic_imports,
        test_basic_functionality,
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\n🎉 QUICK VERIFICATION PASSED!")
        print("✅ Core functionality is working")
        return True
    else:
        print("\n❌ Some tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
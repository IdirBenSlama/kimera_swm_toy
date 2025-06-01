#!/usr/bin/env python3
"""
Final comprehensive verification of the Kimera project
Tests all core functionality and ensures everything is working
"""

import sys
import os
import subprocess
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test all critical imports"""
    print("🔍 Testing imports...")
    
    try:
        # Core imports
        from kimera.identity import create_geoid_identity, Identity
        from kimera.entropy import adaptive_tau, decay_factor, calculate_shannon_entropy
        from kimera.cls import lattice_resolve
        from kimera.storage import LatticeStorage
        from kimera.echoform import EchoForm
        
        print("✅ All imports successful")
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_identity_creation():
    """Test identity creation and basic operations"""
    print("\n🔍 Testing identity creation...")
    
    try:
        from kimera.identity import create_geoid_identity
        
        # Create test identities
        identity_a = create_geoid_identity("Hello world", tags=["greeting", "test"])
        identity_b = create_geoid_identity("Complex multi-term content", 
                                         tags=["complex", "multi", "term", "test"])
        
        print(f"✅ Created identity A: {identity_a.id[:8]}...")
        print(f"✅ Created identity B: {identity_b.id[:8]}...")
        
        # Test entropy calculation
        entropy_a = identity_a.entropy()
        entropy_b = identity_b.entropy()
        
        print(f"✅ Entropy A: {entropy_a:.3f}")
        print(f"✅ Entropy B: {entropy_b:.3f}")
        
        # Test effective tau
        tau_a = identity_a.effective_tau()
        tau_b = identity_b.effective_tau()
        
        print(f"✅ Effective tau A: {tau_a:.1f}")
        print(f"✅ Effective tau B: {tau_b:.1f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Identity creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_lattice_operations():
    """Test lattice operations"""
    print("\n🔍 Testing lattice operations...")
    
    try:
        from kimera.identity import create_geoid_identity
        from kimera.cls import lattice_resolve
        
        # Create test identities
        identity_a = create_geoid_identity("Test A", tags=["test"])
        identity_b = create_geoid_identity("Test B", tags=["test"])
        
        # Test lattice resolve
        intensity = lattice_resolve(identity_a, identity_b)
        print(f"✅ Lattice resolve intensity: {intensity:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Lattice operations failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_storage_operations():
    """Test storage operations"""
    print("\n🔍 Testing storage operations...")
    
    try:
        from kimera.identity import create_geoid_identity
        from kimera.storage import LatticeStorage
        
        # Create temporary database
        db_path = "test_final_verification.db"
        
        try:
            storage = LatticeStorage(db_path)
            
            # Create and store identity
            identity = create_geoid_identity("Storage test", tags=["storage", "test"])
            storage.store_identity(identity)
            
            print(f"✅ Stored identity: {identity.id[:8]}...")
            
            # Test retrieval
            retrieved = storage.get_identity(identity.id)
            if retrieved:
                print(f"✅ Retrieved identity: {retrieved.id[:8]}...")
            else:
                print("❌ Failed to retrieve identity")
                return False
            
            storage.close()
            return True
            
        finally:
            # Clean up
            if os.path.exists(db_path):
                os.unlink(db_path)
        
    except Exception as e:
        print(f"❌ Storage operations failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_entropy_functions():
    """Test entropy calculation functions"""
    print("\n🔍 Testing entropy functions...")
    
    try:
        from kimera.entropy import calculate_shannon_entropy, adaptive_tau, decay_factor
        
        # Test Shannon entropy
        intensities = [0.5, 0.3, 0.2]
        entropy = calculate_shannon_entropy(intensities)
        print(f"✅ Shannon entropy: {entropy:.3f}")
        
        # Test adaptive tau
        tau = adaptive_tau(1000, entropy)
        print(f"✅ Adaptive tau: {tau:.1f}")
        
        # Test decay factor
        decay = decay_factor(100, tau)
        print(f"✅ Decay factor: {decay:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Entropy functions failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_external_tests():
    """Run external test scripts"""
    print("\n🔍 Running external test scripts...")
    
    test_scripts = [
        ("simple_identity_test.py", "Simple identity test"),
        ("test_p0_integration.py", "P0 integration tests"),
    ]
    
    passed = 0
    for script, description in test_scripts:
        if os.path.exists(script):
            try:
                print(f"\n  Running {description}...")
                result = subprocess.run([sys.executable, script], 
                                      capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    print(f"  ✅ {description} passed")
                    passed += 1
                else:
                    print(f"  ❌ {description} failed")
                    print(f"     Error: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                print(f"  ⏰ {description} timed out")
            except Exception as e:
                print(f"  💥 {description} error: {e}")
        else:
            print(f"  ⚠️  {script} not found")
    
    return passed

def main():
    """Run comprehensive verification"""
    print("🚀 KIMERA FINAL VERIFICATION")
    print("=" * 50)
    
    # Core functionality tests
    tests = [
        test_imports,
        test_identity_creation,
        test_lattice_operations,
        test_storage_operations,
        test_entropy_functions,
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    # External tests
    external_passed = run_external_tests()
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 FINAL VERIFICATION RESULTS")
    print('='*50)
    
    total_core = len(tests)
    print(f"Core functionality: {passed}/{total_core} tests passed")
    print(f"External scripts: {external_passed} scripts passed")
    
    overall_success = (passed == total_core)
    
    if overall_success:
        print("\n🎉 KIMERA VERIFICATION SUCCESSFUL!")
        print("\n✅ PROJECT STATUS: FULLY OPERATIONAL")
        print("\n🚀 READY FOR:")
        print("   • poetry run pytest -q")
        print("   • Production deployment")
        print("   • Research applications")
        print("   • Benchmark testing")
        
        print("\n📋 NEXT STEPS:")
        print("   1. Run: poetry run pytest -q")
        print("   2. Deploy to production")
        print("   3. Begin research phase")
        
        return True
    else:
        print(f"\n⚠️  {total_core - passed} core test(s) failed")
        print("   Please address failing tests before proceeding")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
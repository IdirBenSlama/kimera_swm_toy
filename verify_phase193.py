#!/usr/bin/env python3
"""
Verify Phase 19.3 implementation is working
"""
import sys
import os
import subprocess

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        sys.path.insert(0, 'src')
        from kimera.storage import get_storage, close_storage
        from kimera.echoform import EchoForm
        from kimera.geoid import init_geoid
        from kimera.cls import lattice_resolve
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_storage():
    """Test basic storage functionality"""
    print("Testing storage...")
    try:
        sys.path.insert(0, 'src')
        from kimera.storage import get_storage, close_storage
        from kimera.echoform import EchoForm
        
        # Clean up
        if os.path.exists("test_verify.db"):
            os.remove("test_verify.db")
        
        storage = get_storage("test_verify.db")
        
        # Create and store form
        form = EchoForm(
            anchor="verify_test",
            domain="test",
            terms=[{"symbol": "test", "role": "verify", "intensity": 1.0}],
            phase="testing"
        )
        storage.store_form(form)
        
        # Retrieve form
        retrieved = storage.fetch_form("verify_test")
        assert retrieved is not None
        assert retrieved.anchor == "verify_test"
        
        close_storage()
        print("✅ Storage test passed")
        return True
        
    except Exception as e:
        print(f"❌ Storage test failed: {e}")
        return False
    finally:
        if os.path.exists("test_verify.db"):
            os.remove("test_verify.db")

def test_cls():
    """Test CLS functionality"""
    print("Testing CLS...")
    try:
        sys.path.insert(0, 'src')
        from kimera.storage import get_storage, close_storage
        from kimera.geoid import init_geoid
        from kimera.cls import lattice_resolve
        
        # Clean up
        if os.path.exists("test_cls_verify.db"):
            os.remove("test_cls_verify.db")
        
        storage = get_storage("test_cls_verify.db")
        
        # Create geoids and test resolve
        geo_a = init_geoid("Verify A", "en", ["test"])
        geo_b = init_geoid("Verify B", "en", ["test"])
        
        intensity1 = lattice_resolve(geo_a, geo_b)
        intensity2 = lattice_resolve(geo_a, geo_b)
        
        assert intensity2 > intensity1
        
        close_storage()
        print("✅ CLS test passed")
        return True
        
    except Exception as e:
        print(f"❌ CLS test failed: {e}")
        return False
    finally:
        if os.path.exists("test_cls_verify.db"):
            os.remove("test_cls_verify.db")

def test_cli():
    """Test CLI functionality"""
    print("Testing CLI...")
    try:
        # Test CLI help
        result = subprocess.run([
            sys.executable, "-m", "kimera", "--help"
        ], capture_output=True, text=True, cwd="src")
        
        if result.returncode == 0:
            print("✅ CLI test passed")
            return True
        else:
            print(f"❌ CLI test failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False

def main():
    print("🔍 Verifying Phase 19.3 Implementation")
    print("=" * 40)
    
    tests = [
        ("Import test", test_imports),
        ("Storage test", test_storage),
        ("CLS test", test_cls),
        ("CLI test", test_cli),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
        else:
            failed += 1
    
    print(f"\n📊 Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 Phase 19.3 verification successful!")
        print("✨ Ready to commit and push!")
        return True
    else:
        print("💥 Some tests failed. Please fix before proceeding.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
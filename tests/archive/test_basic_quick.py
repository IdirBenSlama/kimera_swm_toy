#!/usr/bin/env python3
"""
Basic quick test for development verification
"""
import pytest

def test_basic_imports():
    """Test that basic imports work"""
    try:
        from src.kimera.identity import Identity
        from src.kimera.storage import Storage
        from src.kimera.cls import CLS
        assert True
    except ImportError:
        pytest.fail("Basic imports failed")

def test_basic_functionality():
    """Test basic system functionality"""
    try:
        from src.kimera.identity import Identity
        identity = Identity()
        scar = identity.generate_scar("test", "content", "similarity")
        assert scar is not None
        assert isinstance(scar, str)
    except Exception as e:
        pytest.fail(f"Basic functionality test failed: {e}")

if __name__ == "__main__":
    test_basic_imports()
    test_basic_functionality()
    print("✅ Basic quick tests passed")
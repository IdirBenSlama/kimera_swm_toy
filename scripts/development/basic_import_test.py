#!/usr/bin/env python3
"""
Basic import test for development verification
"""

def test_basic_imports():
    """Test basic module imports"""
    try:
        from src.kimera.identity import Identity
        from src.kimera.storage import Storage
        from src.kimera.cls import CLS
        print("✅ All basic imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

if __name__ == "__main__":
    test_basic_imports()
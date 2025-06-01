#!/usr/bin/env python3
"""
Check current system status
"""

def check_system_status():
    """Check overall system status"""
    try:
        # Check imports
        from src.kimera.identity import Identity
        from src.kimera.storage import Storage
        from src.kimera.cls import CLS
        print("✅ Core imports working")
        
        # Check basic functionality
        identity = Identity()
        storage = Storage()
        cls = CLS()
        print("✅ Core systems initialized")
        
        # Test basic operations
        scar = identity.generate_scar("test", "content", "similarity")
        print(f"✅ SCAR generation working: {scar}")
        
        print("✅ System status: OPERATIONAL")
        return True
        
    except Exception as e:
        print(f"❌ System check failed: {e}")
        return False

if __name__ == "__main__":
    check_system_status()
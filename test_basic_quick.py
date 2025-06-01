#!/usr/bin/env python3
"""
Very basic test to check if imports work
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    print("Testing basic imports...")
    
    try:
        # Test most basic import
        from kimera.identity import create_geoid_identity
        print("✅ Identity import works")
        
        # Create a simple identity
        identity = create_geoid_identity("Hello world", tags=["test"])
        print(f"✅ Identity created: {identity.id[:8]}...")
        
        # Test entropy
        entropy = identity.entropy()
        print(f"✅ Entropy: {entropy:.3f}")
        
        print("\n🎉 Basic functionality is working!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Ready to run full verification suite")
    else:
        print("\n❌ Basic functionality issues need to be resolved first")
    sys.exit(0 if success else 1)
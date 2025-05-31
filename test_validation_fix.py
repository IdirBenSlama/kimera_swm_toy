#!/usr/bin/env python3
"""
Test the validation fix
"""
import subprocess
import sys

def main():
    """Test the fixed validation"""
    print("🧪 Testing Fixed Validation")
    print("=" * 30)
    
    try:
        result = subprocess.run(
            [sys.executable, "validate_v071.py"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print("Return code:", result.returncode)
        print("\nSTDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("\nSTDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("\n🎉 Validation passed!")
            return True
        else:
            print("\n❌ Validation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    main()
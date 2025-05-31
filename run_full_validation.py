#!/usr/bin/env python3
"""
Run the full v0.7.1 validation
"""
import subprocess
import sys
import os

def main():
    """Run the validation"""
    print("🧪 Running Kimera v0.7.1 Full Validation")
    print("=" * 45)
    
    # Set UTF-8 environment
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    env['LANG'] = 'en_US.UTF-8'
    
    try:
        result = subprocess.run(
            [sys.executable, "validate_v071.py"],
            env=env,
            timeout=120
        )
        
        if result.returncode == 0:
            print("\n🎉 All validations passed!")
            return True
        else:
            print(f"\n❌ Validation failed with return code {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print("\n⏰ Validation timed out")
        return False
    except Exception as e:
        print(f"\n💥 Error running validation: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
#!/usr/bin/env python3
"""
Run quick validation and show results
"""
import subprocess
import sys
import os

def main():
    print("🔍 Running Quick Validation of Kimera 0.7.x Fixes...")
    print("=" * 60)
    
    try:
        # Set environment variable for testing
        env = os.environ.copy()
        env['KIMERA_DB_PATH'] = 'test_kimera.db'
        
        # Run the quick validation script
        result = subprocess.run([sys.executable, "quick_validation.py"], 
                              capture_output=True, text=True, timeout=60, env=env)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("\nSTDERR:")
            print(result.stderr)
        
        print(f"\nReturn code: {result.returncode}")
        
        if result.returncode == 0:
            print("\n🎉 Quick validation PASSED!")
        else:
            print("\n❌ Quick validation FAILED!")
            
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ Validation script timed out")
        return False
    except Exception as e:
        print(f"❌ Error running validation: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
#!/usr/bin/env python3
"""
Run comprehensive test of all fixes
"""
import subprocess
import sys
import os

def main():
    print("🔍 Running Comprehensive Test of Kimera 0.7.x Fixes...")
    print("=" * 60)
    
    try:
        # Set environment variable for testing
        env = os.environ.copy()
        env['KIMERA_DB_PATH'] = 'test_kimera.db'
        
        # Run the comprehensive test script
        result = subprocess.run([sys.executable, "test_final_fixes.py"], 
                              capture_output=True, text=True, timeout=120, env=env)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("\nSTDERR:")
            print(result.stderr)
        
        print(f"\nReturn code: {result.returncode}")
        
        if result.returncode == 0:
            print("\n🎉 Comprehensive test PASSED!")
        else:
            print("\n❌ Comprehensive test FAILED!")
            
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ Test script timed out")
        return False
    except Exception as e:
        print(f"❌ Error running test: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
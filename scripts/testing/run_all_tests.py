#!/usr/bin/env python3
"""
Run all tests in the test suite
"""
import subprocess
import sys

def run_all_tests():
    """Execute all tests"""
    try:
        print("🧪 Running all tests...")
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", "-v", "--tb=short"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
            
        if result.returncode == 0:
            print("✅ All tests passed")
        else:
            print("❌ Some tests failed")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
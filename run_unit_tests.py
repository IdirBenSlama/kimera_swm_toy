#!/usr/bin/env python3
"""
Quick test runner to check current test status
"""
import subprocess
import sys
import os

def run_tests():
    """Run the unit tests and capture output"""
    
    # Test the unit tests
    test_files = [
        "tests/unit/test_echoform_core.py",
        "tests/unit/test_identity.py", 
        "tests/unit/test_storage.py"
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n=== Running {test_file} ===")
            try:
                # Change to the project directory
                result = subprocess.run([sys.executable, test_file], 
                                      capture_output=True, text=True, timeout=30)
                print("STDOUT:", result.stdout)
                if result.stderr:
                    print("STDERR:", result.stderr)
                print("Return code:", result.returncode)
            except subprocess.TimeoutExpired:
                print("Test timed out")
            except Exception as e:
                print(f"Error running test: {e}")
        else:
            print(f"Test file not found: {test_file}")

if __name__ == "__main__":
    run_tests()
#!/usr/bin/env python3
"""
Quick test to verify negation fix doesn't break existing functionality
"""
import subprocess
import sys

def run_test(test_name):
    """Run a specific test and return result"""
    try:
        result = subprocess.run([sys.executable, "-m", "pytest", test_name, "-v"], 
                              capture_output=True, text=True, timeout=60)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("Testing negation fix compatibility...")
    
    # Test core functionality
    tests = [
        "tests/test_geoid.py",
        "tests/test_reactor.py", 
        "test_negation_fix.py"
    ]
    
    for test in tests:
        print(f"\nRunning {test}...")
        success, stdout, stderr = run_test(test)
        if success:
            print(f"✓ {test} passed")
        else:
            print(f"✗ {test} failed")
            if stderr:
                print(f"Error: {stderr}")
    
    print("\nTesting negation detection directly...")
    try:
        # Import and test directly
        sys.path.insert(0, "src")
        from kimera.resonance import negation_mismatch
        
        # Quick tests
        assert negation_mismatch("Birds can fly", "Birds cannot fly") == True
        assert negation_mismatch("Snow is white", "Snow is black") == False
        print("✓ Negation detection working correctly")
        
    except Exception as e:
        print(f"✗ Negation detection failed: {e}")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, 'src')

# Set environment
os.environ['PYTHONPATH'] = 'src'

print("Testing EchoForm unit tests directly...")

try:
    # Import and run the test functions directly
    from tests.unit.test_echoform_core import (
        test_echoform_creation,
        test_echoform_basic_operations, 
        test_echoform_configuration
    )
    
    print("Running test_echoform_creation...")
    test_echoform_creation()
    print("✅ test_echoform_creation passed")
    
    print("Running test_echoform_basic_operations...")
    test_echoform_basic_operations()
    print("✅ test_echoform_basic_operations passed")
    
    print("Running test_echoform_configuration...")
    test_echoform_configuration()
    print("✅ test_echoform_configuration passed")
    
    print("\n🎉 All EchoForm tests passed!")
    
except Exception as e:
    print(f"❌ EchoForm test failed: {e}")
    import traceback
    traceback.print_exc()
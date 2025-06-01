#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, 'src')

# Set environment
os.environ['PYTHONPATH'] = 'src'

print("Testing Identity unit tests directly...")

try:
    # Import and run the test functions directly
    from tests.unit.test_identity import (
        test_identity_creation,
        test_identity_with_metadata,
        test_identity_scar_creation,
        test_identity_equality,
        test_identity_serialization
    )
    
    print("Running test_identity_creation...")
    test_identity_creation()
    print("✅ test_identity_creation passed")
    
    print("Running test_identity_with_metadata...")
    test_identity_with_metadata()
    print("✅ test_identity_with_metadata passed")
    
    print("Running test_identity_scar_creation...")
    test_identity_scar_creation()
    print("✅ test_identity_scar_creation passed")
    
    print("Running test_identity_equality...")
    test_identity_equality()
    print("✅ test_identity_equality passed")
    
    print("Running test_identity_serialization...")
    test_identity_serialization()
    print("✅ test_identity_serialization passed")
    
    print("\n🎉 All Identity tests passed!")
    
except Exception as e:
    print(f"❌ Identity test failed: {e}")
    import traceback
    traceback.print_exc()
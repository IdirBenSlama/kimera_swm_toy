#!/usr/bin/env python3
"""
CRITICAL SECURITY FIXES VALIDATION
=================================

This test validates that critical security fixes are working correctly.
Tests the 3 CRITICAL vulnerabilities that were blocking production deployment.

TESTS:
1. datetime.utcnow() deprecation fix - Timezone confusion attack prevention
2. Numpy array validation - Memory exhaustion/RCE prevention  
3. Recursion depth limits - Stack overflow/DoS prevention

USAGE: python VALIDATE_CRITICAL_FIXES.py
"""

import sys
import traceback
import numpy as np
from datetime import datetime, timezone

def test_datetime_fix():
    """Test that datetime.utcnow() deprecation is fixed."""
    print("🔍 Testing datetime.utcnow() fix...")
    try:
        from src.kimera.identity import Identity
        
        # Test 1: Create identity and check timezone awareness
        identity = Identity("test content")
        
        # Verify timestamps are timezone-aware
        if identity.created_at.tzinfo is None:
            print("  ❌ FAIL: created_at timestamp is not timezone-aware")
            return False
            
        if identity.updated_at.tzinfo is None:
            print("  ❌ FAIL: updated_at timestamp is not timezone-aware")
            return False
            
        # Test 2: Check that timezone is UTC
        if identity.created_at.tzinfo != timezone.utc:
            print(f"  ❌ FAIL: created_at timezone is {identity.created_at.tzinfo}, expected UTC")
            return False
            
        # Test 3: Test metadata update timestamp
        identity.update_metadata("test_key", "test_value")
        if identity.updated_at.tzinfo != timezone.utc:
            print(f"  ❌ FAIL: updated_at timezone after metadata update is {identity.updated_at.tzinfo}, expected UTC")
            return False
            
        # Test 4: Test tag operations timestamp
        identity.add_tag("test_tag")
        if identity.updated_at.tzinfo != timezone.utc:
            print(f"  ❌ FAIL: updated_at timezone after tag add is {identity.updated_at.tzinfo}, expected UTC")
            return False
            
        identity.remove_tag("test_tag")
        if identity.updated_at.tzinfo != timezone.utc:
            print(f"  ❌ FAIL: updated_at timezone after tag remove is {identity.updated_at.tzinfo}, expected UTC")
            return False
            
        # Test 5: Test SCAR creation
        scar = Identity.create_scar(content="test scar", related_ids=["id1", "id2"])
        if scar.created_at.tzinfo != timezone.utc:
            print(f"  ❌ FAIL: SCAR created_at timezone is {scar.created_at.tzinfo}, expected UTC")
            return False
            
        print("  ✅ PASS: All datetime operations use timezone-aware UTC timestamps")
        return True
        
    except Exception as e:
        print(f"  ❌ ERROR: Datetime fix test failed: {e}")
        traceback.print_exc()
        return False

def test_numpy_validation():
    """Test that numpy validation is working."""
    print("🔍 Testing numpy array validation...")
    try:
        from src.kimera.identity import Identity
        
        # Test 1: Valid small array should pass
        try:
            small_array = np.ones((100,), dtype=np.float64)  # ~800 bytes
            identity = Identity("test", vector=small_array)
            print("  ✅ PASS: Valid small array accepted")
        except Exception as e:
            print(f"  ❌ FAIL: Valid small array rejected: {e}")
            return False
            
        # Test 2: Oversized array should be rejected
        try:
            # Create array larger than 100MB limit
            large_array = np.ones((15000000,), dtype=np.float64)  # ~120MB
            Identity("test", vector=large_array)
            print("  ❌ FAIL: Large array should have been rejected")
            return False
        except ValueError as e:
            if "too large" in str(e).lower():
                print(f"  ✅ PASS: Large array correctly rejected: {e}")
            else:
                print(f"  ❌ FAIL: Large array rejected for wrong reason: {e}")
                return False
        except Exception as e:
            print(f"  ❌ FAIL: Unexpected error with large array: {e}")
            return False
            
        # Test 3: Invalid array type should be rejected
        try:
            Identity("test", vector="not_an_array")
            print("  ❌ FAIL: Non-array should have been rejected")
            return False
        except TypeError as e:
            if "numpy ndarray" in str(e):
                print(f"  ✅ PASS: Non-array correctly rejected: {e}")
            else:
                print(f"  ❌ FAIL: Non-array rejected for wrong reason: {e}")
                return False
        except Exception as e:
            print(f"  ❌ FAIL: Unexpected error with non-array: {e}")
            return False
            
        # Test 4: Array with invalid values should be rejected
        try:
            invalid_array = np.array([1.0, 2.0, np.inf, 4.0])
            Identity("test", vector=invalid_array)
            print("  ❌ FAIL: Array with infinity should have been rejected")
            return False
        except ValueError as e:
            if "invalid values" in str(e).lower():
                print(f"  ✅ PASS: Array with infinity correctly rejected: {e}")
            else:
                print(f"  ❌ FAIL: Array with infinity rejected for wrong reason: {e}")
                return False
        except Exception as e:
            print(f"  ❌ FAIL: Unexpected error with infinity array: {e}")
            return False
            
        # Test 5: Array with NaN should be rejected
        try:
            nan_array = np.array([1.0, 2.0, np.nan, 4.0])
            Identity("test", vector=nan_array)
            print("  ❌ FAIL: Array with NaN should have been rejected")
            return False
        except ValueError as e:
            if "invalid values" in str(e).lower():
                print(f"  ✅ PASS: Array with NaN correctly rejected: {e}")
            else:
                print(f"  ❌ FAIL: Array with NaN rejected for wrong reason: {e}")
                return False
        except Exception as e:
            print(f"  ❌ FAIL: Unexpected error with NaN array: {e}")
            return False
            
        print("  ✅ PASS: All numpy validation tests passed")
        return True
        
    except Exception as e:
        print(f"  ❌ ERROR: Numpy validation test failed: {e}")
        traceback.print_exc()
        return False

def test_recursion_limits():
    """Test that recursion limits are working."""
    print("🔍 Testing recursion depth limits...")
    try:
        from src.kimera.echoform import EchoForm
        
        # Test 1: Normal operation should work
        try:
            echo = EchoForm(anchor="test", domain="test")
            print("  ✅ PASS: Normal EchoForm creation works")
        except Exception as e:
            print(f"  ❌ FAIL: Normal EchoForm creation failed: {e}")
            return False
            
        # Test 2: Check recursion limit enforcement
        try:
            echo = EchoForm()
            
            # Try to exceed recursion limit
            for i in range(150):  # Exceed MAX_RECURSION_DEPTH (100)
                echo._check_recursion_limit()
                
            print("  ❌ FAIL: Recursion limit should have been enforced")
            return False
            
        except RecursionError as e:
            if "Maximum recursion depth" in str(e):
                print(f"  ✅ PASS: Recursion limit correctly enforced: {e}")
            else:
                print(f"  ❌ FAIL: Recursion limit enforced for wrong reason: {e}")
                return False
        except Exception as e:
            print(f"  ❌ FAIL: Unexpected error with recursion test: {e}")
            return False
            
        # Test 3: Reset recursion depth should work
        try:
            echo = EchoForm()
            
            # Use some recursion depth
            for i in range(50):
                echo._check_recursion_limit()
                
            # Reset and try again
            echo._reset_recursion_depth()
            
            # Should be able to use recursion again
            for i in range(50):
                echo._check_recursion_limit()
                
            print("  ✅ PASS: Recursion depth reset works correctly")
            
        except Exception as e:
            print(f"  ❌ FAIL: Recursion depth reset failed: {e}")
            return False
            
        # Test 4: Check security constants are defined
        if not hasattr(EchoForm, 'MAX_RECURSION_DEPTH'):
            print("  ❌ FAIL: MAX_RECURSION_DEPTH constant not defined")
            return False
            
        if EchoForm.MAX_RECURSION_DEPTH != 100:
            print(f"  ❌ FAIL: MAX_RECURSION_DEPTH is {EchoForm.MAX_RECURSION_DEPTH}, expected 100")
            return False
            
        print("  ✅ PASS: All recursion limit tests passed")
        return True
        
    except Exception as e:
        print(f"  ❌ ERROR: Recursion limit test failed: {e}")
        traceback.print_exc()
        return False

def test_additional_security_features():
    """Test additional security features that were implemented."""
    print("🔍 Testing additional security features...")
    try:
        from src.kimera.echoform import EchoForm
        
        # Test 1: Check security constants
        security_constants = [
            ('MAX_RECURSION_DEPTH', 100),
            ('MAX_TERMS', 10000),
            ('MAX_TOPOLOGY_SIZE', 1000000)
        ]
        
        for const_name, expected_value in security_constants:
            if not hasattr(EchoForm, const_name):
                print(f"  ❌ FAIL: Security constant {const_name} not defined")
                return False
            
            actual_value = getattr(EchoForm, const_name)
            if actual_value != expected_value:
                print(f"  ❌ FAIL: {const_name} is {actual_value}, expected {expected_value}")
                return False
                
        print("  ✅ PASS: All security constants defined correctly")
        
        # Test 2: Check security methods exist
        echo = EchoForm()
        security_methods = [
            '_check_recursion_limit',
            '_reset_recursion_depth',
            '_validate_terms_limit',
            '_validate_topology_size'
        ]
        
        for method_name in security_methods:
            if not hasattr(echo, method_name):
                print(f"  ❌ FAIL: Security method {method_name} not defined")
                return False
                
        print("  ✅ PASS: All security methods defined")
        
        # Test 3: Check recursion depth tracking
        if not hasattr(echo, '_recursion_depth'):
            print("  ❌ FAIL: Recursion depth tracking not initialized")
            return False
            
        if echo._recursion_depth != 0:
            print(f"  ❌ FAIL: Initial recursion depth is {echo._recursion_depth}, expected 0")
            return False
            
        print("  ✅ PASS: Recursion depth tracking initialized correctly")
        return True
        
    except Exception as e:
        print(f"  ❌ ERROR: Additional security features test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all critical security fixes validation tests."""
    print("🔒 CRITICAL SECURITY FIXES VALIDATION")
    print("=" * 60)
    print("⚠️  VALIDATING FIXES FOR PRODUCTION-BLOCKING VULNERABILITIES")
    print()
    
    tests = [
        ("Timezone-aware datetime fix", test_datetime_fix),
        ("Numpy array validation", test_numpy_validation),
        ("Recursion depth limits", test_recursion_limits),
        ("Additional security features", test_additional_security_features)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"🧪 Running: {test_name}")
        if test_func():
            passed += 1
            print(f"✅ {test_name}: PASSED")
        else:
            print(f"❌ {test_name}: FAILED")
        print()
    
    print("=" * 60)
    print("🔒 CRITICAL SECURITY FIXES VALIDATION SUMMARY")
    print("=" * 60)
    
    print(f"📊 Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🟢 ALL CRITICAL SECURITY FIXES VALIDATED SUCCESSFULLY")
        print("🚀 PRODUCTION DEPLOYMENT SECURITY REQUIREMENTS MET")
        print("📋 Next Steps:")
        print("  • Proceed to Phase 2 (High Priority Fixes)")
        print("  • Implement comprehensive security framework")
        print("  • Conduct full security audit")
        return True
    else:
        print(f"\n🔴 {total - passed} CRITICAL SECURITY FIXES FAILED VALIDATION")
        print("🚨 PRODUCTION DEPLOYMENT REMAINS BLOCKED")
        print("📋 Required Actions:")
        print("  • Fix failed security validations")
        print("  • Re-run validation tests")
        print("  • Do not proceed to production until all tests pass")
        return False

if __name__ == "__main__":
    print("⚠️  CRITICAL SECURITY VALIDATION - PRODUCTION DEPLOYMENT GATE")
    print("🔒 This validation determines if critical security fixes are working")
    print()
    
    success = main()
    
    if success:
        print("\n🎉 CRITICAL SECURITY VALIDATION: PASSED")
        print("🟢 Production deployment security gate: OPEN")
    else:
        print("\n💥 CRITICAL SECURITY VALIDATION: FAILED")
        print("🔴 Production deployment security gate: BLOCKED")
    
    sys.exit(0 if success else 1)
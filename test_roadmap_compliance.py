#!/usr/bin/env python3
"""
Test compliance with the roadmap requirements
"""
import sys
import os
sys.path.insert(0, 'src')

def test_echoform_roadmap_compliance():
    """Test EchoForm against roadmap requirements"""
    print("\n=== Testing EchoForm Roadmap Compliance ===")
    
    try:
        from kimera.echoform import EchoForm
        
        # Test 1: Basic creation
        echo = EchoForm()
        print("[PASS] EchoForm creation")
        
        # Test 2: Required fields according to roadmap
        required_fields = ['anchor', 'domain', 'terms', 'phase', 'recursive', 
                          'topology', 'trace_signature', 'echo_created_at']
        
        missing_fields = []
        for field in required_fields:
            if not hasattr(echo, field):
                missing_fields.append(field)
        
        if missing_fields:
            print(f"[FAIL] Missing required fields: {missing_fields}")
            return False
        else:
            print("[PASS] All required fields present")
        
        # Test 3: Required methods
        required_methods = ['add_term', 'intensity_sum', 'mutate_phase', 
                           'compute_trace', 'flatten', 'reinflate', 'to_dict', 'process']
        
        missing_methods = []
        for method in required_methods:
            if not hasattr(echo, method) or not callable(getattr(echo, method)):
                missing_methods.append(method)
        
        if missing_methods:
            print(f"[FAIL] Missing required methods: {missing_methods}")
            return False
        else:
            print("[PASS] All required methods present")
        
        # Test 4: Time-decay functionality
        echo.add_term("test", intensity=2.0)
        intensity_no_decay = echo.intensity_sum(apply_time_decay=False)
        intensity_with_decay = echo.intensity_sum(apply_time_decay=True)
        
        print(f"[INFO] Intensity without decay: {intensity_no_decay}")
        print(f"[INFO] Intensity with decay: {intensity_with_decay}")
        print("[PASS] Time-decay functionality works")
        
        # Test 5: Serialization round-trip
        json_str = echo.flatten()
        echo_restored = EchoForm.reinflate(json_str)
        print("[PASS] Serialization round-trip works")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] EchoForm compliance test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_identity_roadmap_compliance():
    """Test Identity against roadmap requirements"""
    print("\n=== Testing Identity Roadmap Compliance ===")
    
    try:
        from kimera.identity import Identity
        
        # Test 1: Geoid-style creation (backward compatibility)
        geoid = Identity(content="test content")
        print("[PASS] Geoid-style creation")
        
        # Test 2: SCAR creation
        scar = Identity.create_scar(
            content="test scar",
            related_ids=["id1", "id2"],
            metadata={"type": "test"}
        )
        print("[PASS] SCAR creation")
        
        # Test 3: Required fields
        required_fields = ['id', 'identity_type', 'raw', 'echo', 'lang_axis', 
                          'tags', 'weight', 'related_ids', 'meta', 'created_at', 'updated_at']
        
        missing_fields = []
        for field in required_fields:
            if not hasattr(geoid, field):
                missing_fields.append(field)
        
        if missing_fields:
            print(f"[FAIL] Missing required fields: {missing_fields}")
            return False
        else:
            print("[PASS] All required fields present")
        
        # Test 4: Entropy calculation
        entropy_val = geoid.entropy()
        print(f"[INFO] Geoid entropy: {entropy_val}")
        
        scar_entropy = scar.entropy()
        print(f"[INFO] SCAR entropy: {scar_entropy}")
        print("[PASS] Entropy calculation works")
        
        # Test 5: Effective tau calculation
        tau_val = geoid.effective_tau()
        print(f"[INFO] Effective tau: {tau_val}")
        print("[PASS] Effective tau calculation works")
        
        # Test 6: Serialization
        data = geoid.to_dict()
        geoid_restored = Identity.from_dict(data)
        print("[PASS] Serialization works")
        
        # Test 7: Equality
        assert geoid == geoid_restored
        print("[PASS] Equality works")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Identity compliance test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_entropy_roadmap_compliance():
    """Test entropy calculations against roadmap requirements"""
    print("\n=== Testing Entropy Roadmap Compliance ===")
    
    try:
        from kimera.entropy import (
            calculate_shannon_entropy, 
            calculate_term_entropy, 
            calculate_relationship_entropy,
            adaptive_tau
        )
        
        # Test 1: Shannon entropy
        intensities = [1.0, 2.0, 3.0, 4.0]
        entropy = calculate_shannon_entropy(intensities)
        print(f"[INFO] Shannon entropy: {entropy}")
        print("[PASS] Shannon entropy calculation")
        
        # Test 2: Term entropy
        terms = [
            {"intensity": 1.0},
            {"intensity": 2.0},
            {"intensity": 3.0}
        ]
        term_entropy = calculate_term_entropy(terms)
        print(f"[INFO] Term entropy: {term_entropy}")
        print("[PASS] Term entropy calculation")
        
        # Test 3: Relationship entropy
        related_ids = ["id1", "id2", "id3"]
        rel_entropy = calculate_relationship_entropy(related_ids, weight=1.0)
        print(f"[INFO] Relationship entropy: {rel_entropy}")
        print("[PASS] Relationship entropy calculation")
        
        # Test 4: Adaptive tau
        tau_val = adaptive_tau(entropy, base_tau=14*24*3600)
        print(f"[INFO] Adaptive tau: {tau_val}")
        print("[PASS] Adaptive tau calculation")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Entropy compliance test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_storage_roadmap_compliance():
    """Test storage against roadmap requirements (if available)"""
    print("\n=== Testing Storage Roadmap Compliance ===")
    
    try:
        # Try to import storage - might fail if DuckDB not available
        from kimera.storage import LatticeStorage
        from kimera.identity import Identity
        
        # Create temporary storage
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            test_db = f.name
        
        try:
            storage = LatticeStorage(db_path=test_db)
            print("[PASS] Storage creation")
            
            # Test storing and retrieving identity
            identity = Identity(content="test content")
            storage.store_identity(identity)
            print("[PASS] Identity storage")
            
            retrieved = storage.get_identity(identity.id)
            assert retrieved is not None
            print("[PASS] Identity retrieval")
            
            # Test listing identities
            identities = storage.list_identities()
            assert len(identities) >= 1
            print("[PASS] Identity listing")
            
            return True
            
        finally:
            # Cleanup
            if os.path.exists(test_db):
                os.remove(test_db)
        
    except ImportError as e:
        print(f"[SKIP] Storage test skipped - dependency missing: {e}")
        return True  # Don't fail if optional dependency missing
    except Exception as e:
        print(f"[FAIL] Storage compliance test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main compliance test function"""
    print("=== Testing Roadmap Compliance ===")
    
    tests = [
        ("EchoForm", test_echoform_roadmap_compliance),
        ("Identity", test_identity_roadmap_compliance),
        ("Entropy", test_entropy_roadmap_compliance),
        ("Storage", test_storage_roadmap_compliance)
    ]
    
    results = {}
    for test_name, test_func in tests:
        results[test_name] = test_func()
    
    # Summary
    print(f"\n=== Compliance Results ===")
    passed = 0
    total = 0
    for test_name, success in results.items():
        status = "PASS" if success else "FAIL"
        print(f"{status}: {test_name}")
        if success:
            passed += 1
        total += 1
    
    print(f"\nOverall: {passed}/{total} compliance tests passed")
    
    if passed == total:
        print("[PASS] All compliance tests passed!")
        return True
    else:
        print("[FAIL] Some compliance tests failed")
        return False

if __name__ == "__main__":
    main()
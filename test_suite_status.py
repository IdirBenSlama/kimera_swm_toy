#!/usr/bin/env python3
"""
Comprehensive test suite status report
"""
import sys
import os
sys.path.insert(0, 'src')

def test_imports():
    """Test all core imports"""
    print("\n=== Testing Imports ===")
    results = {}
    
    # Core imports
    core_imports = [
        ('kimera.echoform', 'EchoForm'),
        ('kimera.identity', 'Identity'),
        ('kimera.entropy', 'calculate_shannon_entropy'),
        ('kimera.entropy', 'adaptive_tau'),
    ]
    
    for module, item in core_imports:
        try:
            exec(f"from {module} import {item}")
            print(f"[PASS] {module}.{item}")
            results[f"{module}.{item}"] = True
        except Exception as e:
            print(f"[FAIL] {module}.{item}: {e}")
            results[f"{module}.{item}"] = False
    
    # Optional imports
    optional_imports = [
        ('kimera.storage', 'LatticeStorage'),
        ('kimera.geoid', 'Geoid'),
        ('kimera.cache', 'embed_cache'),
    ]
    
    for module, item in optional_imports:
        try:
            exec(f"from {module} import {item}")
            print(f"[PASS] {module}.{item} (optional)")
            results[f"{module}.{item}"] = True
        except Exception as e:
            print(f"[SKIP] {module}.{item} (optional): {e}")
            results[f"{module}.{item}"] = False
    
    return results

def test_echoform_functionality():
    """Test EchoForm functionality against roadmap"""
    print("\n=== Testing EchoForm Functionality ===")
    results = {}
    
    try:
        from kimera.echoform import EchoForm
        
        # Test 1: Basic creation
        echo = EchoForm()
        results['echoform_creation'] = True
        print("[PASS] EchoForm creation")
        
        # Test 2: Required fields
        required_fields = ['anchor', 'domain', 'terms', 'phase', 'recursive', 
                          'topology', 'trace_signature', 'echo_created_at']
        missing_fields = [f for f in required_fields if not hasattr(echo, f)]
        if missing_fields:
            print(f"[FAIL] Missing fields: {missing_fields}")
            results['echoform_fields'] = False
        else:
            print("[PASS] All required fields present")
            results['echoform_fields'] = True
        
        # Test 3: Required methods
        required_methods = ['add_term', 'intensity_sum', 'mutate_phase', 
                           'compute_trace', 'flatten', 'reinflate', 'to_dict', 'process']
        missing_methods = [m for m in required_methods 
                          if not hasattr(echo, m) or not callable(getattr(echo, m))]
        if missing_methods:
            print(f"[FAIL] Missing methods: {missing_methods}")
            results['echoform_methods'] = False
        else:
            print("[PASS] All required methods present")
            results['echoform_methods'] = True
        
        # Test 4: Time-decay functionality
        echo.add_term("test", intensity=2.0)
        intensity_no_decay = echo.intensity_sum(apply_time_decay=False)
        intensity_with_decay = echo.intensity_sum(apply_time_decay=True)
        print(f"[INFO] Intensity: no decay={intensity_no_decay}, with decay={intensity_with_decay}")
        results['echoform_time_decay'] = True
        print("[PASS] Time-decay functionality")
        
        # Test 5: Serialization
        json_str = echo.flatten()
        echo_restored = EchoForm.reinflate(json_str)
        results['echoform_serialization'] = True
        print("[PASS] Serialization")
        
    except Exception as e:
        print(f"[FAIL] EchoForm functionality: {e}")
        import traceback
        traceback.print_exc()
        results['echoform_functionality'] = False
    
    return results

def test_identity_functionality():
    """Test Identity functionality against roadmap"""
    print("\n=== Testing Identity Functionality ===")
    results = {}
    
    try:
        from kimera.identity import Identity
        
        # Test 1: Geoid-style creation
        geoid = Identity(content="test content")
        results['identity_geoid_creation'] = True
        print("[PASS] Geoid-style creation")
        
        # Test 2: SCAR creation
        scar = Identity.create_scar(
            content="test scar",
            related_ids=["id1", "id2"],
            metadata={"type": "test"}
        )
        results['identity_scar_creation'] = True
        print("[PASS] SCAR creation")
        
        # Test 3: Required fields
        required_fields = ['id', 'identity_type', 'raw', 'echo', 'lang_axis', 
                          'tags', 'weight', 'related_ids', 'meta', 'created_at', 'updated_at']
        missing_fields = [f for f in required_fields if not hasattr(geoid, f)]
        if missing_fields:
            print(f"[FAIL] Missing fields: {missing_fields}")
            results['identity_fields'] = False
        else:
            print("[PASS] All required fields present")
            results['identity_fields'] = True
        
        # Test 4: Entropy calculation
        entropy_val = geoid.entropy()
        print(f"[INFO] Geoid entropy: {entropy_val}")
        scar_entropy = scar.entropy()
        print(f"[INFO] SCAR entropy: {scar_entropy}")
        results['identity_entropy'] = True
        print("[PASS] Entropy calculation")
        
        # Test 5: Effective tau
        tau_val = geoid.effective_tau()
        print(f"[INFO] Effective tau: {tau_val}")
        results['identity_tau'] = True
        print("[PASS] Effective tau calculation")
        
        # Test 6: Serialization
        data = geoid.to_dict()
        geoid_restored = Identity.from_dict(data)
        assert geoid == geoid_restored
        results['identity_serialization'] = True
        print("[PASS] Serialization and equality")
        
    except Exception as e:
        print(f"[FAIL] Identity functionality: {e}")
        import traceback
        traceback.print_exc()
        results['identity_functionality'] = False
    
    return results

def test_entropy_functionality():
    """Test entropy functionality against roadmap"""
    print("\n=== Testing Entropy Functionality ===")
    results = {}
    
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
        results['entropy_shannon'] = True
        print("[PASS] Shannon entropy")
        
        # Test 2: Term entropy
        terms = [{"intensity": 1.0}, {"intensity": 2.0}, {"intensity": 3.0}]
        term_entropy = calculate_term_entropy(terms)
        print(f"[INFO] Term entropy: {term_entropy}")
        results['entropy_term'] = True
        print("[PASS] Term entropy")
        
        # Test 3: Relationship entropy
        related_ids = ["id1", "id2", "id3"]
        rel_entropy = calculate_relationship_entropy(related_ids, weight=1.0)
        print(f"[INFO] Relationship entropy: {rel_entropy}")
        results['entropy_relationship'] = True
        print("[PASS] Relationship entropy")
        
        # Test 4: Adaptive tau
        tau_val = adaptive_tau(14*24*3600, entropy)
        print(f"[INFO] Adaptive tau: {tau_val}")
        results['entropy_adaptive_tau'] = True
        print("[PASS] Adaptive tau")
        
    except Exception as e:
        print(f"[FAIL] Entropy functionality: {e}")
        import traceback
        traceback.print_exc()
        results['entropy_functionality'] = False
    
    return results

def test_storage_functionality():
    """Test storage functionality (if available)"""
    print("\n=== Testing Storage Functionality ===")
    results = {}
    
    try:
        from kimera.storage import LatticeStorage
        from kimera.identity import Identity
        import tempfile
        
        # Create temporary storage
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            test_db = f.name
        
        try:
            storage = LatticeStorage(db_path=test_db)
            results['storage_creation'] = True
            print("[PASS] Storage creation")
            
            # Test storing identity
            identity = Identity(content="test content")
            storage.store_identity(identity)
            results['storage_store'] = True
            print("[PASS] Identity storage")
            
            # Test retrieving identity
            retrieved = storage.get_identity(identity.id)
            assert retrieved is not None
            results['storage_retrieve'] = True
            print("[PASS] Identity retrieval")
            
            # Test listing identities
            identities = storage.list_identities()
            assert len(identities) >= 1
            results['storage_list'] = True
            print("[PASS] Identity listing")
            
        finally:
            if os.path.exists(test_db):
                os.remove(test_db)
        
    except ImportError:
        print("[SKIP] Storage functionality - DuckDB not available")
        results['storage_functionality'] = None
    except Exception as e:
        print(f"[FAIL] Storage functionality: {e}")
        import traceback
        traceback.print_exc()
        results['storage_functionality'] = False
    
    return results

def generate_status_report(all_results):
    """Generate a comprehensive status report"""
    print("\n" + "="*60)
    print("COMPREHENSIVE TEST SUITE STATUS REPORT")
    print("="*60)
    
    # Count results
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    skipped_tests = 0
    
    for category, results in all_results.items():
        print(f"\n{category.upper()}:")
        for test_name, result in results.items():
            total_tests += 1
            if result is True:
                print(f"  [PASS] {test_name}")
                passed_tests += 1
            elif result is False:
                print(f"  [FAIL] {test_name}")
                failed_tests += 1
            else:
                print(f"  [SKIP] {test_name}")
                skipped_tests += 1
    
    print(f"\n" + "="*60)
    print(f"SUMMARY:")
    print(f"  Total tests: {total_tests}")
    print(f"  Passed: {passed_tests}")
    print(f"  Failed: {failed_tests}")
    print(f"  Skipped: {skipped_tests}")
    print(f"  Success rate: {passed_tests/total_tests*100:.1f}%")
    
    # Roadmap compliance assessment
    print(f"\nROADMAP COMPLIANCE ASSESSMENT:")
    
    # Core functionality assessment
    core_functionality = [
        'echoform_creation', 'echoform_fields', 'echoform_methods',
        'identity_geoid_creation', 'identity_scar_creation', 'identity_fields',
        'entropy_shannon', 'entropy_term', 'entropy_relationship'
    ]
    
    core_passed = sum(1 for test in core_functionality 
                     if any(results.get(test, False) for results in all_results.values()))
    core_total = len(core_functionality)
    
    print(f"  Core functionality: {core_passed}/{core_total} ({core_passed/core_total*100:.1f}%)")
    
    if core_passed == core_total:
        print("  Status: READY FOR PHASE 2")
    elif core_passed >= core_total * 0.8:
        print("  Status: MOSTLY READY - Minor fixes needed")
    else:
        print("  Status: NEEDS WORK - Major issues to resolve")
    
    return passed_tests == total_tests

def main():
    """Main status report function"""
    print("KIMERA-SWM TOY IMPLEMENTATION")
    print("Test Suite Status Report")
    print("="*60)
    
    all_results = {}
    
    # Run all test categories
    all_results['imports'] = test_imports()
    all_results['echoform'] = test_echoform_functionality()
    all_results['identity'] = test_identity_functionality()
    all_results['entropy'] = test_entropy_functionality()
    all_results['storage'] = test_storage_functionality()
    
    # Generate comprehensive report
    success = generate_status_report(all_results)
    
    return success

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
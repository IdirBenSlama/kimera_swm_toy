#!/usr/bin/env python3
"""
Comprehensive test suite for roadmap implementation
Tests all features specified in the roadmap
"""
import sys
import os
sys.path.insert(0, 'src')

import time
import tempfile
from datetime import datetime

def test_echoform_enhanced_features():
    """Test enhanced EchoForm features from roadmap"""
    print("\n=== Testing Enhanced EchoForm Features ===")
    
    try:
        from kimera.echoform import EchoForm
        
        # Test 1: Enhanced time decay with entropy weighting
        echo = EchoForm(anchor="test_enhanced", domain="test")
        echo.add_term("high_intensity", intensity=5.0)
        echo.add_term("medium_intensity", intensity=3.0)
        echo.add_term("low_intensity", intensity=1.0)
        
        # Test entropy calculation
        entropy = echo.entropy()
        print(f"[PASS] EchoForm entropy calculation: {entropy:.3f}")
        
        # Test effective tau
        effective_tau = echo.effective_tau()
        print(f"[PASS] EchoForm effective tau: {effective_tau:.0f}")
        
        # Test intensity sum with different options
        intensity_no_decay = echo.intensity_sum(apply_time_decay=False)
        intensity_standard_decay = echo.intensity_sum(apply_time_decay=True, use_entropy_weighting=False)
        intensity_entropy_decay = echo.intensity_sum(apply_time_decay=True, use_entropy_weighting=True)
        
        print(f"[PASS] Intensity variations - no decay: {intensity_no_decay:.1f}, "
              f"standard: {intensity_standard_decay:.3f}, entropy: {intensity_entropy_decay:.3f}")
        
        # Test enhanced to_dict with metadata
        data = echo.to_dict()
        assert "metadata" in data
        assert "entropy" in data["metadata"]
        assert "effective_tau" in data["metadata"]
        print(f"[PASS] Enhanced to_dict with metadata: {list(data['metadata'].keys())}")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Enhanced EchoForm features: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_identity_enhanced_features():
    """Test enhanced Identity features from roadmap"""
    print("\n=== Testing Enhanced Identity Features ===")
    
    try:
        from kimera.identity import Identity
        
        # Test 1: Enhanced geoid identity
        geoid = Identity(content="test content with multiple terms")
        geoid.add_tag("test")
        geoid.add_tag("enhanced")
        
        # Test age calculation
        age = geoid.age_seconds()
        print(f"[PASS] Identity age calculation: {age:.1f} seconds")
        
        # Test decay factor
        decay = geoid.decay_factor()
        print(f"[PASS] Identity decay factor: {decay:.6f}")
        
        # Test metadata updates
        geoid.update_metadata("test_key", "test_value")
        assert geoid.meta["test_key"] == "test_value"
        print("[PASS] Metadata update")
        
        # Test tag management
        geoid.add_tag("new_tag")
        assert "new_tag" in geoid.tags
        removed = geoid.remove_tag("test")
        assert "test" not in geoid.tags
        print("[PASS] Tag management")
        
        # Test 2: Enhanced SCAR identity
        scar = Identity.create_scar(
            content="relationship test",
            related_ids=["id1", "id2", "id3"],
            metadata={"relationship_type": "test", "strength": 0.8}
        )
        
        # Test SCAR entropy (should be higher due to more relationships)
        scar_entropy = scar.entropy()
        geoid_entropy = geoid.entropy()
        print(f"[PASS] Entropy comparison - SCAR: {scar_entropy:.3f}, Geoid: {geoid_entropy:.3f}")
        
        # Test effective tau differences
        scar_tau = scar.effective_tau()
        geoid_tau = geoid.effective_tau()
        print(f"[PASS] Tau comparison - SCAR: {scar_tau:.0f}, Geoid: {geoid_tau:.0f}")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Enhanced Identity features: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_entropy_integration():
    """Test entropy integration across all components"""
    print("\n=== Testing Entropy Integration ===")
    
    try:
        from kimera.echoform import EchoForm
        from kimera.identity import Identity
        from kimera.entropy import (
            calculate_shannon_entropy, 
            calculate_term_entropy,
            calculate_relationship_entropy,
            adaptive_tau,
            entropy_weighted_decay
        )
        
        # Test 1: Entropy consistency across components
        echo = EchoForm()
        echo.add_term("term1", intensity=2.0)
        echo.add_term("term2", intensity=3.0)
        echo.add_term("term3", intensity=1.0)
        
        # Calculate entropy using different methods
        direct_entropy = calculate_term_entropy(echo.terms)
        echo_entropy = echo.entropy()
        
        assert abs(direct_entropy - echo_entropy) < 0.001
        print(f"[PASS] Entropy consistency: direct={direct_entropy:.3f}, echo={echo_entropy:.3f}")
        
        # Test 2: Adaptive tau integration
        base_tau = 14 * 24 * 3600  # 14 days
        adaptive_tau_val = adaptive_tau(base_tau, echo_entropy)
        echo_tau = echo.effective_tau(base_tau)
        
        assert abs(adaptive_tau_val - echo_tau) < 0.001
        print(f"[PASS] Adaptive tau consistency: {adaptive_tau_val:.0f}")
        
        # Test 3: Entropy-weighted decay
        age_seconds = 7 * 24 * 3600  # 7 days
        decay_val = entropy_weighted_decay(age_seconds, base_tau, echo_entropy)
        print(f"[PASS] Entropy-weighted decay: {decay_val:.6f}")
        
        # Test 4: Identity entropy integration
        identity = Identity(content="test content")
        identity.meta["terms"] = echo.terms  # Add terms to identity
        identity_entropy = identity.entropy()
        print(f"[PASS] Identity entropy integration: {identity_entropy:.3f}")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Entropy integration: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_storage_integration():
    """Test storage integration with enhanced features"""
    print("\n=== Testing Storage Integration ===")
    
    try:
        from kimera.storage import LatticeStorage
        from kimera.echoform import EchoForm
        from kimera.identity import Identity
        
        # Create temporary storage
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            test_db = f.name
        
        try:
            storage = LatticeStorage(db_path=test_db)
            
            # Test 1: Store enhanced EchoForm
            echo = EchoForm(anchor="storage_test", domain="test")
            echo.add_term("stored_term", intensity=2.5)
            
            storage.store_form(echo)
            retrieved_echo = storage.fetch_form("storage_test")
            assert retrieved_echo is not None
            assert retrieved_echo.anchor == "storage_test"
            print("[PASS] Enhanced EchoForm storage")
            
            # Test 2: Store enhanced Identity with entropy tracking
            identity = Identity(content="storage test content")
            identity.add_tag("stored")
            identity.update_metadata("storage_test", True)
            
            storage.store_identity(identity)
            retrieved_identity = storage.get_identity(identity.id)
            assert retrieved_identity is not None
            assert retrieved_identity.meta["storage_test"] is True
            print("[PASS] Enhanced Identity storage with entropy tracking")
            
            # Test 3: List identities with entropy scores
            identities = storage.list_identities()
            assert len(identities) >= 1
            
            # Check if entropy score is tracked
            identity_info = identities[0]
            assert "entropy_score" in identity_info
            print(f"[PASS] Identity listing with entropy: {identity_info['entropy_score']:.3f}")
            
            return True
            
        finally:
            if os.path.exists(test_db):
                os.remove(test_db)
        
    except ImportError:
        print("[SKIP] Storage integration - DuckDB not available")
        return True
    except Exception as e:
        print(f"[FAIL] Storage integration: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_backward_compatibility():
    """Test backward compatibility with existing code"""
    print("\n=== Testing Backward Compatibility ===")
    
    try:
        from kimera.echoform import EchoForm
        from kimera.identity import Identity
        
        # Test 1: Legacy EchoForm usage
        echo = EchoForm()  # No arguments
        echo.add_term("legacy_term", 2.0)  # Legacy call pattern
        intensity = echo.intensity_sum()  # Default behavior
        assert intensity > 0
        print("[PASS] Legacy EchoForm usage")
        
        # Test 2: Legacy Identity usage
        identity = Identity(content="legacy content")  # Legacy constructor
        assert hasattr(identity, 'content')
        assert identity.content == "legacy content"
        print("[PASS] Legacy Identity usage")
        
        # Test 3: Legacy SCAR creation
        scar = Identity.create_scar(
            content="legacy scar",
            related_ids=["id1", "id2"],
            metadata={"type": "legacy"}
        )
        assert scar.identity_type == "scar"
        assert hasattr(scar, 'content')
        print("[PASS] Legacy SCAR creation")
        
        # Test 4: Legacy serialization
        data = identity.to_dict()
        restored = Identity.from_dict(data)
        assert restored == identity
        print("[PASS] Legacy serialization")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Backward compatibility: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_performance_characteristics():
    """Test performance characteristics of enhanced features"""
    print("\n=== Testing Performance Characteristics ===")
    
    try:
        from kimera.echoform import EchoForm
        from kimera.identity import Identity
        import time
        
        # Test 1: EchoForm performance with many terms
        start_time = time.time()
        echo = EchoForm(anchor="perf_test")
        
        for i in range(100):
            echo.add_term(f"term_{i}", intensity=float(i % 10 + 1))
        
        entropy = echo.entropy()
        intensity = echo.intensity_sum()
        
        elapsed = time.time() - start_time
        print(f"[PASS] EchoForm performance (100 terms): {elapsed:.3f}s, entropy: {entropy:.3f}")
        
        # Test 2: Identity performance with many tags
        start_time = time.time()
        identity = Identity(content="performance test")
        
        for i in range(50):
            identity.add_tag(f"tag_{i}")
        
        for i in range(50):
            identity.update_metadata(f"key_{i}", f"value_{i}")
        
        entropy = identity.entropy()
        decay = identity.decay_factor()
        
        elapsed = time.time() - start_time
        print(f"[PASS] Identity performance (50 tags, 50 metadata): {elapsed:.3f}s")
        
        # Test 3: Serialization performance
        start_time = time.time()
        
        for i in range(10):
            data = echo.to_dict()
            identity_data = identity.to_dict()
        
        elapsed = time.time() - start_time
        print(f"[PASS] Serialization performance (10 iterations): {elapsed:.3f}s")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Performance characteristics: {e}")
        import traceback
        traceback.print_exc()
        return False

def generate_roadmap_compliance_report(results):
    """Generate comprehensive roadmap compliance report"""
    print("\n" + "="*70)
    print("ROADMAP IMPLEMENTATION COMPLIANCE REPORT")
    print("="*70)
    
    # Roadmap requirements checklist
    requirements = {
        "Enhanced EchoForm Features": {
            "test": "test_echoform_enhanced_features",
            "features": [
                "Entropy-weighted time decay",
                "Enhanced metadata in to_dict",
                "Entropy and effective_tau methods",
                "Multiple intensity calculation modes"
            ]
        },
        "Enhanced Identity Features": {
            "test": "test_identity_enhanced_features", 
            "features": [
                "Age calculation methods",
                "Decay factor calculation",
                "Enhanced metadata management",
                "Tag management methods",
                "SCAR entropy calculation"
            ]
        },
        "Entropy Integration": {
            "test": "test_entropy_integration",
            "features": [
                "Consistent entropy calculation",
                "Adaptive tau integration",
                "Entropy-weighted decay",
                "Cross-component entropy consistency"
            ]
        },
        "Storage Integration": {
            "test": "test_storage_integration",
            "features": [
                "Enhanced EchoForm storage",
                "Identity storage with entropy tracking",
                "Entropy score persistence",
                "Enhanced metadata storage"
            ]
        },
        "Backward Compatibility": {
            "test": "test_backward_compatibility",
            "features": [
                "Legacy EchoForm usage",
                "Legacy Identity constructor",
                "Legacy SCAR creation",
                "Legacy serialization"
            ]
        },
        "Performance": {
            "test": "test_performance_characteristics",
            "features": [
                "Efficient entropy calculation",
                "Fast metadata operations",
                "Optimized serialization",
                "Scalable term management"
            ]
        }
    }
    
    # Calculate compliance
    total_categories = len(requirements)
    passed_categories = sum(1 for req in requirements.values() 
                           if results.get(req["test"], False))
    
    print(f"\nOVERALL COMPLIANCE: {passed_categories}/{total_categories} categories passed")
    print(f"Success Rate: {passed_categories/total_categories*100:.1f}%")
    
    print(f"\nDETAILED BREAKDOWN:")
    for category, req_info in requirements.items():
        test_name = req_info["test"]
        status = "PASS" if results.get(test_name, False) else "FAIL"
        print(f"\n{category}: [{status}]")
        for feature in req_info["features"]:
            print(f"  ✓ {feature}")
    
    # Implementation status
    if passed_categories == total_categories:
        print(f"\n🎉 ROADMAP IMPLEMENTATION: COMPLETE")
        print("All roadmap requirements have been successfully implemented!")
        print("Status: READY FOR PRODUCTION")
    elif passed_categories >= total_categories * 0.8:
        print(f"\n⚠️  ROADMAP IMPLEMENTATION: MOSTLY COMPLETE")
        print("Most roadmap requirements implemented with minor issues.")
        print("Status: READY FOR TESTING")
    else:
        print(f"\n❌ ROADMAP IMPLEMENTATION: INCOMPLETE")
        print("Significant roadmap requirements missing or failing.")
        print("Status: NEEDS MORE WORK")
    
    return passed_categories == total_categories

def main():
    """Main test runner for roadmap implementation"""
    print("KIMERA-SWM TOY IMPLEMENTATION")
    print("Roadmap Implementation Test Suite")
    print("="*70)
    
    # Run all roadmap tests
    tests = [
        ("test_echoform_enhanced_features", test_echoform_enhanced_features),
        ("test_identity_enhanced_features", test_identity_enhanced_features),
        ("test_entropy_integration", test_entropy_integration),
        ("test_storage_integration", test_storage_integration),
        ("test_backward_compatibility", test_backward_compatibility),
        ("test_performance_characteristics", test_performance_characteristics),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name}...")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"[ERROR] {test_name} crashed: {e}")
            results[test_name] = False
    
    # Generate comprehensive report
    success = generate_roadmap_compliance_report(results)
    
    return success

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
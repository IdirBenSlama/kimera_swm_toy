#!/usr/bin/env python3
"""
Test only core functionality (no external dependencies)
"""
import sys
sys.path.insert(0, 'src')

def test_core_imports():
    """Test core imports"""
    print("=== Testing Core Imports ===")
    
    try:
        from kimera.echoform import EchoForm
        print("[PASS] EchoForm import")
    except Exception as e:
        print(f"[FAIL] EchoForm import: {e}")
        return False
    
    try:
        from kimera.identity import Identity
        print("[PASS] Identity import")
    except Exception as e:
        print(f"[FAIL] Identity import: {e}")
        return False
    
    try:
        from kimera.entropy import calculate_shannon_entropy, adaptive_tau
        print("[PASS] Entropy imports")
    except Exception as e:
        print(f"[FAIL] Entropy imports: {e}")
        return False
    
    return True

def test_echoform_core():
    """Test EchoForm core functionality"""
    print("\n=== Testing EchoForm Core ===")
    
    try:
        from kimera.echoform import EchoForm
        
        # Create EchoForm
        echo = EchoForm()
        print(f"[PASS] EchoForm creation - anchor: {echo.anchor}")
        
        # Add terms
        echo.add_term("test", intensity=2.0)
        echo.add_term("another", intensity=3.0, role="primary")
        print(f"[PASS] Added terms - count: {len(echo.terms)}")
        
        # Test intensity sum
        total_intensity = echo.intensity_sum()
        print(f"[PASS] Intensity sum: {total_intensity}")
        
        # Test time decay
        intensity_no_decay = echo.intensity_sum(apply_time_decay=False)
        intensity_with_decay = echo.intensity_sum(apply_time_decay=True)
        print(f"[PASS] Time decay - no decay: {intensity_no_decay}, with decay: {intensity_with_decay}")
        
        # Test serialization
        json_str = echo.flatten()
        echo_restored = EchoForm.reinflate(json_str)
        print(f"[PASS] Serialization - restored anchor: {echo_restored.anchor}")
        
        # Test to_dict
        data = echo.to_dict()
        print(f"[PASS] to_dict - keys: {list(data.keys())}")
        
        # Test process
        result = echo.process("test input")
        print(f"[PASS] Process - result: {result['processed']}")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] EchoForm core: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_identity_core():
    """Test Identity core functionality"""
    print("\n=== Testing Identity Core ===")
    
    try:
        from kimera.identity import Identity
        
        # Test geoid-style creation
        geoid = Identity(content="test content")
        print(f"[PASS] Geoid creation - ID: {geoid.id}")
        
        # Test SCAR creation
        scar = Identity.create_scar(
            content="test scar",
            related_ids=["id1", "id2"],
            metadata={"type": "test"}
        )
        print(f"[PASS] SCAR creation - ID: {scar.id}")
        
        # Test entropy
        geoid_entropy = geoid.entropy()
        scar_entropy = scar.entropy()
        print(f"[PASS] Entropy - geoid: {geoid_entropy:.3f}, scar: {scar_entropy:.3f}")
        
        # Test effective tau
        geoid_tau = geoid.effective_tau()
        scar_tau = scar.effective_tau()
        print(f"[PASS] Effective tau - geoid: {geoid_tau:.0f}, scar: {scar_tau:.0f}")
        
        # Test serialization
        geoid_data = geoid.to_dict()
        geoid_restored = Identity.from_dict(geoid_data)
        print(f"[PASS] Geoid serialization - restored ID: {geoid_restored.id}")
        
        scar_data = scar.to_dict()
        scar_restored = Identity.from_dict(scar_data)
        print(f"[PASS] SCAR serialization - restored ID: {scar_restored.id}")
        
        # Test equality
        assert geoid == geoid_restored
        assert scar == scar_restored
        print("[PASS] Equality checks")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Identity core: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_entropy_core():
    """Test entropy core functionality"""
    print("\n=== Testing Entropy Core ===")
    
    try:
        from kimera.entropy import (
            calculate_shannon_entropy, 
            calculate_term_entropy, 
            calculate_relationship_entropy,
            adaptive_tau,
            decay_factor,
            entropy_weighted_decay
        )
        
        # Test Shannon entropy
        intensities = [1.0, 2.0, 3.0, 4.0]
        entropy = calculate_shannon_entropy(intensities)
        print(f"[PASS] Shannon entropy: {entropy:.3f}")
        
        # Test term entropy
        terms = [
            {"intensity": 1.0},
            {"intensity": 2.0},
            {"intensity": 3.0}
        ]
        term_entropy = calculate_term_entropy(terms)
        print(f"[PASS] Term entropy: {term_entropy:.3f}")
        
        # Test relationship entropy
        related_ids = ["id1", "id2", "id3"]
        rel_entropy = calculate_relationship_entropy(related_ids, weight=1.0)
        print(f"[PASS] Relationship entropy: {rel_entropy:.3f}")
        
        # Test adaptive tau
        base_tau = 14 * 24 * 3600  # 14 days
        tau_val = adaptive_tau(base_tau, entropy)
        print(f"[PASS] Adaptive tau: {tau_val:.0f}")
        
        # Test decay factor
        decay = decay_factor(7 * 24 * 3600, base_tau)  # 7 days age
        print(f"[PASS] Decay factor: {decay:.3f}")
        
        # Test entropy-weighted decay
        weighted_decay = entropy_weighted_decay(7 * 24 * 3600, base_tau, entropy)
        print(f"[PASS] Entropy-weighted decay: {weighted_decay:.3f}")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Entropy core: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("KIMERA-SWM TOY IMPLEMENTATION")
    print("Core Functionality Test")
    print("="*50)
    
    tests = [
        test_core_imports,
        test_echoform_core,
        test_identity_core,
        test_entropy_core
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print(f"[FAIL] {test.__name__}")
    
    print(f"\n" + "="*50)
    print(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("[PASS] All core functionality tests passed!")
        print("Status: READY FOR ROADMAP IMPLEMENTATION")
        return True
    else:
        print("[FAIL] Some core tests failed")
        print("Status: NEEDS FIXES BEFORE ROADMAP")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
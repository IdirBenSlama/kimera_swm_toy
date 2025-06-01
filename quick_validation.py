#!/usr/bin/env python3
"""
Quick validation of current implementation
"""
import sys
import os
sys.path.insert(0, 'src')

def main():
    print("=== Quick Validation ===")
    
    # Test 1: EchoForm basic functionality
    try:
        from kimera.echoform import EchoForm
        echo = EchoForm()
        echo.add_term("test", intensity=2.0)
        intensity = echo.intensity_sum()
        print(f"[PASS] EchoForm basic functionality - intensity: {intensity}")
    except Exception as e:
        print(f"[FAIL] EchoForm: {e}")
        return False
    
    # Test 2: Identity basic functionality
    try:
        from kimera.identity import Identity
        identity = Identity(content="test content")
        data = identity.to_dict()
        identity2 = Identity.from_dict(data)
        print(f"[PASS] Identity basic functionality - ID: {identity.id}")
    except Exception as e:
        print(f"[FAIL] Identity: {e}")
        return False
    
    # Test 3: Entropy calculations
    try:
        from kimera.entropy import calculate_shannon_entropy
        entropy = calculate_shannon_entropy([1.0, 2.0, 3.0])
        print(f"[PASS] Entropy calculations - entropy: {entropy:.3f}")
    except Exception as e:
        print(f"[FAIL] Entropy: {e}")
        return False
    
    # Test 4: Identity entropy and tau
    try:
        entropy_val = identity.entropy()
        tau_val = identity.effective_tau()
        print(f"[PASS] Identity entropy: {entropy_val:.3f}, tau: {tau_val:.0f}")
    except Exception as e:
        print(f"[FAIL] Identity entropy/tau: {e}")
        return False
    
    print("\n[PASS] All quick validation tests passed!")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
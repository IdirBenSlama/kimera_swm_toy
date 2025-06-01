#!/usr/bin/env python3
"""
Quick test of roadmap implementation
"""
import sys
sys.path.insert(0, 'src')

def main():
    print("=== Quick Roadmap Implementation Test ===")
    
    # Test 1: Enhanced EchoForm
    try:
        from kimera.echoform import EchoForm
        echo = EchoForm(anchor="test")
        echo.add_term("test1", intensity=2.0)
        echo.add_term("test2", intensity=3.0)
        
        entropy = echo.entropy()
        effective_tau = echo.effective_tau()
        intensity_entropy = echo.intensity_sum(use_entropy_weighting=True)
        
        print(f"✓ EchoForm enhanced: entropy={entropy:.3f}, tau={effective_tau:.0f}, intensity={intensity_entropy:.3f}")
        
        # Test enhanced to_dict
        data = echo.to_dict()
        assert "metadata" in data
        print(f"✓ Enhanced to_dict: {list(data['metadata'].keys())}")
        
    except Exception as e:
        print(f"✗ EchoForm enhanced features failed: {e}")
        return False
    
    # Test 2: Enhanced Identity
    try:
        from kimera.identity import Identity
        identity = Identity(content="test content")
        identity.add_tag("test")
        identity.update_metadata("test_key", "test_value")
        
        age = identity.age_seconds()
        decay = identity.decay_factor()
        
        print(f"✓ Identity enhanced: age={age:.1f}s, decay={decay:.6f}")
        
        # Test tag management
        identity.add_tag("new_tag")
        removed = identity.remove_tag("test")
        print(f"✓ Tag management: added new_tag, removed test={removed}")
        
    except Exception as e:
        print(f"✗ Identity enhanced features failed: {e}")
        return False
    
    # Test 3: Entropy integration
    try:
        from kimera.entropy import adaptive_tau, entropy_weighted_decay
        
        entropy_val = echo.entropy()
        tau_val = adaptive_tau(14*24*3600, entropy_val)
        decay_val = entropy_weighted_decay(7*24*3600, 14*24*3600, entropy_val)
        
        print(f"✓ Entropy integration: tau={tau_val:.0f}, decay={decay_val:.6f}")
        
    except Exception as e:
        print(f"✗ Entropy integration failed: {e}")
        return False
    
    print("\n✓ All quick roadmap tests passed!")
    print("Status: ROADMAP IMPLEMENTATION SUCCESSFUL")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
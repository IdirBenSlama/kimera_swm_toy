#!/usr/bin/env python3
"""
Simple test for unified identity system
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_basic_identity():
    """Test basic identity creation and entropy calculation"""
    print("🧪 Testing basic identity functionality...")
    
    try:
        from kimera.identity import create_geoid_identity, create_scar_identity
        from kimera.entropy import calculate_shannon_entropy
        
        # Test geoid identity
        geoid = create_geoid_identity("Hello world", tags=["test"])
        print(f"✓ Created geoid identity: {geoid.id}")
        print(f"  Type: {geoid.identity_type}")
        print(f"  Raw: {geoid.raw}")
        print(f"  Tags: {geoid.tags}")
        
        # Test entropy calculation
        entropy = geoid.entropy()
        print(f"  Entropy: {entropy:.3f}")
        
        # Test scar identity
        scar = create_scar_identity("id1", "id2", weight=0.8)
        print(f"✓ Created scar identity: {scar.id}")
        print(f"  Type: {scar.identity_type}")
        print(f"  Related IDs: {scar.related_ids}")
        print(f"  Weight: {scar.weight}")
        
        scar_entropy = scar.entropy()
        print(f"  Entropy: {scar_entropy:.3f}")
        
        # Test effective tau
        effective_tau = geoid.effective_tau()
        print(f"  Effective tau: {effective_tau/86400:.1f} days")
        
        # Test serialization
        data = geoid.to_dict()
        restored = geoid.__class__.from_dict(data)
        assert restored.id == geoid.id
        assert restored.raw == geoid.raw
        print("✓ Serialization works")
        
        print("\n✅ All basic tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_entropy_module():
    """Test entropy calculation functions"""
    print("🧪 Testing entropy module...")
    
    try:
        from kimera.entropy import calculate_shannon_entropy, calculate_term_entropy
        
        # Test Shannon entropy
        intensities = [0.5, 0.3, 0.2]
        entropy = calculate_shannon_entropy(intensities)
        print(f"✓ Shannon entropy for {intensities}: {entropy:.3f}")
        
        # Test term entropy
        terms = [
            {"symbol": "test", "intensity": 0.5},
            {"symbol": "hello", "intensity": 0.3},
            {"symbol": "world", "intensity": 0.2}
        ]
        term_entropy = calculate_term_entropy(terms)
        print(f"✓ Term entropy: {term_entropy:.3f}")
        
        print("✅ Entropy module tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Entropy test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 Simple Identity System Test\n")
    
    success = True
    success &= test_entropy_module()
    print()
    success &= test_basic_identity()
    
    if success:
        print("\n🎉 All tests passed! Identity system is working.")
    else:
        print("\n💥 Some tests failed.")
        sys.exit(1)
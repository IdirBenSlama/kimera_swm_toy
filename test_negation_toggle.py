#!/usr/bin/env python3
"""
Test that the negation fix can be toggled via environment variable
"""
import os
import sys
sys.path.insert(0, 'src')

def test_negation_toggle():
    """Test negation fix toggle"""
    print("🔧 Testing Negation Fix Toggle")
    print("=" * 30)
    
    # Test cases
    test_cases = [
        ("Birds can fly", "Birds cannot fly", True),  # Should detect negation
        ("I like cats", "I don't like cats", True),   # Should detect negation  
        ("Water is hot", "Water is cold", False),     # No negation
    ]
    
    for env_val, description in [("0", "OFF"), ("1", "ON")]:
        print(f"\n🎯 Testing with KIMERA_NEGATION_FIX={env_val} ({description})")
        
        # Set environment variable
        os.environ["KIMERA_NEGATION_FIX"] = env_val
        
        # Import after setting env var (to pick up the setting)
        if 'kimera.resonance' in sys.modules:
            del sys.modules['kimera.resonance']
        if 'kimera.geoid' in sys.modules:
            del sys.modules['kimera.geoid']
            
        try:
            from kimera.geoid import Geoid
            from kimera.resonance import resonance, ENABLE_NEGATION_FIX
            
            print(f"  ENABLE_NEGATION_FIX = {ENABLE_NEGATION_FIX}")
            
            for text1, text2, has_negation in test_cases:
                # Create geoids
                g1 = Geoid(text1)
                g2 = Geoid(text2)
                
                # Get resonance score
                score = resonance(g1, g2)
                
                print(f"  '{text1}' vs '{text2}' → {score:.3f}")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("\n✅ Toggle test complete!")
    print("Expected: Scores should be different between ON/OFF for negation cases")

if __name__ == "__main__":
    test_negation_toggle()
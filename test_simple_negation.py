#!/usr/bin/env python3
"""
Simple test of negation detection
"""
import os
import sys

# Test the toggle mechanism
def test_toggle():
    print("🔧 Testing Negation Toggle Mechanism")
    print("=" * 40)
    
    # Test with negation OFF
    os.environ["KIMERA_NEGATION_FIX"] = "0"
    
    # Clear any cached modules
    modules_to_clear = [k for k in sys.modules.keys() if k.startswith('kimera')]
    for mod in modules_to_clear:
        del sys.modules[mod]
    
    sys.path.insert(0, 'src')
    
    try:
        from kimera.resonance import ENABLE_NEGATION_FIX, negation_mismatch
        print(f"Negation fix OFF: ENABLE_NEGATION_FIX = {ENABLE_NEGATION_FIX}")
        
        # Test negation detection function
        test_cases = [
            ("Birds can fly", "Birds cannot fly"),
            ("I like cats", "I don't like cats"),
            ("Water is hot", "Water is cold"),
        ]
        
        for text1, text2 in test_cases:
            mismatch = negation_mismatch(text1, text2)
            print(f"  '{text1}' vs '{text2}' → negation mismatch: {mismatch}")
            
    except Exception as e:
        print(f"❌ Error with negation OFF: {e}")
        import traceback
        traceback.print_exc()
    
    # Test with negation ON
    print(f"\n" + "="*40)
    os.environ["KIMERA_NEGATION_FIX"] = "1"
    
    # Clear modules again
    modules_to_clear = [k for k in sys.modules.keys() if k.startswith('kimera')]
    for mod in modules_to_clear:
        del sys.modules[mod]
    
    try:
        from kimera.resonance import ENABLE_NEGATION_FIX
        print(f"Negation fix ON: ENABLE_NEGATION_FIX = {ENABLE_NEGATION_FIX}")
        
    except Exception as e:
        print(f"❌ Error with negation ON: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_toggle()
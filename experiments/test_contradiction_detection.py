"""
Test contradiction detection to see why it's not working
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from kimera.geoid import init_geoid
from kimera.contradiction import detect_contradiction

# Test obvious contradictions
test_pairs = [
    ("The sky is blue", "The sky is red"),
    ("All swans are white", "Some swans are black"),
    ("This statement is true", "This statement is false"),
    ("It is raining", "It is not raining"),
    ("The number is positive", "The number is negative"),
    ("Democracy is good", "Democracy is bad"),
]

print("Testing Contradiction Detection")
print("=" * 60)

for text1, text2 in test_pairs:
    g1 = init_geoid(text1)
    g2 = init_geoid(text2)
    
    is_contradiction, confidence, reasoning = detect_contradiction(g1, g2)
    
    print(f"\n'{text1}' vs '{text2}'")
    print(f"  Contradiction: {is_contradiction}")
    print(f"  Confidence: {confidence}")
    print(f"  Reasoning: {reasoning}")

print("\n\nCONCLUSION: The contradiction detection is returning default values!")
print("It's not actually detecting contradictions - just returning False with 0.7-0.8 confidence")
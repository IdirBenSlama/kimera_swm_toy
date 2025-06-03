"""
Diagnose why pressure values are unrealistically high
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
from kimera.geoid import init_geoid
from kimera.contradiction import detect_contradiction
from kimera.resonance import resonance

# Test with just 3 simple, non-contradictory texts
texts = [
    "The sun is bright",
    "Water is wet", 
    "Grass is green"
]

geoids = [init_geoid(t) for t in texts]

print("Pressure Diagnosis")
print("=" * 60)

# Check each pair
total_pressure = 0
pair_count = 0

for i, g1 in enumerate(geoids):
    print(f"\nAnalyzing: '{g1.raw}'")
    
    for j, g2 in enumerate(geoids):
        if i == j:
            continue
            
        pair_count += 1
        
        # Get resonance
        res = resonance(g1, g2)
        
        # Check contradiction
        is_contra, conf, reason = detect_contradiction(g1, g2)
        
        print(f"  vs '{g2.raw}':")
        print(f"    Resonance: {res:.3f}")
        print(f"    Contradiction: {is_contra} (confidence={conf:.3f})")
        
        # Calculate pressure contribution
        pressure_contrib = 0
        
        if res < 0.3:
            pressure_contrib = (1.0 - res) * 1.5
            print(f"    Low resonance pressure: {pressure_contrib:.3f}")
        elif is_contra:
            base = conf * 2.0
            paradox = 1.0 + res
            pressure_contrib = base * paradox
            print(f"    Contradiction pressure: {pressure_contrib:.3f}")
        elif res > 0.7:
            pressure_contrib = res * 0.5
            print(f"    High resonance pressure: {pressure_contrib:.3f}")
        else:
            print(f"    No pressure contribution")
            
        total_pressure += pressure_contrib
    
    print(f"  TOTAL PRESSURE: {total_pressure:.3f}")
    total_pressure = 0  # Reset for next geoid

print(f"\n\nTotal pairs analyzed: {pair_count}")
print("\nKEY INSIGHT: Every low-resonance pair contributes ~1.0-1.5 pressure!")
print("With N geoids, each geoid sees N-1 others, so pressure ≈ (N-1) * 1.0")
print(f"For 16 geoids: Expected pressure ≈ 15 * 1.0 = 15.0")
print("This matches our observed ~19-22 range!")

print("\nPROBLEM: The pressure formula treats ALL low-resonance as opposition")
print("This is fundamentally wrong - unrelated concepts aren't contradictions!")
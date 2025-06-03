"""
Debug pressure calculation to understand why values are so high
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from kimera.geoid import init_geoid
from kimera.thermodynamics import ThermodynamicSystem
from kimera.contradiction import detect_contradiction
from kimera.resonance import resonance

# Test with simple examples
texts = [
    "The sky is blue",
    "The sky is red",
    "Mathematics is beautiful",
    "Mathematics is ugly"
]

geoids = [init_geoid(t) for t in texts]
system = ThermodynamicSystem(pressure_threshold=7.0)

print("Debugging Pressure Calculation")
print("=" * 60)

# Test pairwise
for i, g1 in enumerate(geoids):
    print(f"\nGeoid {i}: '{g1.raw}'")
    
    # Calculate pressure against all others
    others = [g for j, g in enumerate(geoids) if j != i]
    
    print("  Checking against:")
    for j, g2 in enumerate(others):
        # Check resonance
        res = resonance(g1, g2)
        
        # Check contradiction
        is_contra, conf, reason = detect_contradiction(g1, g2)
        
        print(f"    '{g2.raw}':")
        print(f"      Resonance: {res:.3f}")
        print(f"      Contradiction: {is_contra} (conf={conf:.3f})")
        
    # Calculate total pressure
    pressure = system.calculate_pressure(g1, others)
    print(f"  TOTAL PRESSURE: {pressure:.3f}")

# Check equilibrium calculation
print("\n" + "="*60)
print("Equilibrium Analysis:")
for i, g in enumerate(geoids):
    eq = system.find_equilibrium_point(g, geoids)
    print(f"\nGeoid {i}: '{g.raw}'")
    print(f"  Pressure: {eq['pressure']:.3f}")
    print(f"  Coherence: {eq['coherence']:.3f}")
    print(f"  Phase: ", end="")
    
    # Manual phase calculation
    if eq['pressure'] < 2.0 and eq['coherence'] > 0.7:
        print("SOLID")
    elif eq['pressure'] < 5.0 and eq['coherence'] > 0.4:
        print("LIQUID")
    elif eq['pressure'] < 7.0:
        print("GAS")
    else:
        print("PLASMA")
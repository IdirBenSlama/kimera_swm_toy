"""
Test script for thermodynamic functionality
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.kimera.geoid import init_geoid
from src.kimera.thermodynamics import create_thermodynamic_system
from src.kimera.contradiction import detect_contradiction
from src.kimera.resonance import resonance


def test_basic_pressure():
    """Test basic pressure calculation."""
    print("Testing basic pressure calculation...")
    
    thermo = create_thermodynamic_system(pressure_threshold=5.0)
    
    # Create contradicting statements
    g1 = init_geoid("The sky is blue", lang="en")
    g2 = init_geoid("The sky is not blue", lang="en")
    g3 = init_geoid("The sky is green", lang="en")
    
    # Test contradiction detection
    is_contra, conf, reason = detect_contradiction(g1, g2)
    print(f"\nContradiction between '{g1.raw}' and '{g2.raw}':")
    print(f"  Is contradiction: {is_contra}")
    print(f"  Confidence: {conf}")
    print(f"  Reason: {reason}")
    
    # Calculate pressure
    pressure = thermo.calculate_pressure(g1, [g2, g3])
    print(f"\nPressure on '{g1.raw}': {pressure:.2f}")
    
    # Check resonance scores
    print(f"\nResonance scores:")
    print(f"  g1 <-> g2: {resonance(g1, g2):.3f}")
    print(f"  g1 <-> g3: {resonance(g1, g3):.3f}")
    
    return pressure > 0


def test_collapse():
    """Test constructive collapse."""
    print("\n\nTesting constructive collapse...")
    
    thermo = create_thermodynamic_system(pressure_threshold=3.0)  # Low threshold
    
    # Create a paradox
    paradox = init_geoid("This statement is false", lang="en", layers=["paradox"])
    
    # Create pressure sources
    sources = [
        init_geoid("If true then false", lang="en"),
        init_geoid("If false then true", lang="en"),
        init_geoid("Contradictions are impossible", lang="en"),
        init_geoid("Logic must be consistent", lang="en"),
    ]
    
    # Build pressure
    pressure = thermo.calculate_pressure(paradox, sources)
    print(f"\nPressure on paradox: {pressure:.2f}")
    print(f"Threshold: {thermo.pressure_threshold}")
    
    # Check collapse
    should_collapse, ctype = thermo.check_collapse_conditions(paradox)
    print(f"Should collapse: {should_collapse}")
    
    if should_collapse:
        void = thermo.constructive_collapse(paradox, ctype)
        print(f"\nVoid created!")
        print(f"  Origin: {void.origin_gid}")
        print(f"  Collapse pressure: {void.collapse_pressure:.2f}")
        print(f"  Potential energy: {void.potential_energy:.2f}")
        print(f"  Dimensions: {void.dimensions}")
        return True
    
    return False


def test_phase_diagram():
    """Test phase classification."""
    print("\n\nTesting phase diagram...")
    
    thermo = create_thermodynamic_system()
    
    # Create geoids in different states
    geoids = [
        init_geoid("2 + 2 = 4", lang="en"),  # Should be solid
        init_geoid("Democracy is good", lang="en"),  # Should be liquid
        init_geoid("Consciousness is mysterious", lang="en"),  # Should be gas
    ]
    
    # Add some pressure to the last one
    thermo.calculate_pressure(geoids[2], [
        init_geoid("Consciousness is just computation", lang="en"),
        init_geoid("Consciousness cannot be explained", lang="en"),
    ])
    
    phases = thermo.phase_diagram(geoids)
    
    print("\nPhase classification:")
    for phase, items in phases.items():
        if items:
            print(f"\n{phase.upper()}:")
            for g in items:
                print(f"  - {g.raw}")
    
    return len(phases["solid"]) > 0 or len(phases["liquid"]) > 0


def main():
    """Run all tests."""
    print("="*60)
    print("THERMODYNAMICS MODULE TEST")
    print("="*60)
    
    tests = [
        ("Basic Pressure", test_basic_pressure),
        ("Constructive Collapse", test_collapse),
        ("Phase Diagram", test_phase_diagram),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\nERROR in {name}: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    print("\n\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{name}: {status}")


if __name__ == "__main__":
    main()
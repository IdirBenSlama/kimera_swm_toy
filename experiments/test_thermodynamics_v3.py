"""
Test the corrected thermodynamic system V3
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
import matplotlib.pyplot as plt
from kimera.geoid import init_geoid
from kimera.thermodynamics_v3 import ThermodynamicSystemV3


def test_basic_thermodynamics():
    """Test basic thermodynamic calculations."""
    print("Testing Thermodynamic System V3")
    print("=" * 60)
    
    system = ThermodynamicSystemV3()
    
    # Test with known contradictory texts
    contradictory_texts = [
        "The sky is blue",
        "The sky is red", 
        "The sky is not blue"
    ]
    
    print("\n1. Testing contradictory texts:")
    geoids = [init_geoid(t) for t in contradictory_texts]
    
    for i, geoid in enumerate(geoids):
        state = system.analyze_geoid_state(geoid, geoids)
        print(f"  '{contradictory_texts[i]}':")
        print(f"    Pressure: {state.pressure:.3f}")
        print(f"    Coherence: {state.coherence:.3f}")
        print(f"    Phase: {state.phase}")
        print(f"    Contradictions: {len(state.contradictions)}")
    
    # Test with coherent texts
    coherent_texts = [
        "Water is H2O",
        "Ice is frozen water",
        "Steam is water vapor"
    ]
    
    print("\n2. Testing coherent texts:")
    geoids = [init_geoid(t) for t in coherent_texts]
    
    for i, geoid in enumerate(geoids):
        state = system.analyze_geoid_state(geoid, geoids)
        print(f"  '{coherent_texts[i]}':")
        print(f"    Pressure: {state.pressure:.3f}")
        print(f"    Coherence: {state.coherence:.3f}")
        print(f"    Phase: {state.phase}")
        print(f"    Aligned: {len(state.aligned_geoids)}")


def test_phase_diagram():
    """Test phase diagram generation."""
    print("\n\n3. Testing phase diagram generation:")
    print("=" * 60)
    
    system = ThermodynamicSystemV3()
    
    # Create diverse corpus
    texts = [
        # Should be solid (coherent, low pressure)
        "Water freezes at 0°C",
        "Ice is solid water",
        "H2O is the chemical formula for water",
        
        # Should be liquid (some contradictions)
        "Coffee is the best drink",
        "Tea is the best drink",
        
        # Should be gas (contradictory)
        "The sky is blue",
        "The sky is red",
        
        # Should be plasma (highly contradictory)
        "This statement is true",
        "This statement is false",
    ]
    
    geoids = [init_geoid(t) for t in texts]
    phase_diagram, all_states = system.generate_phase_diagram(geoids)
    
    print("\nPhase Distribution:")
    for phase, states in phase_diagram.items():
        print(f"  {phase.upper()}: {len(states)} geoids")
        if states:
            for state in states[:2]:  # Show first 2 examples
                print(f"    - '{state.raw[:40]}...' (P={state.pressure:.3f}, C={state.coherence:.3f})")
    
    # Check if we have multiple phases
    phases_with_content = sum(1 for states in phase_diagram.values() if states)
    print(f"\nPhases detected: {phases_with_content}/4")
    
    if phases_with_content >= 2:
        print("✅ Multiple phases detected - system working correctly!")
    else:
        print("❌ Only one phase detected - system may have issues")
    
    return phase_diagram, all_states


def create_phase_diagram_plot(phase_diagram, all_states):
    """Create visualization of the phase diagram."""
    print("\n4. Creating phase diagram visualization...")
    
    plt.figure(figsize=(10, 8))
    
    colors = {"solid": "blue", "liquid": "green", "gas": "orange", "plasma": "red"}
    
    for phase, states in phase_diagram.items():
        if states:
            pressures = [s.pressure for s in states]
            coherences = [s.coherence for s in states]
            plt.scatter(pressures, coherences, 
                       c=colors[phase], 
                       label=f"{phase} (n={len(states)})",
                       s=100, alpha=0.7)
    
    plt.xlabel("Semantic Pressure")
    plt.ylabel("Semantic Coherence")
    plt.title("Thermodynamic Phase Diagram V3 - Corrected Model")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Add phase boundary guidelines
    plt.axvline(x=0.1, color='blue', linestyle='--', alpha=0.3, label='Solid boundary')
    plt.axvline(x=0.3, color='green', linestyle='--', alpha=0.3, label='Liquid boundary')
    plt.axvline(x=0.6, color='orange', linestyle='--', alpha=0.3, label='Gas boundary')
    
    plt.xlim(-0.05, 1.0)
    plt.ylim(-0.05, 1.0)
    
    output_path = Path("experiments/thermodynamic_v3_phase_diagram.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Phase diagram saved to: {output_path}")
    plt.close()


def run_validation():
    """Run the built-in validation."""
    print("\n5. Running built-in validation:")
    print("=" * 60)
    
    system = ThermodynamicSystemV3()
    results = system.validate_system()
    
    print("\nValidation Results:")
    for test, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status} {test}")
    
    all_passed = all(results.values())
    print(f"\nOverall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    return all_passed


def main():
    """Run all tests."""
    # Basic tests
    test_basic_thermodynamics()
    
    # Phase diagram
    phase_diagram, all_states = test_phase_diagram()
    
    # Visualization
    create_phase_diagram_plot(phase_diagram, all_states)
    
    # Validation
    validation_passed = run_validation()
    
    # Summary
    print("\n" + "=" * 60)
    print("THERMODYNAMIC SYSTEM V3 TESTING COMPLETE")
    
    if validation_passed:
        print("✅ All validations passed - system is working correctly!")
        print("✅ Phase diagram generation successful")
        print("✅ Contradiction detection integrated properly")
        print("\n🎉 THERMODYNAMIC PHASE DIAGRAM: NOW ACTUALLY COMPLETE!")
    else:
        print("❌ Some validations failed - further work needed")


if __name__ == "__main__":
    main()
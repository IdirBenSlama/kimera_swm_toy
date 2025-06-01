"""
Demonstration of Thermodynamic Concepts in Kimera-SWM
====================================================

This demo shows:
1. Semantic pressure from contradictions
2. Constructive collapse and void formation
3. Phase transitions in conceptual space
4. Energy transfer between geoids
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.kimera.geoid import init_geoid
from src.kimera.thermodynamics import create_thermodynamic_system
from src.kimera.resonance import resonance
import numpy as np


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"{title:^60}")
    print('='*60)


def demo_semantic_pressure():
    """Demonstrate how contradictions create semantic pressure."""
    print_section("Semantic Pressure from Contradictions")
    
    # Create a thermodynamic system
    thermo = create_thermodynamic_system(pressure_threshold=10.0)
    
    # Create geoids with contradictions
    geoids = [
        init_geoid("The Earth is round", lang="en", layers=["astronomy"]),
        init_geoid("The Earth is flat", lang="en", layers=["conspiracy"]),
        init_geoid("The Earth is not flat", lang="en", layers=["science"]),
        init_geoid("The Earth cannot be flat", lang="en", layers=["physics"]),
    ]
    
    # Calculate pressure on the "flat Earth" geoid from contradictions
    flat_earth = geoids[1]
    contradicting = [geoids[0], geoids[2], geoids[3]]
    
    pressure = thermo.calculate_pressure(flat_earth, contradicting)
    
    print(f"\nGeoid: '{flat_earth.raw}'")
    print(f"Contradicting statements: {len(contradicting)}")
    print(f"Accumulated semantic pressure: {pressure:.2f}")
    print(f"Pressure sources: {thermo.pressures[flat_earth.gid].sources}")
    
    # Check if collapse conditions are met
    should_collapse, collapse_type = thermo.check_collapse_conditions(flat_earth)
    print(f"\nShould collapse? {should_collapse}")
    if should_collapse:
        print(f"Collapse type: {collapse_type}")


def demo_constructive_collapse():
    """Demonstrate constructive collapse creating conceptual voids."""
    print_section("Constructive Collapse and Void Formation")
    
    thermo = create_thermodynamic_system(pressure_threshold=5.0)  # Lower threshold for demo
    
    # Create a geoid with many contradictions
    central = init_geoid("Light is both a wave and a particle", lang="en", layers=["quantum"])
    
    # Create contradicting views
    contradictions = [
        init_geoid("Light is only a wave", lang="en", layers=["classical"]),
        init_geoid("Light is only a particle", lang="en", layers=["classical"]),
        init_geoid("Light cannot be both wave and particle", lang="en", layers=["logic"]),
        init_geoid("Wave-particle duality is impossible", lang="en", layers=["philosophy"]),
        init_geoid("Light must be either wave or particle", lang="en", layers=["binary"]),
    ]
    
    # Build up pressure
    pressure = thermo.calculate_pressure(central, contradictions)
    print(f"\nCentral concept: '{central.raw}'")
    print(f"Semantic pressure: {pressure:.2f}")
    print(f"Pressure threshold: {thermo.pressure_threshold}")
    
    # Perform collapse
    should_collapse, collapse_type = thermo.check_collapse_conditions(central)
    if should_collapse:
        void = thermo.constructive_collapse(central, collapse_type)
        print(f"\nCollapse occurred! Type: {collapse_type}")
        print(f"Void created with properties:")
        for key, value in void.dimensions.items():
            print(f"  - {key}: {value:.2f}")
        print(f"Potential energy available: {void.potential_energy:.2f}")
        print("\nThis void represents a space where quantum mechanics can emerge")


def demo_phase_transitions():
    """Demonstrate phase transitions in conceptual space."""
    print_section("Phase Transitions in Conceptual Space")
    
    thermo = create_thermodynamic_system()
    
    # Create geoids representing different states
    geoids = [
        # Solid phase - stable, well-defined concepts
        init_geoid("Water freezes at 0°C", lang="en", layers=["physics"]),
        init_geoid("Ice is solid water", lang="en", layers=["chemistry"]),
        
        # Liquid phase - flexible, adaptable concepts
        init_geoid("Democracy adapts to culture", lang="en", layers=["politics"]),
        init_geoid("Language evolves over time", lang="en", layers=["linguistics"]),
        
        # Gas phase - volatile, disputed concepts
        init_geoid("Consciousness emerges from complexity", lang="en", layers=["philosophy"]),
        init_geoid("Free will is an illusion", lang="en", layers=["neuroscience"]),
        
        # Near plasma - highly contradictory
        init_geoid("This statement is false", lang="en", layers=["paradox"]),
    ]
    
    # Add some contradictions to create pressure
    paradox = geoids[-1]
    thermo.calculate_pressure(paradox, [
        init_geoid("This statement is true", lang="en", layers=["logic"]),
        init_geoid("Paradoxes cannot exist", lang="en", layers=["philosophy"]),
    ])
    
    # Classify into phases
    phases = thermo.phase_diagram(geoids)
    
    print("\nConceptual Phase Diagram:")
    for phase, phase_geoids in phases.items():
        print(f"\n{phase.upper()} phase ({len(phase_geoids)} geoids):")
        for g in phase_geoids:
            equilibrium = thermo.find_equilibrium_point(g, geoids)
            print(f"  - '{g.raw[:40]}...' (pressure: {equilibrium['pressure']:.2f}, coherence: {equilibrium['coherence']:.2f})")


def demo_energy_transfer():
    """Demonstrate energy transfer between geoids."""
    print_section("Energy Transfer Between Geoids")
    
    thermo = create_thermodynamic_system()
    
    # Create source and target geoids
    source = init_geoid("Evolution explains biodiversity", lang="en", layers=["biology"])
    
    targets = [
        init_geoid("Natural selection drives adaptation", lang="en", layers=["evolution"]),
        init_geoid("God created all species", lang="en", layers=["creationism"]),
        init_geoid("Life emerged from chemical processes", lang="en", layers=["abiogenesis"]),
    ]
    
    print(f"\nSource: '{source.raw}'")
    print("\nEnergy transfer to different targets:")
    
    for target in targets:
        result = thermo.energy_transfer(source, target, amount=5.0)
        res_score = resonance(source, target)
        
        print(f"\nTarget: '{target.raw}'")
        print(f"  Resonance: {res_score:.3f}")
        print(f"  Transfer efficiency: {result['efficiency']:.3f}")
        print(f"  Energy transferred: {result['transferred']:.2f}")
        print(f"  Pressure created: {result['pressure_created']:.2f}")


def demo_system_entropy():
    """Demonstrate entropy calculation for geoid systems."""
    print_section("System Entropy and Information Diversity")
    
    thermo = create_thermodynamic_system()
    
    # Create two systems - one diverse, one uniform
    diverse_system = [
        init_geoid("Quantum mechanics describes the very small", lang="en"),
        init_geoid("Poetry expresses human emotion", lang="en"),
        init_geoid("Economics studies resource allocation", lang="en"),
        init_geoid("Music is organized sound", lang="en"),
        init_geoid("Chemistry explores molecular interactions", lang="en"),
    ]
    
    uniform_system = [
        init_geoid("Physics studies matter and energy", lang="en"),
        init_geoid("Physics explains natural phenomena", lang="en"),
        init_geoid("Physics uses mathematics", lang="en"),
        init_geoid("Physics is a natural science", lang="en"),
        init_geoid("Physics discovers universal laws", lang="en"),
    ]
    
    diverse_entropy = thermo.calculate_system_entropy(diverse_system)
    uniform_entropy = thermo.calculate_system_entropy(uniform_system)
    
    print("\nDiverse System (different domains):")
    for g in diverse_system:
        print(f"  - {g.raw}")
    print(f"System entropy: {diverse_entropy:.3f}")
    
    print("\nUniform System (same domain):")
    for g in uniform_system:
        print(f"  - {g.raw}")
    print(f"System entropy: {uniform_entropy:.3f}")
    
    print(f"\nThe diverse system has {diverse_entropy/uniform_entropy:.1f}x higher entropy")
    print("Higher entropy indicates richer information content")


def main():
    """Run all demonstrations."""
    print("\n" + "="*60)
    print("THERMODYNAMIC CONCEPTS IN KIMERA-SWM")
    print("="*60)
    
    demos = [
        demo_semantic_pressure,
        demo_constructive_collapse,
        demo_phase_transitions,
        demo_energy_transfer,
        demo_system_entropy,
    ]
    
    for demo in demos:
        try:
            demo()
        except Exception as e:
            print(f"\nError in {demo.__name__}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("Demo completed!")
    print("="*60)


if __name__ == "__main__":
    main()
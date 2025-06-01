"""
Advanced Thermodynamics Demo - Paradox Resolution through Collapse
================================================================

This demo shows how paradoxes create extreme semantic pressure
leading to constructive collapse and the emergence of new understanding.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.kimera.geoid import init_geoid
from src.kimera.thermodynamics import create_thermodynamic_system
from src.kimera.resonance import resonance
import time


def print_header(title, char='='):
    """Print a formatted header."""
    print(f"\n{char*70}")
    print(f"{title:^70}")
    print(f"{char*70}\n")


def simulate_paradox_resolution():
    """Simulate how a paradox creates pressure and resolves through collapse."""
    print_header("PARADOX RESOLUTION THROUGH CONSTRUCTIVE COLLAPSE")
    
    # Create system with lower threshold to see effects
    thermo = create_thermodynamic_system(pressure_threshold=8.0)
    
    # The Liar's Paradox
    print("Creating the Liar's Paradox...")
    liar = init_geoid("This statement is false", lang="en", layers=["paradox", "logic"])
    
    # Create related statements that increase pressure
    related_statements = [
        init_geoid("If this statement is true, then it is false", lang="en", layers=["analysis"]),
        init_geoid("If this statement is false, then it is true", lang="en", layers=["analysis"]),
        init_geoid("Truth and falsehood are mutually exclusive", lang="en", layers=["logic"]),
        init_geoid("Every statement must be either true or false", lang="en", layers=["classical_logic"]),
        init_geoid("Self-reference creates logical problems", lang="en", layers=["metalogic"]),
        init_geoid("This paradox has no resolution in classical logic", lang="en", layers=["limitation"]),
    ]
    
    # Show initial state
    print(f"\nParadox: '{liar.raw}'")
    print(f"Initial pressure: {thermo.pressures.get(liar.gid, 0)}")
    
    # Gradually add contradictions to build pressure
    print("\nBuilding semantic pressure...")
    for i, stmt in enumerate(related_statements):
        pressure = thermo.calculate_pressure(liar, related_statements[:i+1])
        print(f"  Step {i+1}: Added '{stmt.raw[:30]}...'")
        print(f"          Pressure now: {pressure:.2f}")
        
        # Check for collapse
        should_collapse, collapse_type = thermo.check_collapse_conditions(liar)
        if should_collapse:
            print(f"\n*** CRITICAL PRESSURE REACHED! ***")
            print(f"Collapse type: {collapse_type}")
            
            # Perform the collapse
            void = thermo.constructive_collapse(liar, collapse_type)
            
            print(f"\nCONSTRUCTIVE COLLAPSE OCCURRED!")
            print(f"Void properties:")
            for key, value in void.dimensions.items():
                print(f"  {key}: {value}")
            print(f"Potential energy released: {void.potential_energy:.2f}")
            
            # Show what can emerge from the void
            print("\nFrom this void, new understanding can emerge:")
            print("  - Three-valued logic (true, false, undefined)")
            print("  - Paraconsistent logic (tolerates contradictions)")
            print("  - Levels of truth (metalanguages)")
            print("  - Fuzzy logic (degrees of truth)")
            
            break
    
    return thermo, liar


def simulate_wave_particle_duality():
    """Simulate the resolution of wave-particle duality through thermodynamics."""
    print_header("WAVE-PARTICLE DUALITY: FROM PARADOX TO QUANTUM MECHANICS")
    
    thermo = create_thermodynamic_system(pressure_threshold=12.0)
    
    # Central paradox
    duality = init_geoid(
        "Light exhibits both wave and particle properties simultaneously",
        lang="en",
        layers=["quantum", "paradox"]
    )
    
    # Classical objections that create pressure
    classical_objections = [
        init_geoid("A phenomenon cannot be two contradictory things at once", lang="en", layers=["classical"]),
        init_geoid("Waves are continuous, particles are discrete", lang="en", layers=["physics"]),
        init_geoid("Waves spread out, particles are localized", lang="en", layers=["physics"]),
        init_geoid("Classical physics requires deterministic behavior", lang="en", layers=["determinism"]),
        init_geoid("Observation should not change physical reality", lang="en", layers=["realism"]),
        init_geoid("Energy must be either continuous or quantized, not both", lang="en", layers=["energy"]),
    ]
    
    # Experimental evidence that also creates pressure (paradoxically)
    experiments = [
        init_geoid("Double-slit experiment shows interference patterns", lang="en", layers=["experiment"]),
        init_geoid("Photoelectric effect shows particle behavior", lang="en", layers=["experiment"]),
        init_geoid("Compton scattering confirms photon momentum", lang="en", layers=["experiment"]),
    ]
    
    print(f"Central concept: '{duality.raw}'")
    
    # Build pressure from classical objections
    print("\nClassical physics objects...")
    pressure1 = thermo.calculate_pressure(duality, classical_objections)
    print(f"Pressure from classical objections: {pressure1:.2f}")
    
    # Add experimental paradoxes
    print("\nExperimental evidence creates additional pressure...")
    all_pressure_sources = classical_objections + experiments
    pressure2 = thermo.calculate_pressure(duality, all_pressure_sources)
    print(f"Total pressure: {pressure2:.2f}")
    
    # Check for collapse
    should_collapse, collapse_type = thermo.check_collapse_conditions(duality)
    
    if should_collapse:
        print(f"\n*** CONCEPTUAL FRAMEWORK COLLAPSE IMMINENT ***")
        print(f"Type: {collapse_type}")
        
        void = thermo.constructive_collapse(duality, collapse_type)
        
        print(f"\nCOLLAPSE COMPLETE - Void Created")
        print(f"This void has {void.potential_energy:.2f} units of potential energy")
        print("\nFrom this void emerged:")
        print("  ✓ Quantum mechanics")
        print("  ✓ Complementarity principle")
        print("  ✓ Uncertainty relations")
        print("  ✓ Probability amplitudes")
        print("  ✓ Wave function collapse")
    
    return thermo, duality


def demonstrate_phase_space_evolution():
    """Show how a system of geoids evolves through phase space."""
    print_header("PHASE SPACE EVOLUTION OF CONCEPTUAL SYSTEMS")
    
    thermo = create_thermodynamic_system(pressure_threshold=10.0)
    
    # Create an evolving system about consciousness
    geoids = [
        init_geoid("Consciousness is purely physical", lang="en", layers=["materialism"]),
        init_geoid("Consciousness transcends the physical", lang="en", layers=["dualism"]),
        init_geoid("The hard problem of consciousness is unsolvable", lang="en", layers=["philosophy"]),
        init_geoid("Consciousness emerges from complexity", lang="en", layers=["emergence"]),
        init_geoid("Consciousness is fundamental like mass or charge", lang="en", layers=["panpsychism"]),
        init_geoid("Consciousness is an illusion", lang="en", layers=["illusionism"]),
    ]
    
    print("Initial phase distribution:")
    phases = thermo.phase_diagram(geoids)
    for phase, items in phases.items():
        if items:
            print(f"\n{phase.upper()}: {len(items)} geoids")
            for g in items[:2]:  # Show first 2
                print(f"  - {g.raw[:50]}...")
    
    # Create contradictions to evolve the system
    print("\n\nAdding contradictory evidence to create pressure...")
    
    # Add pressure to materialism from qualia arguments
    materialism = geoids[0]
    qualia_objections = [
        init_geoid("Subjective experience cannot be reduced to brain states", lang="en"),
        init_geoid("The explanatory gap between neural activity and experience", lang="en"),
        init_geoid("Mary's room thought experiment shows limits of physical knowledge", lang="en"),
    ]
    
    pressure = thermo.calculate_pressure(materialism, qualia_objections)
    print(f"\nPressure on materialism: {pressure:.2f}")
    
    # Add pressure to dualism from interaction problem
    dualism = geoids[1]
    interaction_problems = [
        init_geoid("How can non-physical mind interact with physical brain?", lang="en"),
        init_geoid("Causal closure of the physical domain", lang="en"),
        init_geoid("Conservation of energy prohibits non-physical causation", lang="en"),
    ]
    
    pressure = thermo.calculate_pressure(dualism, interaction_problems)
    print(f"Pressure on dualism: {pressure:.2f}")
    
    # Show evolved phase distribution
    print("\n\nEvolved phase distribution:")
    phases = thermo.phase_diagram(geoids)
    for phase, items in phases.items():
        if items:
            print(f"\n{phase.upper()}: {len(items)} geoids")
            for g in items:
                eq = thermo.find_equilibrium_point(g, geoids)
                print(f"  - {g.raw[:40]}... (P:{eq['pressure']:.1f}, C:{eq['coherence']:.2f})")
    
    # Find which concepts might collapse
    print("\n\nChecking for potential collapses...")
    for g in geoids:
        should_collapse, ctype = thermo.check_collapse_conditions(g)
        if should_collapse:
            print(f"  ! '{g.raw[:40]}...' ready to collapse ({ctype})")


def visualize_energy_landscape():
    """Visualize the energy landscape of interacting concepts."""
    print_header("ENERGY LANDSCAPE OF INTERACTING CONCEPTS", char='*')
    
    thermo = create_thermodynamic_system()
    
    # Create a network of related concepts
    concepts = [
        init_geoid("Information is physical", lang="en", layers=["information_theory"]),
        init_geoid("Information requires a physical substrate", lang="en", layers=["computing"]),
        init_geoid("Information is abstract and non-physical", lang="en", layers=["mathematics"]),
        init_geoid("Information and energy are related", lang="en", layers=["thermodynamics"]),
        init_geoid("Information has entropy", lang="en", layers=["shannon"]),
    ]
    
    print("Concept network:")
    for i, c in enumerate(concepts):
        print(f"{i+1}. {c.raw}")
    
    # Calculate pairwise energy transfers
    print("\n\nEnergy transfer matrix (efficiency):")
    print("     ", end="")
    for i in range(len(concepts)):
        print(f"{i+1:^7}", end="")
    print()
    
    for i, source in enumerate(concepts):
        print(f"{i+1:^5}", end="")
        for j, target in enumerate(concepts):
            if i != j:
                result = thermo.energy_transfer(source, target, amount=1.0)
                eff = result['efficiency']
                print(f"{eff:^7.3f}", end="")
            else:
                print(f"{'---':^7}", end="")
        print()
    
    # Show system entropy
    entropy = thermo.calculate_system_entropy(concepts)
    print(f"\n\nSystem entropy: {entropy:.3f}")
    print("This indicates the diversity of information in the concept network")
    
    # Find stable configurations
    print("\n\nEquilibrium analysis:")
    for c in concepts:
        eq = thermo.find_equilibrium_point(c, concepts)
        status = "STABLE" if eq['equilibrium'] else "UNSTABLE"
        print(f"{status}: {c.raw[:50]}...")
        print(f"         Stability: {eq['stability']:.3f}, Tension: {eq['tension']:.3f}")


def main():
    """Run all advanced demonstrations."""
    print("\n" + "="*70)
    print("ADVANCED THERMODYNAMIC CONCEPTS IN KIMERA-SWM")
    print("="*70)
    
    # Run demonstrations
    demos = [
        simulate_paradox_resolution,
        simulate_wave_particle_duality,
        demonstrate_phase_space_evolution,
        visualize_energy_landscape,
    ]
    
    for demo in demos:
        try:
            demo()
            time.sleep(0.5)  # Brief pause between demos
        except Exception as e:
            print(f"\nError in {demo.__name__}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*70)
    print("Advanced demo completed!")
    print("="*70)


if __name__ == "__main__":
    main()
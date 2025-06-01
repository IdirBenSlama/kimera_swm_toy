"""
Integration example: Thermodynamics with Kimera Core Components
==============================================================

Shows how thermodynamics integrates with:
- Geoid creation and management
- Resonance detection
- Contradiction detection
- Entropy calculations
- Storage (if available)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.kimera import init_geoid, create_thermodynamic_system
from src.kimera.resonance import resonance
from src.kimera.contradiction import detect_contradiction
from src.kimera.entropy import calculate_shannon_entropy, adaptive_tau

# Optional storage
try:
    from src.kimera.storage import LatticeStorage
    HAS_STORAGE = True
except ImportError:
    HAS_STORAGE = False
    print("Note: Storage not available, running without persistence\n")


def demonstrate_integrated_workflow():
    """Show a complete workflow using thermodynamics with other components."""
    
    print("="*70)
    print("INTEGRATED THERMODYNAMIC WORKFLOW")
    print("="*70)
    
    # 1. Create thermodynamic system
    thermo = create_thermodynamic_system(pressure_threshold=8.0)
    
    # 2. Create a knowledge domain about reality
    print("\n1. Creating knowledge domain about the nature of reality...")
    
    geoids = {
        "materialism": init_geoid(
            "Reality consists only of physical matter and energy",
            lang="en", layers=["philosophy", "materialism"]
        ),
        "idealism": init_geoid(
            "Reality is fundamentally mental or experiential",
            lang="en", layers=["philosophy", "idealism"]
        ),
        "dualism": init_geoid(
            "Reality contains both physical and mental substances",
            lang="en", layers=["philosophy", "dualism"]
        ),
        "simulation": init_geoid(
            "Reality might be a computer simulation",
            lang="en", layers=["philosophy", "simulation_hypothesis"]
        ),
        "quantum": init_geoid(
            "Reality is probabilistic at the quantum level",
            lang="en", layers=["physics", "quantum"]
        ),
        "buddhist": init_geoid(
            "Reality is empty of inherent existence",
            lang="en", layers=["philosophy", "buddhism"]
        )
    }
    
    # 3. Analyze resonances
    print("\n2. Analyzing conceptual resonances...")
    print("\nResonance matrix:")
    print("          ", end="")
    for key in list(geoids.keys())[:4]:
        print(f"{key[:8]:^10}", end="")
    print()
    
    for k1, g1 in list(geoids.items())[:4]:
        print(f"{k1[:8]:^10}", end="")
        for k2, g2 in list(geoids.items())[:4]:
            if k1 == k2:
                print(f"{'---':^10}", end="")
            else:
                score = resonance(g1, g2)
                print(f"{score:^10.3f}", end="")
        print()
    
    # 4. Detect contradictions and build pressure
    print("\n3. Detecting contradictions and building semantic pressure...")
    
    # Materialism faces pressure from other views
    contradicting_materialism = [
        geoids["idealism"],
        geoids["dualism"],
        geoids["buddhist"]
    ]
    
    pressure_mat = thermo.calculate_pressure(
        geoids["materialism"], 
        contradicting_materialism
    )
    
    print(f"\nPressure on materialism: {pressure_mat:.2f}")
    
    # Check specific contradictions
    for name, other in [("idealism", geoids["idealism"]), 
                       ("quantum", geoids["quantum"])]:
        is_contra, conf, reason = detect_contradiction(
            geoids["materialism"], other
        )
        print(f"\nMaterialism vs {name}:")
        print(f"  Contradiction: {is_contra} (confidence: {conf:.2f})")
        print(f"  Reason: {reason}")
    
    # 5. Calculate entropy of the system
    print("\n4. Calculating system entropy...")
    
    geoid_list = list(geoids.values())
    system_entropy = thermo.calculate_system_entropy(geoid_list)
    
    # Also calculate entropy of term intensities (if we had terms)
    # For demo, use resonance scores as "intensities"
    intensities = []
    for g1 in geoid_list:
        for g2 in geoid_list:
            if g1.gid != g2.gid:
                intensities.append(resonance(g1, g2))
    
    resonance_entropy = calculate_shannon_entropy(intensities)
    
    print(f"System entropy (vector diversity): {system_entropy:.3f}")
    print(f"Resonance entropy (connection diversity): {resonance_entropy:.3f}")
    
    # 6. Demonstrate adaptive tau based on entropy
    print("\n5. Entropy-based memory decay...")
    
    base_tau = 14 * 24 * 3600  # 14 days in seconds
    
    for name, geoid in list(geoids.items())[:3]:
        # Use system position as proxy for geoid entropy
        geoid_entropy = abs(hash(geoid.gid)) % 5  # Fake entropy 0-4
        
        effective_tau = adaptive_tau(base_tau, geoid_entropy)
        days = effective_tau / (24 * 3600)
        
        print(f"\n{name}:")
        print(f"  Entropy: {geoid_entropy:.1f}")
        print(f"  Memory decay tau: {days:.1f} days")
        print(f"  (Higher entropy = slower decay)")
    
    # 7. Check phase states
    print("\n6. Analyzing phase states...")
    
    phases = thermo.phase_diagram(geoid_list)
    
    for phase, items in phases.items():
        if items:
            print(f"\n{phase.upper()} phase:")
            for g in items:
                eq = thermo.find_equilibrium_point(g, geoid_list)
                print(f"  {g.raw[:40]}...")
                print(f"    Pressure: {eq['pressure']:.2f}, Stability: {eq['stability']:.3f}")
    
    # 8. Simulate energy transfer
    print("\n7. Simulating conceptual energy transfer...")
    
    # Quantum mechanics influences materialism
    transfer = thermo.energy_transfer(
        geoids["quantum"], 
        geoids["materialism"], 
        amount=10.0
    )
    
    print(f"\nQuantum → Materialism energy transfer:")
    print(f"  Efficiency: {transfer['efficiency']:.3f}")
    print(f"  Transferred: {transfer['transferred']:.2f} units")
    print(f"  Pressure created: {transfer['pressure_created']:.2f}")
    
    # 9. Check for potential collapses
    print("\n8. Checking for potential conceptual collapses...")
    
    for name, geoid in geoids.items():
        should_collapse, collapse_type = thermo.check_collapse_conditions(geoid)
        if should_collapse:
            print(f"\n! {name} ready to collapse ({collapse_type})")
            print(f"  Current pressure: {thermo.pressures[geoid.gid].value:.2f}")
    
    # 10. Optional: Save to storage
    if HAS_STORAGE:
        print("\n9. Saving to storage...")
        storage = LatticeStorage(":memory:")
        
        # Store geoids
        for name, geoid in geoids.items():
            # LatticeStorage expects specific format
            from src.kimera.identity import Identity
            identity = Identity(
                gid=geoid.gid,
                echo=geoid.echo,
                lang=geoid.lang_axis,
                layers=geoid.context_layers
            )
            storage.store_identity(identity)
        
        # Store pressure data as relationships
        for gid, pressure_data in thermo.pressures.items():
            if pressure_data.value > 0:
                storage.store_scar(
                    source_gid=gid,
                    target_gids=pressure_data.sources,
                    weight=pressure_data.value,
                    scar_type="semantic_pressure"
                )
        
        print(f"Stored {len(geoids)} geoids with pressure relationships")
    
    print("\n" + "="*70)
    print("Integration demonstration complete!")
    print("="*70)
    
    return thermo, geoids


def demonstrate_collapse_and_emergence():
    """Show how collapse leads to new understanding."""
    
    print("\n\n" + "="*70)
    print("CONSTRUCTIVE COLLAPSE AND EMERGENCE")
    print("="*70)
    
    thermo = create_thermodynamic_system(pressure_threshold=5.0)
    
    # Create a concept under extreme pressure
    print("\n1. Creating paradoxical concept...")
    
    wave_particle = init_geoid(
        "Light is simultaneously wave and particle",
        lang="en", layers=["physics", "paradox"]
    )
    
    # Sources of pressure
    classical_objections = [
        init_geoid("Things cannot be two contradictory types at once", lang="en"),
        init_geoid("Waves are continuous, particles are discrete", lang="en"),
        init_geoid("Classical logic forbids true contradictions", lang="en"),
        init_geoid("Physical objects have definite properties", lang="en"),
    ]
    
    # Calculate pressure
    pressure = thermo.calculate_pressure(wave_particle, classical_objections)
    print(f"\nSemantic pressure: {pressure:.2f}")
    print(f"Threshold: {thermo.pressure_threshold}")
    
    # Force collapse if needed
    if pressure < thermo.pressure_threshold:
        print("\nManually adding pressure to demonstrate collapse...")
        thermo.pressures[wave_particle.gid].add_pressure(10.0, "forced")
    
    # Perform collapse
    should_collapse, collapse_type = thermo.check_collapse_conditions(wave_particle)
    
    if should_collapse:
        print(f"\n2. Initiating {collapse_type} collapse...")
        
        void = thermo.constructive_collapse(wave_particle, collapse_type)
        
        print(f"\n3. Void created:")
        print(f"   Origin concept: '{wave_particle.raw}'")
        print(f"   Collapse pressure: {void.collapse_pressure:.2f}")
        print(f"   Potential energy: {void.potential_energy:.2f}")
        print(f"   Void dimensions: {void.dimensions}")
        
        print("\n4. From this void, new understanding emerges:")
        
        # Create new concepts that can exist in the void
        quantum_concepts = [
            init_geoid("Complementarity: wave and particle are complementary aspects", lang="en"),
            init_geoid("Measurement determines which aspect manifests", lang="en"),
            init_geoid("Quantum superposition allows multiple states", lang="en"),
            init_geoid("Wave function describes probability amplitudes", lang="en"),
        ]
        
        print("\nEmergent concepts:")
        for qc in quantum_concepts:
            print(f"  - {qc.raw}")
        
        # These new concepts have lower pressure
        print("\n5. Checking stability of emergent concepts...")
        for qc in quantum_concepts:
            # They don't contradict each other as strongly
            pressure = thermo.calculate_pressure(qc, quantum_concepts)
            print(f"   Pressure on '{qc.raw[:40]}...': {pressure:.2f}")
        
        print("\nThe void allowed quantum mechanics to emerge!")
    
    return void if should_collapse else None


def main():
    """Run integrated demonstrations."""
    
    # Basic integration
    thermo, geoids = demonstrate_integrated_workflow()
    
    # Collapse and emergence
    void = demonstrate_collapse_and_emergence()
    
    print("\n\nKey Insights:")
    print("- Thermodynamics quantifies conceptual tension through pressure")
    print("- Entropy measures information diversity in knowledge systems")
    print("- Constructive collapse creates space for new understanding")
    print("- Energy transfer models conceptual influence")
    print("- Phase states indicate conceptual stability")


if __name__ == "__main__":
    main()
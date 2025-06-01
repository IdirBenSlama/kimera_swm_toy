"""
EchoForm Thermodynamics Demo
===========================

Shows how EchoForms interact with thermodynamic concepts:
- Internal pressure from contradictory terms
- Phase transitions based on coherence
- Energy transfer between forms
- Constructive collapse of overloaded forms
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.kimera.thermodynamic_echoform import create_thermodynamic_echoform
import time


def print_section(title):
    """Print formatted section header."""
    print(f"\n{'='*60}")
    print(f"{title:^60}")
    print('='*60)


def demo_pressure_buildup():
    """Demonstrate how contradictory terms create pressure."""
    print_section("Pressure Buildup in EchoForm")
    
    # Create a form about temperature
    form = create_thermodynamic_echoform(
        anchor="temperature_concepts",
        domain="echo"
    )
    
    print(f"\nInitial form: {form.anchor}")
    print(f"Domain: {form.domain}")
    print(f"Phase: {form.phase_state}")
    
    # Add compatible terms
    print("\n1. Adding compatible terms...")
    terms = [
        ("hot", "descriptor", 1.0),
        ("warm", "descriptor", 0.8),
        ("heat", "concept", 0.9),
    ]
    
    for symbol, role, intensity in terms:
        result = form.add_term_with_pressure_check(symbol, role, intensity)
        print(f"   Added '{symbol}': pressure={result['pressure_after']:.2f}, phase={result['phase_after']}")
    
    # Add contradictory terms
    print("\n2. Adding contradictory terms...")
    contradictions = [
        ("cold", "descriptor", 1.0),
        ("freezing", "descriptor", 0.9),
        ("ice", "concept", 0.8),
    ]
    
    for symbol, role, intensity in contradictions:
        result = form.add_term_with_pressure_check(symbol, role, intensity)
        print(f"   Added '{symbol}': pressure={result['pressure_after']:.2f}, phase={result['phase_after']}")
        if result['phase_changed']:
            print(f"   *** PHASE TRANSITION: {result['phase_before']} → {result['phase_after']} ***")
    
    # Show final state
    print(f"\nFinal pressure: {form.calculate_internal_pressure():.2f}")
    print(f"Final coherence: {form.calculate_coherence():.2f}")
    print(f"Final phase: {form.phase_state}")
    
    return form


def demo_phase_transitions():
    """Show how forms transition between phases."""
    print_section("Phase Transitions in EchoForm")
    
    # Create forms in different states
    forms = {
        "stable": create_thermodynamic_echoform("mathematical_axioms", "law"),
        "flexible": create_thermodynamic_echoform("language_evolution", "echo"),
        "volatile": create_thermodynamic_echoform("quantum_paradox", "scar"),
    }
    
    # Add terms to create different phase states
    print("\nCreating forms in different phases...")
    
    # Stable form - coherent mathematical concepts
    forms["stable"].add_term("2+2=4", "axiom", 1.0)
    forms["stable"].add_term("a²+b²=c²", "theorem", 1.0)
    forms["stable"].add_term("π≈3.14159", "constant", 1.0)
    forms["stable"].update_phase_state()
    
    # Flexible form - evolving language
    forms["flexible"].add_term("cool", "slang", 0.8)
    forms["flexible"].add_term("awesome", "slang", 0.7)
    forms["flexible"].add_term("groovy", "dated_slang", 0.3)
    forms["flexible"].add_term("lit", "modern_slang", 0.9)
    forms["flexible"].update_phase_state()
    
    # Volatile form - quantum paradoxes
    forms["volatile"].add_term("wave", "property", 1.0)
    forms["volatile"].add_term("particle", "property", 1.0)
    forms["volatile"].add_term("superposition", "state", 0.9)
    forms["volatile"].add_term("collapse", "event", 0.8)
    forms["volatile"].add_term("deterministic", "classical", 0.7)
    forms["volatile"].add_term("probabilistic", "quantum", 0.7)
    forms["volatile"].update_phase_state()
    
    # Display phase states
    print("\nForm phase states:")
    for name, form in forms.items():
        pressure = form.calculate_internal_pressure()
        coherence = form.calculate_coherence()
        print(f"\n{name.upper()} ({form.anchor}):")
        print(f"  Phase: {form.phase_state}")
        print(f"  Pressure: {pressure:.2f}")
        print(f"  Coherence: {coherence:.2f}")
        print(f"  Effective tau: {form.effective_tau_thermodynamic():.1f}s")
    
    # Demonstrate temperature-based mutation
    print("\n\nTemperature-based mutations:")
    for temp in [0.5, 1.0, 2.0]:
        mutated = forms["flexible"].thermodynamic_mutate(temperature=temp)
        print(f"\nTemperature {temp}:")
        print(f"  Original phase: {forms['flexible'].phase_state}")
        print(f"  Mutated phase: {mutated.phase_state}")
        print(f"  Energy retained: {mutated.stored_energy:.2f}")


def demo_energy_transfer():
    """Demonstrate energy transfer between EchoForms."""
    print_section("Energy Transfer Between EchoForms")
    
    # Create source and target forms
    source = create_thermodynamic_echoform(
        "energy_source",
        "echo",
        initial_energy=10.0
    )
    
    targets = [
        create_thermodynamic_echoform("compatible_echo", "echo"),
        create_thermodynamic_echoform("related_scar", "scar"),
        create_thermodynamic_echoform("strict_law", "law"),
    ]
    
    print(f"\nSource form: {source.anchor} (domain: {source.domain})")
    print(f"Initial energy: {source.stored_energy}")
    
    # Transfer energy to each target
    print("\nTransferring 3.0 energy units to each target...")
    
    for target in targets:
        print(f"\n→ Target: {target.anchor} (domain: {target.domain})")
        
        result = source.energy_transfer_to(target, amount=3.0)
        
        print(f"  Efficiency: {result['efficiency']:.2f}")
        print(f"  Transferred: {result['transferred']:.2f}")
        print(f"  Pressure created: {result['pressure_created']:.2f}")
        print(f"  Target energy: {target.stored_energy:.2f}")
    
    print(f"\nSource energy remaining: {source.stored_energy:.2f}")


def demo_constructive_collapse():
    """Show how overloaded forms collapse into voids."""
    print_section("Constructive Collapse of Overloaded Forms")
    
    # Create a form that will accumulate contradictions
    form = create_thermodynamic_echoform(
        "philosophical_paradoxes",
        "echo"
    )
    
    print(f"\nForm: {form.anchor}")
    
    # Add increasingly contradictory philosophical statements
    paradoxes = [
        ("Everything is relative", "relativism", 1.0),
        ("Absolute truth exists", "absolutism", 1.0),
        ("I think therefore I am", "rationalism", 0.9),
        ("Experience precedes essence", "empiricism", 0.9),
        ("Free will exists", "libertarianism", 0.8),
        ("Everything is determined", "determinism", 0.8),
        ("Nothing has meaning", "nihilism", 1.0),
        ("Life has inherent purpose", "essentialism", 1.0),
        ("Knowledge is impossible", "skepticism", 0.9),
        ("We can know reality", "realism", 0.9),
    ]
    
    print("\nAdding paradoxical statements...")
    for i, (symbol, role, intensity) in enumerate(paradoxes):
        result = form.add_term_with_pressure_check(symbol, role, intensity)
        
        print(f"\n{i+1}. '{symbol[:30]}...'")
        print(f"   Pressure: {result['pressure_after']:.2f}")
        print(f"   Phase: {result['phase_after']}")
        
        # Check for collapse
        should_collapse, collapse_type = form.check_collapse_conditions()
        if should_collapse:
            print(f"\n*** COLLAPSE IMMINENT! Type: {collapse_type} ***")
            
            # Perform collapse
            void = form.constructive_collapse()
            
            print(f"\nCOLLAPSE COMPLETE!")
            print(f"Void properties:")
            print(f"  Origin: {void.origin_gid}")
            print(f"  Collapse pressure: {void.collapse_pressure:.2f}")
            print(f"  Potential energy: {void.potential_energy:.2f}")
            print(f"  Dimensions: {void.dimensions}")
            
            print(f"\nForm after collapse:")
            print(f"  Terms: {len(form.terms)}")
            print(f"  Phase: {form.phase}")
            print(f"  Topology: {form.topology}")
            
            break


def demo_echoform_entropy_decay():
    """Show how entropy affects time decay in thermodynamic context."""
    print_section("Entropy-Influenced Time Decay")
    
    # Create forms with different entropy levels
    low_entropy = create_thermodynamic_echoform("uniform_concepts", "echo")
    high_entropy = create_thermodynamic_echoform("diverse_concepts", "echo")
    
    # Low entropy - similar terms
    print("\n1. Low entropy form (uniform concepts):")
    for i in range(5):
        low_entropy.add_term(f"physics_law_{i}", "law", 1.0, timestamp=time.time() - i*3600)
    
    # High entropy - diverse terms
    print("\n2. High entropy form (diverse concepts):")
    diverse_terms = [
        ("quantum_mechanics", "physics", 0.3),
        ("impressionist_art", "art", 0.8),
        ("baroque_music", "music", 0.5),
        ("existentialism", "philosophy", 0.9),
        ("machine_learning", "computing", 0.7),
    ]
    
    for i, (symbol, role, intensity) in enumerate(diverse_terms):
        high_entropy.add_term(symbol, role, intensity, timestamp=time.time() - i*3600)
    
    # Compare entropy and decay
    print(f"\nLow entropy form:")
    print(f"  Entropy: {low_entropy.entropy():.3f}")
    print(f"  Base tau: {low_entropy.effective_tau():.1f}s")
    print(f"  Thermodynamic tau: {low_entropy.effective_tau_thermodynamic():.1f}s")
    print(f"  Phase: {low_entropy.update_phase_state()}")
    
    print(f"\nHigh entropy form:")
    print(f"  Entropy: {high_entropy.entropy():.3f}")
    print(f"  Base tau: {high_entropy.effective_tau():.1f}s")
    print(f"  Thermodynamic tau: {high_entropy.effective_tau_thermodynamic():.1f}s")
    print(f"  Phase: {high_entropy.update_phase_state()}")
    
    # Show intensity decay
    print("\nIntensity comparison:")
    print(f"Low entropy:")
    print(f"  Raw intensity: {low_entropy.intensity_sum(apply_time_decay=False):.3f}")
    print(f"  Decayed intensity: {low_entropy.intensity_sum(apply_time_decay=True):.3f}")
    
    print(f"High entropy:")
    print(f"  Raw intensity: {high_entropy.intensity_sum(apply_time_decay=False):.3f}")
    print(f"  Decayed intensity: {high_entropy.intensity_sum(apply_time_decay=True):.3f}")


def main():
    """Run all demonstrations."""
    print("\n" + "="*60)
    print("ECHOFORM THERMODYNAMICS DEMONSTRATION")
    print("="*60)
    
    demos = [
        demo_pressure_buildup,
        demo_phase_transitions,
        demo_energy_transfer,
        demo_constructive_collapse,
        demo_echoform_entropy_decay,
    ]
    
    for demo in demos:
        try:
            demo()
            time.sleep(0.5)
        except Exception as e:
            print(f"\nError in {demo.__name__}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("Demo completed!")
    print("="*60)


if __name__ == "__main__":
    main()
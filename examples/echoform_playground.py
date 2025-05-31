#!/usr/bin/env python3
"""
EchoForm Playground - Interactive demonstration of EchoForm capabilities
"""
import sys
sys.path.insert(0, 'src')

from kimera.echoform import EchoForm
from kimera.geoid import init_geoid
from kimera.cls import lattice_resolve, create_lattice_form
import json


def demo_basic_echoform():
    """Demonstrate basic EchoForm creation and manipulation"""
    print("🎯 Basic EchoForm Demo")
    print("-" * 25)
    
    # Create a basic EchoForm
    echo = EchoForm(anchor="Demo_001")
    print(f"Created: {echo}")
    
    # Add some terms
    echo.add_term("∂contradiction", "seed", 1.0)
    echo.add_term("∇resonance", "marker", 0.5)
    echo.add_term("⊕synthesis", "combiner", 0.3)
    
    print(f"After adding terms: {echo}")
    print(f"Total intensity: {echo.intensity_sum()}")
    print(f"Trace signature: {echo.trace_signature}")
    print()


def demo_phase_mutation():
    """Demonstrate phase mutation and trace chaining"""
    print("🔄 Phase Mutation Demo")
    print("-" * 25)
    
    # Create initial form
    echo1 = EchoForm(
        anchor="Mutation_Test",
        terms=[{"symbol": "α", "role": "primary", "intensity": 1.0}]
    )
    print(f"Original: {echo1}")
    print(f"Original trace: {echo1.trace_signature}")
    
    # Mutate through phases
    echo2 = echo1.mutate_phase("evolving")
    echo3 = echo2.mutate_phase("crystallized")
    echo4 = echo3.mutate_phase("archived")
    
    print(f"Evolved: {echo2}")
    print(f"Evolved trace: {echo2.trace_signature}")
    print(f"Crystallized: {echo3}")
    print(f"Crystallized trace: {echo3.trace_signature}")
    print(f"Archived: {echo4}")
    print(f"Archived trace: {echo4.trace_signature}")
    print()


def demo_serialization():
    """Demonstrate flatten/reinflate serialization"""
    print("💾 Serialization Demo")
    print("-" * 25)
    
    # Create complex form
    echo = EchoForm(
        anchor="Serialization_Test",
        domain="scar",
        terms=[
            {"symbol": "!∂Scar_007", "role": "contradiction_seed", "intensity": 1.0},
            {"symbol": "∇echo_response", "role": "resonance_marker", "intensity": 0.7},
            {"symbol": "⊕meta_synthesis", "role": "combiner", "intensity": 0.3, "metadata": {"source": "demo"}}
        ],
        phase="active",
        topology={
            "nodes": ["A", "B", "C"],
            "edges": [["A", "B"], ["B", "C"]],
            "properties": {"complexity": "medium"}
        }
    )
    
    print(f"Original: {echo}")
    print(f"Intensity sum: {echo.intensity_sum()}")
    
    # Serialize
    blob = echo.flatten()
    print(f"Serialized to {len(blob)} characters")
    
    # Pretty print JSON
    data = json.loads(blob)
    print("JSON structure:")
    for key, value in data.items():
        if isinstance(value, (list, dict)):
            print(f"  {key}: {type(value).__name__} with {len(value)} items")
        else:
            print(f"  {key}: {value}")
    
    # Deserialize
    restored = EchoForm.reinflate(blob)
    print(f"Restored: {restored}")
    print(f"Integrity check: {echo.trace_signature == restored.trace_signature}")
    print()


def demo_cls_integration():
    """Demonstrate CLS lattice integration"""
    print("🔗 CLS Integration Demo")
    print("-" * 25)
    
    # Create test geoids
    geo_a = init_geoid("Birds can fly", "en", ["demo"])
    geo_b = init_geoid("Birds cannot fly", "en", ["demo"])
    
    print(f"Geoid A: {geo_a.gid[:12]}... '{geo_a.raw}'")
    print(f"Geoid B: {geo_b.gid[:12]}... '{geo_b.raw}'")
    
    # Simple lattice resolve
    intensity = lattice_resolve(geo_a, geo_b)
    print(f"Lattice resolve intensity: {intensity}")
    
    # Create full lattice form
    lattice_form = create_lattice_form("contradiction_lattice", geo_a, geo_b)
    print(f"Lattice form: {lattice_form}")
    print(f"Lattice intensity: {lattice_form.intensity_sum()}")
    print(f"Lattice topology: {lattice_form.topology}")
    
    # Demonstrate lattice form evolution
    evolved_lattice = lattice_form.mutate_phase("resolved")
    evolved_lattice.add_term("⊕resolution", "outcome", 0.2)
    
    print(f"Evolved lattice: {evolved_lattice}")
    print(f"Final intensity: {evolved_lattice.intensity_sum()}")
    print()


def demo_complex_workflow():
    """Demonstrate a complex workflow combining all features"""
    print("🌟 Complex Workflow Demo")
    print("-" * 25)
    
    # Step 1: Create initial contradiction form
    scar_form = EchoForm(
        anchor="Complex_Workflow_001",
        domain="scar",
        terms=[{"symbol": "!∂initial", "role": "contradiction_seed", "intensity": 1.0}]
    )
    print(f"1. Initial scar form: {scar_form}")
    
    # Step 2: Create geoids for lattice
    geo_a = init_geoid("The sky is blue", "en", ["workflow"])
    geo_b = init_geoid("The sky is green", "en", ["workflow"])
    
    # Step 3: Create lattice form
    lattice_form = create_lattice_form("workflow_lattice", geo_a, geo_b)
    print(f"2. Lattice form: {lattice_form}")
    
    # Step 4: Evolve both forms
    evolved_scar = scar_form.mutate_phase("processing")
    evolved_scar.add_term("∇processing", "evolution_marker", 0.5)
    
    evolved_lattice = lattice_form.mutate_phase("analyzed")
    evolved_lattice.add_term("⊕analysis", "outcome", 0.3)
    
    print(f"3. Evolved scar: {evolved_scar}")
    print(f"4. Evolved lattice: {evolved_lattice}")
    
    # Step 5: Create synthesis form
    synthesis_form = EchoForm(
        anchor="Synthesis_" + evolved_scar.trace_signature[:8],
        domain="echo",
        terms=[
            {"symbol": f"∂{evolved_scar.trace_signature[:8]}", "role": "scar_ref", "intensity": 0.4},
            {"symbol": f"∂{evolved_lattice.trace_signature[:8]}", "role": "lattice_ref", "intensity": 0.4},
            {"symbol": "⊕synthesis", "role": "combiner", "intensity": 0.2}
        ],
        phase="synthesis",
        topology={
            "synthesis_type": "scar_lattice_combination",
            "source_traces": [evolved_scar.trace_signature, evolved_lattice.trace_signature],
            "workflow_id": "Complex_Workflow_001"
        }
    )
    
    print(f"5. Synthesis form: {synthesis_form}")
    print(f"   Total intensity: {synthesis_form.intensity_sum()}")
    print(f"   Synthesis topology: {synthesis_form.topology}")
    
    # Step 6: Serialize everything
    workflow_data = {
        "scar_form": evolved_scar.flatten(),
        "lattice_form": evolved_lattice.flatten(),
        "synthesis_form": synthesis_form.flatten()
    }
    
    print(f"6. Serialized workflow: {sum(len(v) for v in workflow_data.values())} total chars")
    
    # Step 7: Verify restoration
    restored_synthesis = EchoForm.reinflate(workflow_data["synthesis_form"])
    print(f"7. Restored synthesis integrity: {synthesis_form.trace_signature == restored_synthesis.trace_signature}")
    print()


def main():
    """Run all demonstrations"""
    print("🎮 EchoForm Playground")
    print("=" * 35)
    print("Demonstrating EchoForm v0.7.1 capabilities\n")
    
    demos = [
        demo_basic_echoform,
        demo_phase_mutation,
        demo_serialization,
        demo_cls_integration,
        demo_complex_workflow
    ]
    
    for demo in demos:
        try:
            demo()
        except Exception as e:
            print(f"❌ {demo.__name__} failed: {e}")
            import traceback
            traceback.print_exc()
            print()
    
    print("🎉 EchoForm playground complete!")
    print("\nKey capabilities demonstrated:")
    print("  • Basic form creation and term management")
    print("  • Phase mutation with trace chaining")
    print("  • JSON serialization and restoration")
    print("  • CLS lattice integration")
    print("  • Complex multi-form workflows")
    print("  • Topology management and synthesis")


if __name__ == "__main__":
    main()
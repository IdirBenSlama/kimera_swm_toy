"""
Thermodynamic Phase Diagram Demonstration
========================================

This demo generates and visualizes the thermodynamic phase diagram for a set of geoids
using the Kimera SWM thermodynamics module.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
import matplotlib.pyplot as plt
from kimera.geoid import init_geoid
from kimera.thermodynamics import create_thermodynamic_system


def generate_sample_geoids():
    """Create a diverse set of geoids for demonstration."""
    texts = [
        # Solid: highly coherent, low contradiction
        "Mathematics is the language of the universe.",
        "The sum of the angles in a triangle is 180 degrees.",
        "Pi is an irrational number.",
        "The Pythagorean theorem relates the sides of a right triangle.",
        # Liquid: moderate coherence, some contradiction
        "Mathematics is a human invention.",
        "Some triangles have angle sums greater than 180 degrees (non-Euclidean).",
        "Pi is sometimes approximated as 22/7.",
        # Gas: low coherence, high contradiction
        "Triangles can have four sides.",
        "Pi is exactly 3.",
        "The sum of the angles in a triangle is 200 degrees.",
        # Plasma: extreme contradiction, near collapse
        "A triangle is a square.",
        "Pi is a negative number.",
        "Triangles have no angles."
    ]
    return [init_geoid(text) for text in texts]


def plot_phase_diagram(phases, system):
    """Visualize the phase diagram as a scatter plot."""
    colors = {
        "solid": "blue",
        "liquid": "green",
        "gas": "orange",
        "plasma": "red"
    }
    markers = {
        "solid": "o",
        "liquid": "s",
        "gas": "^",
        "plasma": "x"
    }
    plt.figure(figsize=(8, 6))
    for phase, geoids in phases.items():
        pressures = []
        coherences = []
        for geoid in geoids:
            eq = system.find_equilibrium_point(geoid, sum(phases.values(), []))
            pressures.append(eq["pressure"])
            coherences.append(eq["coherence"])
        if geoids:
            plt.scatter(pressures, coherences, c=colors[phase], marker=markers[phase], label=f"{phase.capitalize()} ({len(geoids)})", s=80)
    plt.xlabel("Semantic Pressure")
    plt.ylabel("Coherence")
    plt.title("Kimera SWM Thermodynamic Phase Diagram")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
    print("Kimera SWM Thermodynamic Phase Diagram Demo")
    print("=" * 50)
    geoids = generate_sample_geoids()
    system = create_thermodynamic_system(pressure_threshold=7.0)
    phases = system.phase_diagram(geoids)
    
    # Print phase statistics
    print("\nPhase Statistics:")
    for phase, items in phases.items():
        print(f"  {phase.capitalize()}: {len(items)} geoids")
    
    # Show a few examples from each phase
    for phase, items in phases.items():
        if items:
            print(f"\nExamples from {phase.capitalize()} phase:")
            for geoid in items[:2]:
                eq = system.find_equilibrium_point(geoid, geoids)
                print(f"  - '{geoid.raw[:40]}...' | Pressure: {eq['pressure']:.2f}, Coherence: {eq['coherence']:.2f}")
    
    # Visualize
    plot_phase_diagram(phases, system)

if __name__ == "__main__":
    main()

"""
Pressure-Collapse Dynamics Experiment
====================================

This script simulates semantic pressure accumulation and collapse events in a set of geoids,
validating the theoretical predictions of the Kimera SWM thermodynamic framework.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
import matplotlib.pyplot as plt
from kimera.geoid import init_geoid
from kimera.thermodynamics import create_thermodynamic_system
import random


def generate_contradictory_geoids():
    """Create geoids with increasing levels of contradiction."""
    base = "The sum of the angles in a triangle is 180 degrees."
    contradictions = [
        "The sum of the angles in a triangle is 200 degrees.",
        "Triangles can have four sides.",
        "A triangle is a square.",
        "Triangles have no angles.",
        "Pi is a negative number.",
        "Pi is exactly 3.",
        "Mathematics is a human invention.",
        "Mathematics is the language of the universe."
    ]
    geoids = [init_geoid(base)]
    for c in contradictions:
        geoids.append(init_geoid(c))
    return geoids


def simulate_pressure_and_collapse(system, geoids, steps=10):
    """Simulate pressure accumulation and collapse events."""
    pressure_history = {g.gid: [] for g in geoids}
    collapse_events = []
    for step in range(steps):
        # Randomly select pairs to interact
        for g in geoids:
            others = [o for o in geoids if o.gid != g.gid]
            sample = random.sample(others, min(3, len(others)))
            system.calculate_pressure(g, sample)
            pressure_history[g.gid].append(system.pressures.get(g.gid, None).value if g.gid in system.pressures else 0.0)
            # Check for collapse
            should_collapse, collapse_type = system.check_collapse_conditions(g)
            if should_collapse:
                void = system.constructive_collapse(g, collapse_type)
                collapse_events.append({
                    "step": step,
                    "geoid": g.raw,
                    "collapse_type": collapse_type,
                    "pressure": void.collapse_pressure
                })
    return pressure_history, collapse_events


def plot_pressure_evolution(pressure_history, collapse_events, geoids):
    """Plot the evolution of pressure for each geoid and mark collapse events."""
    plt.figure(figsize=(10, 6))
    for g in geoids:
        plt.plot(pressure_history[g.gid], label=g.raw[:30] + ("..." if len(g.raw) > 30 else ""))
    for event in collapse_events:
        plt.axvline(event["step"], color="red", linestyle="--", alpha=0.5)
    plt.xlabel("Simulation Step")
    plt.ylabel("Semantic Pressure")
    plt.title("Pressure Evolution and Collapse Events")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.show()


def main():
    print("Kimera SWM Pressure-Collapse Dynamics Experiment")
    print("=" * 50)
    geoids = generate_contradictory_geoids()
    system = create_thermodynamic_system(pressure_threshold=7.0)
    pressure_history, collapse_events = simulate_pressure_and_collapse(system, geoids, steps=15)
    
    print(f"\nCollapse Events ({len(collapse_events)} total):")
    for event in collapse_events:
        print(f"  Step {event['step']}: '{event['geoid'][:40]}...' collapsed via {event['collapse_type']} (pressure={event['pressure']:.2f})")
    
    plot_pressure_evolution(pressure_history, collapse_events, geoids)

if __name__ == "__main__":
    main()

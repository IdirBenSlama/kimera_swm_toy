"""
Phase Diagram Visualization Demo
--------------------------------
Generates a thermodynamic phase diagram using kimera.thermodynamics_phase.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from kimera.geoid import init_geoid
from kimera.thermodynamics_phase import compute_phase_metrics, plot_phase_diagram
from kimera.thermodynamics_v3 import ThermodynamicSystemV3 as ThermodynamicSystem

SAMPLE_TEXTS = [
    # coherent
    "Energy is conserved in a closed system.",
    "Entropy measures disorder in thermodynamics.",
    "Heat flows from hot to cold bodies.",
    # moderate contradictions
    "Energy can be created from nothing.",
    "Entropy always decreases spontaneously.",
    # strong contradictions
    "Cold objects heat hotter ones spontaneously.",
    "Entropy is a negative quantity.",
]

def main():
    geoids = [init_geoid(t) for t in SAMPLE_TEXTS]
    system = ThermodynamicSystem(pressure_threshold=6.0)
    import matplotlib.pyplot as plt
    metrics = compute_phase_metrics(geoids, system=system)
    # Generate plot without displaying (headless)
    plot_phase_diagram(metrics, system=system, annotate=1, show=False)
    output = Path(__file__).with_suffix(".png")
    plt.savefig(output, dpi=200)
    print(f"Phase diagram saved to {output}")

if __name__ == "__main__":
    main()

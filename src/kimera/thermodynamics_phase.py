"""kimera.thermodynamics_phase
================================
Advanced thermodynamic phase-diagram utilities for Kimera SWM.

This helper module builds upon ``kimera.thermodynamics`` by providing:

1. ``compute_phase_metrics``   – calculate pressure / coherence for each geoid
2. ``detect_critical_points``  – automatic detection of phase-transition points
3. ``plot_phase_diagram``      – high-level visualisation with critical lines

The implementation is **self-contained** and uses only NumPy/Matplotlib in
addition to Kimera core modules.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Tuple

import numpy as np
import matplotlib.pyplot as plt

from .geoid import Geoid
from .thermodynamics import ThermodynamicSystem

###############################################################################
# Data classes
###############################################################################

@dataclass
class PhaseMetrics:
    """Pressure / coherence metrics for a single Geoid."""
    gid: str
    raw: str
    pressure: float
    coherence: float
    phase: str

###############################################################################
# Core API
###############################################################################

PHASE_COLOURS = {
    "solid": "#1f77b4",   # blue
    "liquid": "#2ca02c",  # green
    "gas": "#ff7f0e",    # orange
    "plasma": "#d62728", # red
}

PHASE_THRESHOLDS = {
    "solid": (2.0, 0.7),   # (max pressure, min coherence)
    "liquid": (5.0, 0.4),
}

def _classify(pressure: float, coherence: float, threshold: float) -> str:
    """Classify into thermodynamic phase based on heuristics."""
    if pressure < PHASE_THRESHOLDS["solid"][0] and coherence > PHASE_THRESHOLDS["solid"][1]:
        return "solid"
    if pressure < PHASE_THRESHOLDS["liquid"][0] and coherence > PHASE_THRESHOLDS["liquid"][1]:
        return "liquid"
    if pressure < threshold:
        return "gas"
    return "plasma"


def compute_phase_metrics(
    geoids: List[Geoid],
    *,
    system: ThermodynamicSystem | None = None,
) -> List[PhaseMetrics]:
    """Compute pressure/coherence and assign phase for each provided geoid."""
    if system is None:
        system = ThermodynamicSystem()
    # Ensure we have pre-computed pressure values
    metrics: List[PhaseMetrics] = []
    for geoid in geoids:
        eq = system.find_equilibrium_point(geoid, geoids)
        metrics.append(
            PhaseMetrics(
                gid=geoid.gid,
                raw=geoid.raw,
                pressure=eq["pressure"],
                coherence=eq["coherence"],
                phase=_classify(eq["pressure"], eq["coherence"], system.pressure_threshold),
            )
        )
    return metrics


def detect_critical_points(metrics: List[PhaseMetrics]) -> Dict[str, float]:
    """Detect approximate critical points for phase transitions.

    Returns dictionary mapping *phase_boundary* -> critical pressure value.
    """
    # Simple heuristic: median pressure of highest-pressure item in each phase
    boundaries: Dict[str, float] = {}
    phase_order = ["solid", "liquid", "gas"]
    for phase in phase_order:
        pressures = [m.pressure for m in metrics if m.phase == phase]
        if pressures:
            boundaries[f"{phase}_max"] = float(np.percentile(pressures, 95))
    # plasma boundary is system threshold
    max_pressure = max(m.pressure for m in metrics)
    boundaries["plasma_min"] = max_pressure
    return boundaries


def plot_phase_diagram(
    metrics: List[PhaseMetrics],
    *,
    system: ThermodynamicSystem | None = None,
    show=True,
    figsize: Tuple[int, int] = (8, 6),
    annotate: int = 0,
):
    """Plot pressure vs coherence coloured by phase and show critical boundaries."""
    if system is None:
        system = ThermodynamicSystem()
    plt.figure(figsize=figsize)

    # Scatter per phase
    for phase, colour in PHASE_COLOURS.items():
        xs = [m.pressure for m in metrics if m.phase == phase]
        ys = [m.coherence for m in metrics if m.phase == phase]
        if xs:
            plt.scatter(xs, ys, label=f"{phase.capitalize()} ({len(xs)})", color=colour, s=60, alpha=0.8)
            # Optionally annotate first *annotate* points
            if annotate > 0:
                for m in [k for k in metrics if k.phase == phase][:annotate]:
                    plt.text(m.pressure, m.coherence, m.raw[:12] + "...", fontsize=7, alpha=0.7)

    # Draw vertical critical lines (pressure thresholds)
    boundaries = detect_critical_points(metrics)
    solid_max = boundaries.get("solid_max", 0)
    liquid_max = boundaries.get("liquid_max", 0)
    gas_max = boundaries.get("gas_max", system.pressure_threshold)
    plt.axvline(solid_max, color="#1f77b4", linestyle="--", alpha=0.4)
    plt.axvline(liquid_max, color="#2ca02c", linestyle="--", alpha=0.4)
    plt.axvline(system.pressure_threshold, color="#d62728", linestyle=":", alpha=0.6, label="Collapse Threshold")

    plt.xlabel("Semantic Pressure")
    plt.ylabel("Coherence")
    plt.title("Thermodynamic Phase Diagram (Kimera SWM)")
    plt.legend(frameon=False)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    if show:
        plt.show()

###############################################################################
# CLI helper
###############################################################################

if __name__ == "__main__":  # pragma: no cover
    import argparse, sys
    parser = argparse.ArgumentParser(description="Generate phase diagram for sample texts")
    parser.add_argument("texts", nargs="*", help="Sample texts to embed as geoids")
    parser.add_argument("--threshold", type=float, default=7.0, help="Collapse pressure threshold")
    args = parser.parse_args()

    if not args.texts:
        print("Provide sample texts as positional arguments.", file=sys.stderr)
        sys.exit(1)

    from .geoid import init_geoid

    geoids = [init_geoid(t) for t in args.texts]
    system = ThermodynamicSystem(pressure_threshold=args.threshold)
    metrics = compute_phase_metrics(geoids, system=system)
    plot_phase_diagram(metrics, system=system)

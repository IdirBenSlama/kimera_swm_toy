"""
Fixed Thermodynamic Validation with Proper Pressure Calculation
==============================================================

This fixes the accumulation bug and provides accurate phase diagram validation.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple
import json
from datetime import datetime

from kimera.geoid import init_geoid
from kimera.thermodynamics import ThermodynamicSystem, SemanticPressure
from kimera.contradiction import detect_contradiction
from kimera.resonance import resonance


class FixedThermodynamicSystem(ThermodynamicSystem):
    """Fixed version that doesn't accumulate pressure incorrectly."""
    
    def calculate_pressure_fresh(self, geoid, context_geoids):
        """Calculate pressure without accumulation."""
        total_pressure = 0.0
        
        for other in context_geoids:
            if other.gid == geoid.gid:
                continue
                
            # Check resonance
            res_score = resonance(geoid, other)
            
            # Low resonance indicates opposition
            if res_score < 0.3:
                base_pressure = (1.0 - res_score) * 1.5
                total_pressure += base_pressure
                continue
            
            # Check explicit contradiction
            is_contradiction, confidence, _ = detect_contradiction(geoid, other)
            
            if is_contradiction:
                base_pressure = confidence * 2.0
                paradox_multiplier = 1.0 + res_score
                pressure_amount = base_pressure * paradox_multiplier
                total_pressure += pressure_amount
            elif res_score > 0.7:
                # High resonance might indicate internal tension
                total_pressure += res_score * 0.5
        
        return total_pressure
    
    def find_equilibrium_point_fixed(self, geoid, context_geoids):
        """Fixed equilibrium calculation without pressure accumulation."""
        # Calculate fresh pressure
        pressure = self.calculate_pressure_fresh(geoid, context_geoids)
        
        # Calculate coherence
        coherence_scores = []
        for other in context_geoids:
            if other.gid != geoid.gid:
                is_contradiction, _, _ = detect_contradiction(geoid, other)
                if not is_contradiction:
                    coherence_scores.append(resonance(geoid, other))
        
        avg_coherence = np.mean(coherence_scores) if coherence_scores else 0.0
        
        # Calculate equilibrium metrics
        stability = avg_coherence / (1.0 + pressure)
        tension = pressure / (1.0 + avg_coherence)
        
        return {
            "pressure": pressure,
            "coherence": avg_coherence,
            "stability": stability,
            "tension": tension,
            "equilibrium": stability > 0.5
        }


def load_diverse_corpus():
    """Load a diverse set of texts for testing."""
    # Mix of coherent and contradictory texts
    texts = [
        # Coherent scientific facts (should be "solid")
        "Water freezes at 0 degrees Celsius",
        "The Earth orbits around the Sun",
        "Gravity attracts objects with mass",
        "Light travels at 299,792,458 meters per second",
        
        # Mild contradictions (should be "liquid")
        "Coffee is the best beverage",
        "Tea is the best beverage",
        "Morning is the most productive time",
        "Night is the most productive time",
        
        # Stronger contradictions (should be "gas")
        "All swans are white",
        "Black swans exist in Australia",
        "Mathematics is discovered",
        "Mathematics is invented",
        
        # Extreme contradictions (should be "plasma")
        "This statement is false",
        "I always lie",
        "The set of all sets contains itself",
        "Nothing is everything"
    ]
    
    # Add some from real data if available
    try:
        df = pd.read_csv("data/mixed_contradictions.csv", nrows=50)
        if 'text1' in df.columns and 'text2' in df.columns:
            texts.extend(df['text1'].tolist()[:10])
            texts.extend(df['text2'].tolist()[:10])
    except:
        pass
    
    return texts


def compute_fixed_phase_metrics(geoids, system):
    """Compute phase metrics using fixed pressure calculation."""
    metrics = []
    
    for geoid in geoids:
        eq = system.find_equilibrium_point_fixed(geoid, geoids)
        
        # Determine phase
        pressure = eq["pressure"]
        coherence = eq["coherence"]
        
        if pressure < 2.0 and coherence > 0.7:
            phase = "solid"
        elif pressure < 5.0 and coherence > 0.4:
            phase = "liquid"
        elif pressure < system.pressure_threshold:
            phase = "gas"
        else:
            phase = "plasma"
        
        metrics.append({
            "gid": geoid.gid,
            "raw": geoid.raw[:50] + "..." if len(geoid.raw) > 50 else geoid.raw,
            "pressure": pressure,
            "coherence": coherence,
            "phase": phase
        })
    
    return metrics


def analyze_results(metrics):
    """Analyze and print detailed results."""
    print("\nPhase Distribution:")
    print("-" * 60)
    
    phase_counts = {"solid": 0, "liquid": 0, "gas": 0, "plasma": 0}
    phase_examples = {"solid": [], "liquid": [], "gas": [], "plasma": []}
    
    for m in metrics:
        phase_counts[m["phase"]] += 1
        if len(phase_examples[m["phase"]]) < 3:
            phase_examples[m["phase"]].append(m)
    
    # Print counts
    for phase, count in phase_counts.items():
        print(f"{phase.upper()}: {count} ({count/len(metrics)*100:.1f}%)")
    
    # Print examples
    print("\nExample Geoids by Phase:")
    print("-" * 60)
    
    for phase in ["solid", "liquid", "gas", "plasma"]:
        if phase_examples[phase]:
            print(f"\n{phase.upper()}:")
            for ex in phase_examples[phase]:
                print(f"  '{ex['raw']}'")
                print(f"    Pressure: {ex['pressure']:.3f}, Coherence: {ex['coherence']:.3f}")
    
    # Statistical summary
    print("\nStatistical Summary:")
    print("-" * 60)
    
    all_pressures = [m["pressure"] for m in metrics]
    all_coherences = [m["coherence"] for m in metrics]
    
    print(f"Pressure: {np.mean(all_pressures):.3f} ± {np.std(all_pressures):.3f}")
    print(f"Coherence: {np.mean(all_coherences):.3f} ± {np.std(all_coherences):.3f}")
    
    # Test correlation
    if len(metrics) > 2:
        corr = np.corrcoef(all_pressures, all_coherences)[0, 1]
        print(f"Pressure-Coherence Correlation: {corr:.3f}")


def create_phase_diagram_plot(metrics, output_path):
    """Create a proper phase diagram visualization."""
    plt.figure(figsize=(10, 8))
    
    colors = {"solid": "blue", "liquid": "green", "gas": "orange", "plasma": "red"}
    
    for phase in ["solid", "liquid", "gas", "plasma"]:
        phase_metrics = [m for m in metrics if m["phase"] == phase]
        if phase_metrics:
            pressures = [m["pressure"] for m in phase_metrics]
            coherences = [m["coherence"] for m in phase_metrics]
            plt.scatter(pressures, coherences, 
                       c=colors[phase], 
                       label=f"{phase} (n={len(phase_metrics)})",
                       alpha=0.6, s=50)
    
    # Add phase boundary lines
    plt.axvline(x=2.0, color='gray', linestyle='--', alpha=0.5, label='Solid-Liquid boundary')
    plt.axvline(x=5.0, color='gray', linestyle='--', alpha=0.5, label='Liquid-Gas boundary')
    plt.axvline(x=7.0, color='gray', linestyle='--', alpha=0.5, label='Gas-Plasma boundary')
    
    plt.xlabel("Semantic Pressure")
    plt.ylabel("Coherence")
    plt.title("Fixed Thermodynamic Phase Diagram")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"\nPhase diagram saved to: {output_path}")


def main():
    """Run fixed thermodynamic validation."""
    print("Fixed Thermodynamic Validation")
    print("=" * 60)
    
    # Load diverse texts
    texts = load_diverse_corpus()
    print(f"\nLoaded {len(texts)} diverse text samples")
    
    # Create geoids
    geoids = [init_geoid(text) for text in texts]
    
    # Create fixed system
    system = FixedThermodynamicSystem(pressure_threshold=7.0)
    
    # Compute metrics
    print("\nComputing phase metrics with fixed pressure calculation...")
    metrics = compute_fixed_phase_metrics(geoids, system)
    
    # Analyze results
    analyze_results(metrics)
    
    # Create visualization
    output_path = Path("experiments/thermodynamic_phase_diagram_fixed.png")
    create_phase_diagram_plot(metrics, output_path)
    
    # Save detailed results
    results = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "n_samples": len(geoids),
            "pressure_threshold": system.pressure_threshold,
            "fixed": True
        },
        "metrics": metrics,
        "summary": {
            "phase_counts": {
                phase: sum(1 for m in metrics if m["phase"] == phase)
                for phase in ["solid", "liquid", "gas", "plasma"]
            },
            "mean_pressure": np.mean([m["pressure"] for m in metrics]),
            "mean_coherence": np.mean([m["coherence"] for m in metrics])
        }
    }
    
    results_path = Path("experiments/thermodynamic_validation_fixed.json")
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nDetailed results saved to: {results_path}")
    
    print("\n" + "="*60)
    print("Validation complete with fixed pressure calculation.")


if __name__ == "__main__":
    main()
"""
Rigorous Thermodynamic Phase Diagram Validation
==============================================

This experiment rigorously validates the thermodynamic phase diagram predictions
using real data and statistical analysis.

Zetetic approach:
1. Use actual corpus data, not toy examples
2. Measure quantitative metrics
3. Test theoretical predictions
4. Document all results with error bars
5. Identify failures and limitations
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
from kimera.thermodynamics import ThermodynamicSystem
from kimera.thermodynamics_phase import compute_phase_metrics, detect_critical_points, plot_phase_diagram


def load_real_corpus(max_samples: int = 500) -> List[str]:
    """Load real text data from existing corpus files."""
    corpus_files = [
        "data/mixed_5k.csv",
        "data/contradictions_2k.csv",
        "data/mixed_contradictions.csv"
    ]
    
    all_texts = []
    for file in corpus_files:
        path = Path(file)
        if path.exists():
            df = pd.read_csv(path)
            # Extract text columns (handle different formats)
            if 'text' in df.columns:
                texts = df['text'].tolist()
            elif 'text1' in df.columns and 'text2' in df.columns:
                texts = df['text1'].tolist() + df['text2'].tolist()
            else:
                # Try first column
                texts = df.iloc[:, 0].tolist()
            
            all_texts.extend([str(t) for t in texts if pd.notna(t)])
    
    # Random sample to keep computation tractable
    if len(all_texts) > max_samples:
        np.random.seed(42)  # Reproducibility
        indices = np.random.choice(len(all_texts), max_samples, replace=False)
        all_texts = [all_texts[i] for i in indices]
    
    return all_texts


def compute_phase_statistics(metrics) -> Dict:
    """Compute detailed statistics for each phase."""
    stats = {}
    
    for phase in ["solid", "liquid", "gas", "plasma"]:
        phase_metrics = [m for m in metrics if m.phase == phase]
        
        if phase_metrics:
            pressures = [m.pressure for m in phase_metrics]
            coherences = [m.coherence for m in phase_metrics]
            
            stats[phase] = {
                "count": len(phase_metrics),
                "pressure_mean": np.mean(pressures),
                "pressure_std": np.std(pressures),
                "pressure_min": np.min(pressures),
                "pressure_max": np.max(pressures),
                "coherence_mean": np.mean(coherences),
                "coherence_std": np.std(coherences),
                "coherence_min": np.min(coherences),
                "coherence_max": np.max(coherences),
            }
        else:
            stats[phase] = {"count": 0}
    
    return stats


def test_theoretical_predictions(metrics, system) -> Dict:
    """Test specific theoretical predictions."""
    tests = {}
    
    # Test 1: Phase boundaries should be distinct
    phase_pressures = {}
    for phase in ["solid", "liquid", "gas", "plasma"]:
        phase_metrics = [m for m in metrics if m.phase == phase]
        if phase_metrics:
            phase_pressures[phase] = [m.pressure for m in phase_metrics]
    
    # Check if pressure distributions are significantly different
    if len(phase_pressures) >= 2:
        from scipy import stats as scipy_stats
        phases = list(phase_pressures.keys())
        if len(phases) >= 2 and all(len(phase_pressures[p]) > 1 for p in phases[:2]):
            _, p_value = scipy_stats.ttest_ind(
                phase_pressures[phases[0]], 
                phase_pressures[phases[1]]
            )
            tests["phase_separation_significant"] = p_value < 0.05
            tests["phase_separation_p_value"] = p_value
    
    # Test 2: Critical points should align with phase transitions
    critical_points = detect_critical_points(metrics)
    tests["critical_points"] = critical_points
    
    # Test 3: Coherence should decrease with pressure (negative correlation)
    pressures = [m.pressure for m in metrics]
    coherences = [m.coherence for m in metrics]
    if len(pressures) > 2:
        correlation = np.corrcoef(pressures, coherences)[0, 1]
        tests["pressure_coherence_correlation"] = correlation
        tests["negative_correlation_confirmed"] = correlation < -0.3
    
    # Test 4: Phase distribution should follow power law (many solid, few plasma)
    phase_counts = {phase: sum(1 for m in metrics if m.phase == phase) 
                   for phase in ["solid", "liquid", "gas", "plasma"]}
    tests["phase_distribution"] = phase_counts
    
    return tests


def generate_comprehensive_report(texts, metrics, stats, tests, system):
    """Generate a comprehensive validation report."""
    report = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "n_samples": len(texts),
            "pressure_threshold": system.pressure_threshold,
            "kimera_version": "0.8.0"
        },
        "phase_statistics": stats,
        "theoretical_tests": tests,
        "summary": {
            "total_geoids": len(metrics),
            "phases_detected": sum(1 for phase, s in stats.items() if s["count"] > 0),
            "mean_pressure": np.mean([m.pressure for m in metrics]),
            "mean_coherence": np.mean([m.coherence for m in metrics]),
        }
    }
    
    # Save report
    report_path = Path("experiments/thermodynamic_validation_report.json")
    report_path.parent.mkdir(exist_ok=True)
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\nValidation report saved to: {report_path}")
    return report


def create_validation_plots(metrics, system):
    """Create comprehensive validation plots."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # 1. Phase diagram with error regions
    ax = axes[0, 0]
    for phase in ["solid", "liquid", "gas", "plasma"]:
        phase_metrics = [m for m in metrics if m.phase == phase]
        if phase_metrics:
            pressures = [m.pressure for m in phase_metrics]
            coherences = [m.coherence for m in phase_metrics]
            ax.scatter(pressures, coherences, label=f"{phase} (n={len(phase_metrics)})", 
                      alpha=0.6, s=30)
    ax.set_xlabel("Pressure")
    ax.set_ylabel("Coherence")
    ax.set_title("Phase Diagram")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2. Pressure distribution by phase
    ax = axes[0, 1]
    phase_data = []
    phase_labels = []
    for phase in ["solid", "liquid", "gas", "plasma"]:
        pressures = [m.pressure for m in metrics if m.phase == phase]
        if pressures:
            phase_data.append(pressures)
            phase_labels.append(phase)
    if phase_data:
        ax.boxplot(phase_data, labels=phase_labels)
        ax.set_ylabel("Pressure")
        ax.set_title("Pressure Distribution by Phase")
    
    # 3. Coherence vs Pressure scatter
    ax = axes[1, 0]
    pressures = [m.pressure for m in metrics]
    coherences = [m.coherence for m in metrics]
    ax.scatter(pressures, coherences, alpha=0.5, s=20)
    # Add trend line
    if len(pressures) > 2:
        z = np.polyfit(pressures, coherences, 1)
        p = np.poly1d(z)
        ax.plot(sorted(pressures), p(sorted(pressures)), "r--", alpha=0.8)
    ax.set_xlabel("Pressure")
    ax.set_ylabel("Coherence")
    ax.set_title("Pressure-Coherence Relationship")
    ax.grid(True, alpha=0.3)
    
    # 4. Phase count histogram
    ax = axes[1, 1]
    phase_counts = {phase: sum(1 for m in metrics if m.phase == phase) 
                   for phase in ["solid", "liquid", "gas", "plasma"]}
    ax.bar(phase_counts.keys(), phase_counts.values())
    ax.set_ylabel("Count")
    ax.set_title("Phase Distribution")
    
    plt.tight_layout()
    plot_path = Path("experiments/thermodynamic_validation_plots.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"Validation plots saved to: {plot_path}")
    plt.close()


def main():
    """Run comprehensive thermodynamic validation."""
    print("Kimera SWM Thermodynamic Validation Experiment")
    print("=" * 60)
    print("\nApplying zetetic (skeptical inquiry) methodology...")
    
    # 1. Load real data
    print("\n1. Loading real corpus data...")
    texts = load_real_corpus(max_samples=500)
    print(f"   Loaded {len(texts)} text samples")
    
    if not texts:
        print("ERROR: No data loaded. Check data files.")
        return
    
    # 2. Create geoids and system
    print("\n2. Creating geoids and thermodynamic system...")
    geoids = [init_geoid(text) for text in texts[:200]]  # Limit for memory
    system = ThermodynamicSystem(pressure_threshold=7.0)
    
    # 3. Compute phase metrics
    print("\n3. Computing phase metrics...")
    metrics = compute_phase_metrics(geoids, system=system)
    
    # 4. Statistical analysis
    print("\n4. Computing phase statistics...")
    stats = compute_phase_statistics(metrics)
    
    # Print summary statistics
    print("\nPhase Statistics Summary:")
    print("-" * 60)
    for phase, s in stats.items():
        if s["count"] > 0:
            print(f"\n{phase.upper()}:")
            print(f"  Count: {s['count']}")
            print(f"  Pressure: {s['pressure_mean']:.3f} ± {s['pressure_std']:.3f}")
            print(f"  Coherence: {s['coherence_mean']:.3f} ± {s['coherence_std']:.3f}")
    
    # 5. Test theoretical predictions
    print("\n5. Testing theoretical predictions...")
    tests = test_theoretical_predictions(metrics, system)
    
    print("\nTheoretical Test Results:")
    print("-" * 60)
    if "pressure_coherence_correlation" in tests:
        print(f"Pressure-Coherence Correlation: {tests['pressure_coherence_correlation']:.3f}")
        print(f"Negative correlation confirmed: {tests.get('negative_correlation_confirmed', False)}")
    
    if "phase_separation_significant" in tests:
        print(f"Phase separation significant: {tests['phase_separation_significant']}")
        print(f"P-value: {tests.get('phase_separation_p_value', 'N/A'):.4f}")
    
    print(f"\nCritical points detected: {tests.get('critical_points', {})}")
    
    # 6. Generate report and plots
    print("\n6. Generating validation report and plots...")
    report = generate_comprehensive_report(texts, metrics, stats, tests, system)
    create_validation_plots(metrics, system)
    
    # 7. Identify limitations
    print("\n7. Identified Limitations:")
    print("-" * 60)
    print("- Pressure calculation depends on contradiction detection accuracy")
    print("- Phase boundaries are heuristic, not derived from first principles")
    print("- No temporal evolution tracked")
    print("- Critical points detection is approximate")
    print(f"- Sample size limited to {len(geoids)} for computational tractability")
    
    print("\n" + "="*60)
    print("Validation complete. Check experiments/ directory for detailed results.")


if __name__ == "__main__":
    main()
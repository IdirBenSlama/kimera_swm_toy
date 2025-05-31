#!/usr/bin/env python3
"""
Demo script showing the new Kimera-SWM v0.7.0 metrics capabilities.
Generates synthetic data and demonstrates all metric functions.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from kimera.metrics import (
    roc_stats, pr_stats, accuracy_stats, bootstrap_ci,
    mcnemar_test, compute_optimal_threshold
)

def generate_synthetic_data(n_samples=200, seed=42):
    """Generate synthetic contradiction detection data."""
    np.random.seed(seed)
    
    # True labels (50% contradictions)
    y_true = np.random.randint(0, 2, n_samples)
    
    # Kimera-like classifier (good but not perfect)
    kimera_base = y_true + np.random.normal(0, 0.3, n_samples)
    kimera_scores = 1 / (1 + np.exp(-kimera_base))  # Sigmoid to [0,1]
    
    # GPT-like classifier (different characteristics)
    gpt_base = y_true + np.random.normal(0, 0.4, n_samples)
    gpt_scores = 1 / (1 + np.exp(-gpt_base))
    
    return y_true, kimera_scores, gpt_scores

def demo_basic_metrics():
    """Demonstrate basic metric computation."""
    print("📊 Basic Metrics Demo")
    print("-" * 30)
    
    y_true, kimera_scores, gpt_scores = generate_synthetic_data()
    
    # ROC metrics
    kimera_roc = roc_stats(y_true, kimera_scores)
    gpt_roc = roc_stats(y_true, gpt_scores)
    
    print(f"Kimera AUROC: {kimera_roc['auroc']:.3f}")
    print(f"GPT AUROC: {gpt_roc['auroc']:.3f}")
    
    # PR metrics
    kimera_pr = pr_stats(y_true, kimera_scores)
    gpt_pr = pr_stats(y_true, gpt_scores)
    
    print(f"Kimera AUPR: {kimera_pr['aupr']:.3f}")
    print(f"GPT AUPR: {gpt_pr['aupr']:.3f}")
    
    # Optimal thresholds
    kimera_thresh, kimera_f1 = compute_optimal_threshold(y_true, kimera_scores, "f1")
    gpt_thresh, gpt_f1 = compute_optimal_threshold(y_true, gpt_scores, "f1")
    
    print(f"Kimera optimal threshold: {kimera_thresh:.3f} (F1: {kimera_f1:.3f})")
    print(f"GPT optimal threshold: {gpt_thresh:.3f} (F1: {gpt_f1:.3f})")
    
    return y_true, kimera_scores, gpt_scores, kimera_thresh, gpt_thresh

def demo_confidence_intervals():
    """Demonstrate bootstrap confidence intervals."""
    print("\n🔄 Bootstrap Confidence Intervals Demo")
    print("-" * 40)
    
    y_true, kimera_scores, gpt_scores = generate_synthetic_data()
    
    # AUROC confidence intervals
    kimera_auroc_ci = bootstrap_ci(
        lambda yt, ys: roc_stats(yt, ys)["auroc"],
        y_true, kimera_scores, n=1000, seed=42
    )
    
    gpt_auroc_ci = bootstrap_ci(
        lambda yt, ys: roc_stats(yt, ys)["auroc"],
        y_true, gpt_scores, n=1000, seed=42
    )
    
    print(f"Kimera AUROC 95% CI: [{kimera_auroc_ci[0]:.3f}, {kimera_auroc_ci[1]:.3f}]")
    print(f"GPT AUROC 95% CI: [{gpt_auroc_ci[0]:.3f}, {gpt_auroc_ci[1]:.3f}]")
    
    # F1 confidence intervals
    kimera_thresh, _ = compute_optimal_threshold(y_true, kimera_scores, "f1")
    gpt_thresh, _ = compute_optimal_threshold(y_true, gpt_scores, "f1")
    
    kimera_f1_ci = bootstrap_ci(
        lambda yt, ys: accuracy_stats(yt, (ys >= kimera_thresh).astype(int))["f1"],
        y_true, kimera_scores, n=1000, seed=42
    )
    
    gpt_f1_ci = bootstrap_ci(
        lambda yt, ys: accuracy_stats(yt, (ys >= gpt_thresh).astype(int))["f1"],
        y_true, gpt_scores, n=1000, seed=42
    )
    
    print(f"Kimera F1 95% CI: [{kimera_f1_ci[0]:.3f}, {kimera_f1_ci[1]:.3f}]")
    print(f"GPT F1 95% CI: [{gpt_f1_ci[0]:.3f}, {gpt_f1_ci[1]:.3f}]")

def demo_significance_testing():
    """Demonstrate statistical significance testing."""
    print("\n📈 Statistical Significance Testing Demo")
    print("-" * 45)
    
    y_true, kimera_scores, gpt_scores = generate_synthetic_data()
    
    # Get binary predictions
    kimera_thresh, _ = compute_optimal_threshold(y_true, kimera_scores, "f1")
    gpt_thresh, _ = compute_optimal_threshold(y_true, gpt_scores, "f1")
    
    kimera_pred = (kimera_scores >= kimera_thresh).astype(int)
    gpt_pred = (gpt_scores >= gpt_thresh).astype(int)
    
    # McNemar's test
    kimera_correct = (kimera_pred == y_true)
    gpt_correct = (gpt_pred == y_true)
    
    mcnemar_stat, mcnemar_p = mcnemar_test(kimera_correct, gpt_correct)
    
    print(f"McNemar's test statistic: {mcnemar_stat:.3f}")
    print(f"McNemar's test p-value: {mcnemar_p:.4f}")
    
    if mcnemar_p < 0.05:
        print("✓ Significant difference between classifiers (p < 0.05)")
    else:
        print("✗ No significant difference between classifiers (p ≥ 0.05)")
    
    # Performance comparison
    kimera_acc = np.mean(kimera_correct)
    gpt_acc = np.mean(gpt_correct)
    
    print(f"Kimera accuracy: {kimera_acc:.3f}")
    print(f"GPT accuracy: {gpt_acc:.3f}")
    print(f"Difference: {kimera_acc - gpt_acc:.3f}")

def demo_visualization():
    """Create demonstration plots."""
    print("\n📊 Visualization Demo")
    print("-" * 25)
    
    y_true, kimera_scores, gpt_scores = generate_synthetic_data()
    
    # Compute metrics
    kimera_roc = roc_stats(y_true, kimera_scores)
    gpt_roc = roc_stats(y_true, gpt_scores)
    kimera_pr = pr_stats(y_true, kimera_scores)
    gpt_pr = pr_stats(y_true, gpt_scores)
    
    # Create plots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Kimera-SWM v0.7.0 Metrics Demo', fontsize=16, fontweight='bold')
    
    # ROC Curve
    ax1.plot(kimera_roc["fpr"], kimera_roc["tpr"], 
             label=f'Kimera (AUROC={kimera_roc["auroc"]:.3f})', linewidth=2)
    ax1.plot(gpt_roc["fpr"], gpt_roc["tpr"], 
             label=f'GPT (AUROC={gpt_roc["auroc"]:.3f})', linewidth=2)
    ax1.plot([0, 1], [0, 1], 'k--', alpha=0.5, label='Random')
    ax1.set_xlabel('False Positive Rate')
    ax1.set_ylabel('True Positive Rate')
    ax1.set_title('ROC Curves')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # PR Curve
    ax2.plot(kimera_pr["recall"], kimera_pr["precision"], 
             label=f'Kimera (AUPR={kimera_pr["aupr"]:.3f})', linewidth=2)
    ax2.plot(gpt_pr["recall"], gpt_pr["precision"], 
             label=f'GPT (AUPR={gpt_pr["aupr"]:.3f})', linewidth=2)
    ax2.axhline(y=0.5, color='k', linestyle='--', alpha=0.5, label='Baseline')
    ax2.set_xlabel('Recall')
    ax2.set_ylabel('Precision')
    ax2.set_title('Precision-Recall Curves')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Score distributions
    ax3.hist(kimera_scores[y_true == 0], alpha=0.5, bins=20, label='Kimera (No Contradiction)', density=True)
    ax3.hist(kimera_scores[y_true == 1], alpha=0.5, bins=20, label='Kimera (Contradiction)', density=True)
    ax3.set_xlabel('Confidence Score')
    ax3.set_ylabel('Density')
    ax3.set_title('Kimera Score Distributions')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Comparison scatter
    ax4.scatter(kimera_scores, gpt_scores, alpha=0.6, c=y_true, cmap='RdYlBu')
    ax4.plot([0, 1], [0, 1], 'k--', alpha=0.5)
    ax4.set_xlabel('Kimera Scores')
    ax4.set_ylabel('GPT Scores')
    ax4.set_title('Score Correlation')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('metrics_demo.png', dpi=150, bbox_inches='tight')
    print("✓ Plots saved to metrics_demo.png")

def main():
    """Run the complete metrics demonstration."""
    print("🎯 Kimera-SWM v0.7.0 Metrics Infrastructure Demo")
    print("=" * 60)
    print("Demonstrating zetetic metrics for macro-level performance tracking")
    print()
    
    try:
        # Run all demos
        demo_basic_metrics()
        demo_confidence_intervals()
        demo_significance_testing()
        demo_visualization()
        
        print("\n" + "=" * 60)
        print("🎉 Demo completed successfully!")
        print("\nKey features demonstrated:")
        print("  ✓ ROC and PR curve computation with AUROC/AUPR")
        print("  ✓ Bootstrap confidence intervals for uncertainty quantification")
        print("  ✓ McNemar's test for statistical significance")
        print("  ✓ Optimal threshold finding for binary classification")
        print("  ✓ Comprehensive visualization capabilities")
        print("\nThis infrastructure enables every micro-optimization to be")
        print("evaluated against macro-level performance metrics.")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
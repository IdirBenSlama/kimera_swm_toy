"""CLI wrapper: computes Kimera + GPT stats, YAML + plots.

This module provides a command-line interface for computing comprehensive
metrics on benchmark results and generating visualizations.

Usage:
    poetry run python -m benchmarks.metric_runner results.csv
    poetry run python -m benchmarks.metric_runner results.csv --out metrics.yaml
"""
import argparse
import yaml
import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend

from kimera.metrics import (
    roc_stats, pr_stats, accuracy_stats, bootstrap_ci, 
    mcnemar_test, compute_optimal_threshold
)


def load_benchmark_results(csv_path: Path) -> pd.DataFrame:
    """Load benchmark results CSV with error handling."""
    try:
        df = pd.read_csv(csv_path)
        required_cols = ['label']
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        return df
    except Exception as e:
        raise ValueError(f"Failed to load {csv_path}: {e}")


def compute_model_metrics(y_true: np.ndarray, y_score: np.ndarray, 
                         model_name: str) -> Dict[str, Any]:
    """Compute comprehensive metrics for a single model."""
    metrics = {}
    
    # ROC and PR curves
    metrics.update(roc_stats(y_true, y_score))
    metrics.update(pr_stats(y_true, y_score))
    
    # Optimal threshold and binary metrics
    opt_thresh, opt_f1 = compute_optimal_threshold(y_true, y_score, "f1")
    y_pred = (y_score >= opt_thresh).astype(int)
    metrics.update(accuracy_stats(y_true, y_pred))
    metrics["optimal_threshold"] = opt_thresh
    
    # Bootstrap confidence intervals
    auroc_ci = bootstrap_ci(
        lambda yt, ys: roc_stats(yt, ys)["auroc"], 
        y_true, y_score, n=1000
    )
    f1_ci = bootstrap_ci(
        lambda yt, ys: accuracy_stats(yt, (ys >= opt_thresh).astype(int))["f1"],
        y_true, y_score, n=1000
    )
    
    metrics["auroc_ci"] = {"lower": auroc_ci[0], "upper": auroc_ci[1]}
    metrics["f1_ci"] = {"lower": f1_ci[0], "upper": f1_ci[1]}
    
    return metrics


def compute_significance_tests(df: pd.DataFrame) -> Dict[str, Any]:
    """Compute statistical significance tests between models."""
    significance = {}
    
    if "kimera_conf" in df.columns and "gpt_conf" in df.columns:
        y_true = df["label"].values
        kimera_scores = df["kimera_conf"].values
        gpt_scores = df["gpt_conf"].values
        
        # Find optimal thresholds for both models
        kimera_thresh, _ = compute_optimal_threshold(y_true, kimera_scores, "f1")
        gpt_thresh, _ = compute_optimal_threshold(y_true, gpt_scores, "f1")
        
        # Binary predictions
        kimera_pred = (kimera_scores >= kimera_thresh).astype(int)
        gpt_pred = (gpt_scores >= gpt_thresh).astype(int)
        
        # McNemar's test
        kimera_correct = (kimera_pred == y_true)
        gpt_correct = (gpt_pred == y_true)
        
        mcnemar_stat, mcnemar_p = mcnemar_test(kimera_correct, gpt_correct)
        
        significance["mcnemar"] = {
            "statistic": mcnemar_stat,
            "p_value": mcnemar_p,
            "significant": mcnemar_p < 0.05
        }
        
        # Performance difference
        kimera_acc = np.mean(kimera_correct)
        gpt_acc = np.mean(gpt_correct)
        
        significance["accuracy_difference"] = {
            "kimera": kimera_acc,
            "gpt": gpt_acc,
            "difference": kimera_acc - gpt_acc
        }
    
    return significance


def create_plots(results: Dict[str, Any], output_dir: Path):
    """Create ROC and PR curve plots."""
    
    # ROC Curve
    plt.figure(figsize=(10, 5))
    
    plt.subplot(1, 2, 1)
    for model_name, metrics in results.items():
        if model_name in ["kimera", "gpt"] and "fpr" in metrics:
            fpr = metrics["fpr"]
            tpr = metrics["tpr"]
            auroc = metrics["auroc"]
            plt.plot(fpr, tpr, label=f'{model_name.upper()} (AUROC={auroc:.3f})')
    
    plt.plot([0, 1], [0, 1], 'k--', alpha=0.5, label='Random')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curves')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # PR Curve
    plt.subplot(1, 2, 2)
    for model_name, metrics in results.items():
        if model_name in ["kimera", "gpt"] and "precision" in metrics:
            precision = metrics["precision"]
            recall = metrics["recall"]
            aupr = metrics["aupr"]
            plt.plot(recall, precision, label=f'{model_name.upper()} (AUPR={aupr:.3f})')
    
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curves')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / "metrics_plots.png", dpi=150, bbox_inches='tight')
    plt.close()


def generate_summary_report(results: Dict[str, Any], output_dir: Path):
    """Generate a human-readable summary report."""
    report_lines = []
    report_lines.append("# Kimera-SWM Metrics Report")
    report_lines.append("=" * 50)
    report_lines.append("")
    
    for model_name, metrics in results.items():
        if model_name in ["kimera", "gpt"]:
            report_lines.append(f"## {model_name.upper()} Performance")
            report_lines.append(f"- AUROC: {metrics.get('auroc', 'N/A'):.3f}")
            if 'auroc_ci' in metrics:
                ci = metrics['auroc_ci']
                report_lines.append(f"  - 95% CI: [{ci['lower']:.3f}, {ci['upper']:.3f}]")
            
            report_lines.append(f"- AUPR: {metrics.get('aupr', 'N/A'):.3f}")
            report_lines.append(f"- Accuracy: {metrics.get('accuracy', 'N/A'):.3f}")
            report_lines.append(f"- F1 Score: {metrics.get('f1', 'N/A'):.3f}")
            if 'f1_ci' in metrics:
                ci = metrics['f1_ci']
                report_lines.append(f"  - 95% CI: [{ci['lower']:.3f}, {ci['upper']:.3f}]")
            
            report_lines.append(f"- Precision: {metrics.get('precision', 'N/A'):.3f}")
            report_lines.append(f"- Recall: {metrics.get('recall', 'N/A'):.3f}")
            report_lines.append(f"- Optimal Threshold: {metrics.get('optimal_threshold', 'N/A'):.3f}")
            report_lines.append("")
    
    if "significance" in results:
        sig = results["significance"]
        report_lines.append("## Statistical Significance")
        if "mcnemar" in sig:
            mcnemar = sig["mcnemar"]
            report_lines.append(f"- McNemar's Test: p = {mcnemar['p_value']:.4f}")
            report_lines.append(f"  - Significant difference: {mcnemar['significant']}")
        
        if "accuracy_difference" in sig:
            acc_diff = sig["accuracy_difference"]
            report_lines.append(f"- Accuracy Difference: {acc_diff['difference']:.3f}")
            report_lines.append(f"  - Kimera: {acc_diff['kimera']:.3f}")
            report_lines.append(f"  - GPT: {acc_diff['gpt']:.3f}")
    
    with open(output_dir / "summary_report.md", "w") as f:
        f.write("\n".join(report_lines))


def main():
    parser = argparse.ArgumentParser(description="Compute metrics and generate plots for benchmark results")
    parser.add_argument("csv", help="Path to benchmark results CSV file")
    parser.add_argument("--out", help="Output directory (default: same as CSV)")
    parser.add_argument("--no-plots", action="store_true", help="Skip plot generation")
    parser.add_argument("--no-report", action="store_true", help="Skip summary report")
    
    args = parser.parse_args()
    
    csv_path = Path(args.csv)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    # Determine output directory
    if args.out:
        output_dir = Path(args.out)
    else:
        output_dir = csv_path.parent
    
    output_dir.mkdir(exist_ok=True)
    
    # Load data
    print(f"Loading benchmark results from {csv_path}")
    df = load_benchmark_results(csv_path)
    print(f"Loaded {len(df)} samples")
    
    # Compute metrics
    results = {}
    y_true = df["label"].values
    
    # Kimera metrics
    if "kimera_conf" in df.columns:
        print("Computing Kimera metrics...")
        kimera_scores = df["kimera_conf"].values
        results["kimera"] = compute_model_metrics(y_true, kimera_scores, "kimera")
    
    # GPT metrics
    if "gpt_conf" in df.columns:
        print("Computing GPT metrics...")
        gpt_scores = df["gpt_conf"].values
        results["gpt"] = compute_model_metrics(y_true, gpt_scores, "gpt")
    
    # Significance tests
    if len(results) > 1:
        print("Computing significance tests...")
        results["significance"] = compute_significance_tests(df)
    
    # Save metrics as YAML
    yaml_path = output_dir / "metrics.yaml"
    print(f"Saving metrics to {yaml_path}")
    with open(yaml_path, "w") as f:
        yaml.safe_dump(results, f, default_flow_style=False, sort_keys=False)
    
    # Generate plots
    if not args.no_plots and len(results) > 0:
        print("Generating plots...")
        create_plots(results, output_dir)
        print(f"Plots saved to {output_dir / 'metrics_plots.png'}")
    
    # Generate summary report
    if not args.no_report:
        print("Generating summary report...")
        generate_summary_report(results, output_dir)
        print(f"Summary report saved to {output_dir / 'summary_report.md'}")
    
    print("Metrics computation complete!")


if __name__ == "__main__":
    main()
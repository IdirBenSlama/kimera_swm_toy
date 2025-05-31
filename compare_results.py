#!/usr/bin/env python3
"""
Compare baseline vs negation fix results
"""
import yaml
import pandas as pd
from pathlib import Path

def load_metrics(filename):
    """Load metrics from YAML file"""
    try:
        with open(filename, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Warning: {filename} not found")
        return None

def compare_metrics():
    """Compare metrics between baseline and negation fix"""
    print("Comparing baseline vs negation fix results...")
    print("=" * 50)
    
    # Load baseline metrics (if they exist)
    baseline_metrics = None
    if Path("metrics_baseline.yaml").exists():
        baseline_metrics = load_metrics("metrics_baseline.yaml")
    
    # Load current metrics (should be from negation fix run)
    current_metrics = load_metrics("metrics.yaml")
    
    if current_metrics is None:
        print("No current metrics found. Run the benchmark first.")
        return
    
    # Display current metrics
    print("Current Metrics (with negation fix):")
    kimera_metrics = current_metrics.get('kimera', {})
    for metric, value in kimera_metrics.items():
        if isinstance(value, (int, float)):
            print(f"  {metric}: {value:.4f}")
    
    print()
    
    # If we have baseline, compare
    if baseline_metrics:
        print("Comparison (Negation Fix vs Baseline):")
        baseline_kimera = baseline_metrics.get('kimera', {})
        current_kimera = current_metrics.get('kimera', {})
        
        for metric in ['auroc', 'aupr', 'f1', 'precision', 'recall']:
            if metric in baseline_kimera and metric in current_kimera:
                baseline_val = baseline_kimera[metric]
                current_val = current_kimera[metric]
                delta = current_val - baseline_val
                direction = "↑" if delta > 0 else "↓" if delta < 0 else "="
                print(f"  {metric}: {baseline_val:.4f} → {current_val:.4f} ({direction}{abs(delta):.4f})")
    else:
        print("No baseline metrics found for comparison.")
        print("To create baseline, run benchmark and save metrics.yaml as metrics_baseline.yaml")

def analyze_predictions():
    """Analyze prediction differences"""
    print("\nAnalyzing prediction files...")
    
    files_to_check = ["mixed5k_baseline.csv", "mixed5k_negfix.csv"]
    existing_files = [f for f in files_to_check if Path(f).exists()]
    
    if len(existing_files) == 2:
        print("Both prediction files found - detailed comparison possible")
        
        # Load both files
        baseline_df = pd.read_csv("mixed5k_baseline.csv")
        negfix_df = pd.read_csv("mixed5k_negfix.csv")
        
        # Find differences
        if len(baseline_df) == len(negfix_df):
            # Compare predictions
            baseline_preds = baseline_df['kimera_prediction'].astype(bool)
            negfix_preds = negfix_df['kimera_prediction'].astype(bool)
            
            differences = baseline_preds != negfix_preds
            num_differences = differences.sum()
            
            print(f"  Total pairs: {len(baseline_df)}")
            print(f"  Prediction differences: {num_differences}")
            print(f"  Percentage changed: {100 * num_differences / len(baseline_df):.2f}%")
            
            if num_differences > 0:
                print("\nSample of changed predictions:")
                changed_indices = differences[differences].index[:5]
                for idx in changed_indices:
                    text1 = baseline_df.loc[idx, 'text1']
                    text2 = baseline_df.loc[idx, 'text2']
                    baseline_pred = baseline_df.loc[idx, 'kimera_prediction']
                    negfix_pred = negfix_df.loc[idx, 'kimera_prediction']
                    print(f"  '{text1}' vs '{text2}'")
                    print(f"    Baseline: {baseline_pred} → Negfix: {negfix_pred}")
        else:
            print("  Warning: Files have different lengths")
    else:
        print(f"  Found files: {existing_files}")
        print("  Need both baseline and negfix files for comparison")

if __name__ == "__main__":
    compare_metrics()
    analyze_predictions()
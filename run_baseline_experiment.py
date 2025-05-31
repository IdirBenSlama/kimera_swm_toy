#!/usr/bin/env python3
"""
Run the 0→1 experiment checklist to validate negation fix
"""
import subprocess
import sys
import time
import os
from pathlib import Path

def run_command(cmd, description, env_vars=None):
    """Run a command and handle output"""
    print(f"\n🔄 {description}")
    print(f"Command: {cmd}")
    if env_vars:
        print(f"Environment: {env_vars}")
    print("-" * 50)
    
    # Set up environment
    env = os.environ.copy()
    if env_vars:
        env.update(env_vars)
    
    start_time = time.time()
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env)
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ Success ({elapsed:.1f}s)")
            if result.stdout:
                # Show last few lines of output
                lines = result.stdout.strip().split('\n')
                for line in lines[-5:]:
                    print(f"  {line}")
        else:
            print(f"❌ Failed ({elapsed:.1f}s)")
            print("Error:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False
    
    return True

def main():
    """Run the complete 0→1 experiment"""
    print("🧪 Kimera 0→1 Experiment: Negation Fix Validation")
    print("=" * 60)
    
    # Check if data file exists
    data_file = "data/mixed_contradictions.csv"
    if not Path(data_file).exists():
        print(f"❌ Data file not found: {data_file}")
        return
    
    print(f"✅ Data file found: {data_file}")
    
    # Step 1: Run baseline (disable negation fix)
    print("\n📊 Step 1: Running baseline benchmark (negation fix OFF)")
    baseline_cmd = f"poetry run python -m benchmarks.llm_compare {data_file} --stats --kimera-only --outfile baseline.csv --no-emoji"
    baseline_env = {"KIMERA_NEGATION_FIX": "0"}
    
    if not run_command(baseline_cmd, "Baseline benchmark", baseline_env):
        print("❌ Baseline failed - stopping experiment")
        return
    
    # Step 2: Run with negation fix (enable negation fix)
    print("\n🔧 Step 2: Running with negation fix (negation fix ON)")
    negfix_cmd = f"poetry run python -m benchmarks.llm_compare {data_file} --stats --kimera-only --outfile neg_fix.csv --no-emoji"
    negfix_env = {"KIMERA_NEGATION_FIX": "1"}
    
    if not run_command(negfix_cmd, "Negation fix benchmark", negfix_env):
        print("❌ Negation fix benchmark failed - stopping experiment")
        return
    
    # Step 3: Compare results
    print("\n📈 Step 3: Comparing results")
    compare_cmd = "python compare_results.py baseline.csv neg_fix.csv"
    
    if not run_command(compare_cmd, "Results comparison"):
        print("❌ Comparison failed")
        return
    
    print("\n🎉 Experiment complete!")
    print("\nNext steps:")
    print("1. Check if AUROC/F1 confidence intervals overlap")
    print("2. If no overlap → significant improvement! 🎯")
    print("3. Use explorer.html to analyze disagreement patterns")
    print("4. Identify next error bucket for improvement")
    
    # Quick file check
    if Path("baseline.csv").exists() and Path("neg_fix.csv").exists():
        print(f"\n📁 Output files created:")
        print(f"  - baseline.csv ({Path('baseline.csv').stat().st_size} bytes)")
        print(f"  - neg_fix.csv ({Path('neg_fix.csv').stat().st_size} bytes)")

if __name__ == "__main__":
    main()
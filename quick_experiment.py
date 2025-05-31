#!/usr/bin/env python3
"""
Quick experiment to test negation fix impact
"""
import os
import sys
import subprocess
from pathlib import Path

def run_quick_test():
    """Run a quick test on a small subset"""
    print("🧪 Quick Negation Fix Test")
    print("=" * 30)
    
    # Use the smaller dataset for quick testing
    data_file = "data/mixed_quick.csv"
    if not Path(data_file).exists():
        data_file = "data/toy_contradictions.csv"
    
    if not Path(data_file).exists():
        print("❌ No test data found")
        return
    
    print(f"📊 Using dataset: {data_file}")
    
    # Test 1: Baseline (negation fix OFF)
    print("\n🔄 Running baseline (negation fix OFF)...")
    env_baseline = os.environ.copy()
    env_baseline["KIMERA_NEGATION_FIX"] = "0"
    
    cmd_baseline = f"python -m benchmarks.llm_compare {data_file} --kimera-only --outfile quick_baseline.csv --no-emoji"
    
    try:
        result1 = subprocess.run(cmd_baseline, shell=True, env=env_baseline, 
                               capture_output=True, text=True, cwd=".")
        if result1.returncode == 0:
            print("✅ Baseline complete")
        else:
            print(f"❌ Baseline failed: {result1.stderr}")
            return
    except Exception as e:
        print(f"❌ Baseline error: {e}")
        return
    
    # Test 2: With negation fix (negation fix ON)
    print("\n🔄 Running with negation fix (negation fix ON)...")
    env_negfix = os.environ.copy()
    env_negfix["KIMERA_NEGATION_FIX"] = "1"
    
    cmd_negfix = f"python -m benchmarks.llm_compare {data_file} --kimera-only --outfile quick_negfix.csv --no-emoji"
    
    try:
        result2 = subprocess.run(cmd_negfix, shell=True, env=env_negfix,
                               capture_output=True, text=True, cwd=".")
        if result2.returncode == 0:
            print("✅ Negation fix complete")
        else:
            print(f"❌ Negation fix failed: {result2.stderr}")
            return
    except Exception as e:
        print(f"❌ Negation fix error: {e}")
        return
    
    # Compare results
    print("\n📈 Comparing results...")
    if Path("compare_results.py").exists():
        try:
            result3 = subprocess.run("python compare_results.py quick_baseline.csv quick_negfix.csv",
                                   shell=True, capture_output=True, text=True)
            if result3.returncode == 0:
                print("✅ Comparison complete")
                print(result3.stdout)
            else:
                print(f"❌ Comparison failed: {result3.stderr}")
        except Exception as e:
            print(f"❌ Comparison error: {e}")
    
    # Show file sizes as basic check
    files = ["quick_baseline.csv", "quick_negfix.csv"]
    for f in files:
        if Path(f).exists():
            size = Path(f).stat().st_size
            print(f"📁 {f}: {size} bytes")

if __name__ == "__main__":
    run_quick_test()
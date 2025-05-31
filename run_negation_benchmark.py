#!/usr/bin/env python3
"""
Run the benchmark with negation fix
"""
import subprocess
import sys
import os
from pathlib import Path

def run_benchmark():
    """Run the mixed contradictions benchmark with negation fix"""
    print("Running benchmark with negation fix...")
    
    # Ensure we're using the right encoding
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    cmd = [
        sys.executable, "-m", "benchmarks.llm_compare",
        "data/mixed_contradictions.csv",
        "--stats", "--no-cache", "--kimera-only", 
        "--outfile", "mixed5k_negfix.csv", "--no-emoji"
    ]
    
    try:
        print(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, env=env, timeout=300)  # 5 minute timeout
        
        if result.returncode == 0:
            print("✓ Negation fix benchmark completed successfully")
            
            # Check if output files exist
            if Path("mixed5k_negfix.csv").exists():
                print("✓ Results saved to mixed5k_negfix.csv")
            if Path("metrics.yaml").exists():
                print("✓ Metrics saved to metrics.yaml")
                
        else:
            print(f"✗ Benchmark failed with return code {result.returncode}")
            
    except subprocess.TimeoutExpired:
        print("✗ Benchmark timed out after 5 minutes")
    except Exception as e:
        print(f"✗ Error running benchmark: {e}")

if __name__ == "__main__":
    run_benchmark()
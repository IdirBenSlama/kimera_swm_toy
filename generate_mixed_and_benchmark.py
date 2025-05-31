#!/usr/bin/env python3
"""
Quick script to generate mixed dataset and run initial benchmark
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors gracefully."""
    print(f"\n🔄 {description}")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print("Output:", result.stdout[-500:])  # Last 500 chars
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print("Error:", e.stderr)
        return False

def main():
    print("🚀 Generating mixed dataset and running benchmark...")
    
    # Step 1: Generate mixed dataset
    if not run_command([
        "poetry", "run", "python", "scripts/build_mixed_dataset.py",
        "--rows", "1000",  # Start smaller for testing
        "--ratio", "0.5",
        "--out", "data/mixed_1k.csv"
    ], "Generating mixed dataset (1000 pairs)"):
        return
    
    # Step 2: Run benchmark on mixed dataset
    if not run_command([
        "poetry", "run", "python", "-m", "benchmarks.llm_compare",
        "data/mixed_1k.csv",
        "--max-pairs", "100",  # Subset for quick test
        "--stats",
        "--outfile", "mixed_benchmark_results.csv"
    ], "Running benchmark on mixed dataset"):
        return
    
    print("\n🎉 All steps completed successfully!")
    print("\nNext steps:")
    print("1. Check mixed_benchmark_results.csv")
    print("2. Open tools/explorer.html and load the results")
    print("3. Filter to 'disagreements' to see where Kimera fails")
    print("4. Start tagging error patterns!")

if __name__ == "__main__":
    main()
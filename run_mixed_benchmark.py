#!/usr/bin/env python3
"""
Run benchmark on the mixed contradictions dataset
"""
import subprocess
import sys
from pathlib import Path

def main():
    print("🚀 Running benchmark on mixed dataset...")
    
    # Check if dataset exists
    dataset_path = Path("data/mixed_contradictions.csv")
    if not dataset_path.exists():
        print(f"❌ Dataset not found: {dataset_path}")
        print("Available datasets in data/:")
        data_dir = Path("data")
        if data_dir.exists():
            for csv_file in data_dir.glob("*.csv"):
                print(f"  - {csv_file}")
        return
    
    # Run benchmark with emoji-safe mode
    cmd = [
        sys.executable, "-m", "benchmarks.llm_compare",
        str(dataset_path),
        "--max-pairs", "100",  # Start with subset for speed
        "--stats",
        "--kimera-only",
        "--no-emoji",  # Windows-safe
        "--outfile", "mixed_benchmark_results.csv"
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n✅ Benchmark completed successfully!")
        
        # Check outputs
        results_file = Path("mixed_benchmark_results.csv")
        metrics_file = Path("metrics.yaml")
        
        if results_file.exists():
            print(f"📊 Results saved to: {results_file}")
            # Quick peek at results
            with open(results_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                print(f"   Contains {len(lines)-1} result rows")
        
        if metrics_file.exists():
            print(f"📈 Metrics saved to: {metrics_file}")
            # Show key metrics
            with open(metrics_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if "auroc:" in content:
                    for line in content.split('\n'):
                        if 'auroc:' in line or 'f1:' in line or 'accuracy:' in line:
                            print(f"   {line.strip()}")
        
        print("\n🎯 Next steps:")
        print("1. Open tools/explorer.html in your browser")
        print("2. Load mixed_benchmark_results.csv")
        print("3. Click 'Only disagreements' to see where Kimera fails")
        print("4. Start tagging error patterns!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Benchmark failed with return code {e.returncode}")
        print("Try running with --no-cache if there are caching issues")

if __name__ == "__main__":
    main()
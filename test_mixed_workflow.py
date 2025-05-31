#!/usr/bin/env python3
"""
Test the complete mixed dataset workflow
"""
import subprocess
import sys
from pathlib import Path

def main():
    print("🚀 Testing mixed dataset workflow...")
    
    # Step 1: Create quick mixed dataset
    print("\n📊 Creating mixed dataset...")
    try:
        import quick_mixed_test
        dataset_path = quick_mixed_test.create_quick_mixed_dataset()
        print(f"✅ Dataset created: {dataset_path}")
    except Exception as e:
        print(f"❌ Failed to create dataset: {e}")
        return
    
    # Step 2: Run benchmark
    print("\n🔬 Running benchmark...")
    try:
        cmd = [
            sys.executable, "-m", "benchmarks.llm_compare",
            str(dataset_path),
            "--max-pairs", "20",
            "--stats",
            "--outfile", "mixed_test_results.csv"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ Benchmark completed successfully")
        print("Output:", result.stdout[-300:] if result.stdout else "No output")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Benchmark failed: {e}")
        print("Error:", e.stderr)
        return
    
    # Step 3: Check results
    results_file = Path("mixed_test_results.csv")
    if results_file.exists():
        print(f"\n📈 Results saved to: {results_file}")
        
        # Quick peek at results
        with open(results_file, 'r') as f:
            lines = f.readlines()
            print(f"Results contain {len(lines)-1} rows")
            if len(lines) > 1:
                print("Sample row:", lines[1][:100] + "..." if len(lines[1]) > 100 else lines[1])
    
    # Step 4: Check metrics
    metrics_file = Path("metrics.yaml")
    if metrics_file.exists():
        print(f"\n📊 Metrics saved to: {metrics_file}")
        with open(metrics_file, 'r') as f:
            content = f.read()
            print("Metrics preview:")
            print(content[:300] + "..." if len(content) > 300 else content)
    
    print("\n🎉 Mixed dataset workflow test completed!")
    print("\nNext steps:")
    print("1. Open tools/explorer.html")
    print("2. Load mixed_test_results.csv")
    print("3. Filter to disagreements")
    print("4. Start error analysis!")

if __name__ == "__main__":
    main()
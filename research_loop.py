#!/usr/bin/env python3
"""
Complete research loop: baseline → negation fix → comparison
"""
import subprocess
import sys
import os
import shutil
from pathlib import Path
import time

def run_command(cmd, description, timeout=300):
    """Run a command with proper error handling"""
    print(f"\n{description}...")
    print(f"Command: {' '.join(cmd)}")
    
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    try:
        start_time = time.time()
        result = subprocess.run(cmd, env=env, timeout=timeout)
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✓ {description} completed successfully ({elapsed:.1f}s)")
            return True
        else:
            print(f"✗ {description} failed with return code {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"✗ {description} timed out after {timeout}s")
        return False
    except Exception as e:
        print(f"✗ Error in {description}: {e}")
        return False

def backup_file(src, dst):
    """Backup a file if it exists"""
    if Path(src).exists():
        shutil.copy2(src, dst)
        print(f"✓ Backed up {src} to {dst}")
        return True
    return False

def main():
    """Run the complete research loop"""
    print("🚀 Starting Kimera Research Loop")
    print("=" * 50)
    
    # Step 1: Test the negation fix implementation
    print("\n📋 Step 1: Testing negation fix implementation")
    success = run_command([sys.executable, "test_negation_fix.py"], 
                         "Testing negation detection", timeout=30)
    if not success:
        print("❌ Negation fix test failed. Aborting.")
        return
    
    # Step 2: Run baseline benchmark (temporarily disable negation fix)
    print("\n📊 Step 2: Running baseline benchmark")
    
    # First, let's create a version without negation fix for baseline
    print("Creating baseline version (without negation fix)...")
    
    # Backup current resonance.py
    backup_file("src/kimera/resonance.py", "src/kimera/resonance_with_negfix.py")
    
    # Create baseline version (comment out negation fix)
    with open("src/kimera/resonance.py", "r") as f:
        content = f.read()
    
    # Comment out negation fix lines
    baseline_content = content.replace(
        "    # Apply negation mismatch penalty\n    if negation_mismatch(a.raw, b.raw):\n        score -= 0.25          # push them further apart\n        score = max(-1.0, score)",
        "    # Apply negation mismatch penalty (DISABLED FOR BASELINE)\n    # if negation_mismatch(a.raw, b.raw):\n    #     score -= 0.25          # push them further apart\n    #     score = max(-1.0, score)"
    )
    
    with open("src/kimera/resonance.py", "w") as f:
        f.write(baseline_content)
    
    # Run baseline benchmark
    cmd_baseline = [
        sys.executable, "-m", "benchmarks.llm_compare",
        "data/mixed_contradictions.csv",
        "--stats", "--no-cache", "--kimera-only", 
        "--outfile", "mixed5k_baseline.csv", "--no-emoji"
    ]
    
    success = run_command(cmd_baseline, "Running baseline benchmark", timeout=600)
    if success:
        backup_file("metrics.yaml", "metrics_baseline.yaml")
        backup_file("metrics_plots.png", "metrics_baseline_plots.png")
    
    # Step 3: Restore negation fix and run improved benchmark
    print("\n🔧 Step 3: Running benchmark with negation fix")
    
    # Restore the negation fix version
    if Path("src/kimera/resonance_with_negfix.py").exists():
        shutil.copy2("src/kimera/resonance_with_negfix.py", "src/kimera/resonance.py")
        print("✓ Restored negation fix version")
    
    cmd_negfix = [
        sys.executable, "-m", "benchmarks.llm_compare",
        "data/mixed_contradictions.csv",
        "--stats", "--no-cache", "--kimera-only", 
        "--outfile", "mixed5k_negfix.csv", "--no-emoji"
    ]
    
    success = run_command(cmd_negfix, "Running negation fix benchmark", timeout=600)
    if success:
        backup_file("metrics.yaml", "metrics_negfix.yaml")
        backup_file("metrics_plots.png", "metrics_negfix_plots.png")
    
    # Step 4: Compare results
    print("\n📈 Step 4: Comparing results")
    success = run_command([sys.executable, "compare_results.py"], 
                         "Comparing baseline vs negation fix", timeout=30)
    
    # Step 5: Summary
    print("\n📋 Research Loop Summary")
    print("=" * 30)
    
    files_created = []
    for filename in ["mixed5k_baseline.csv", "mixed5k_negfix.csv", 
                    "metrics_baseline.yaml", "metrics_negfix.yaml"]:
        if Path(filename).exists():
            files_created.append(filename)
    
    print(f"✓ Files created: {', '.join(files_created)}")
    
    if Path("tools/explorer.html").exists():
        print("\n🔍 Next steps:")
        print("1. Open tools/explorer.html in your browser")
        print("2. Load mixed5k_baseline.csv and mixed5k_negfix.csv")
        print("3. Click 'Only disagreements' to analyze error patterns")
        print("4. Tag 30-50 rows to identify next improvement areas")
    
    print("\n🎉 Research loop completed!")

if __name__ == "__main__":
    main()
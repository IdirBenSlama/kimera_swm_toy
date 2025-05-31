#!/usr/bin/env python3
"""
Quick validation checklist to confirm all-green status.
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description, timeout=120):
    """Run a command and report results."""
    print(f"\n{'='*50}")
    print(f"RUNNING: {description}")
    print(f"Command: {' '.join(cmd)}")
    print('='*50)
    
    try:
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=timeout,
            cwd=Path.cwd()
        )
        
        if result.returncode == 0:
            print(f"✅ SUCCESS: {description}")
            if result.stdout.strip():
                print("Output:")
                print(result.stdout[-500:])  # Last 500 chars
        else:
            print(f"❌ FAILED: {description} (exit code: {result.returncode})")
            print("STDOUT:", result.stdout[-300:])
            print("STDERR:", result.stderr[-300:])
            
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print(f"⏰ TIMEOUT: {description}")
        return False
    except Exception as e:
        print(f"💥 ERROR: {description} - {e}")
        return False

def main():
    """Run the validation checklist."""
    print("🚀 KIMERA-SWM VALIDATION CHECKLIST")
    print("Verifying all-green status after bootstrap_ci fix...")
    
    results = []
    
    # 1. Check Poetry lock/install
    results.append(run_command(
        ["poetry", "check"], 
        "Poetry configuration check"
    ))
    
    # 2. Run unit tests
    results.append(run_command(
        ["poetry", "run", "pytest", "tests/", "-v", "--tb=short", "-x"], 
        "Unit test suite",
        timeout=180
    ))
    
    # 3. Run validation script
    results.append(run_command(
        [sys.executable, "validate_all_green.py"], 
        "All-green validation script"
    ))
    
    # 4. Quick metrics test
    results.append(run_command(
        [sys.executable, "quick_test_validation.py"], 
        "Bootstrap CI fix verification"
    ))
    
    # Summary
    print(f"\n{'='*60}")
    print("VALIDATION SUMMARY")
    print('='*60)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 ALL CHECKS PASSED ({passed}/{total})")
        print("✅ Kimera-SWM is ALL-GREEN!")
        print("\nNext steps:")
        print("- Run benchmark: poetry run python -m benchmarks.llm_compare data/toy_contradictions.csv --max-pairs 20 --stats --kimera-only")
        print("- Open tools/explorer.html to analyze results")
    else:
        print(f"⚠️  SOME CHECKS FAILED ({passed}/{total})")
        print("Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
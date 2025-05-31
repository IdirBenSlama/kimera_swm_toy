#!/usr/bin/env python3
"""
Run all metrics-related tests to validate the v0.7.0 implementation.
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and report results."""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
            return True
        else:
            print(f"❌ {description} - FAILED (exit code: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def main():
    """Run all metrics tests."""
    print("🚀 Kimera-SWM v0.7.0 Metrics Test Suite")
    print("Testing the new zetetic metrics infrastructure...")
    
    tests = [
        (
            [sys.executable, "-m", "pytest", "tests/test_metrics.py", "-v"],
            "Unit tests for metrics module"
        ),
        (
            [sys.executable, "test_metrics_integration.py"],
            "Integration test for metrics pipeline"
        ),
        (
            [sys.executable, "-c", "from kimera.metrics import roc_stats; print('✓ Metrics module imports successfully')"],
            "Import test for metrics module"
        ),
    ]
    
    results = []
    for cmd, description in tests:
        success = run_command(cmd, description)
        results.append((description, success))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {description}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Metrics infrastructure is ready.")
        print("\nNext steps:")
        print("  1. Run: poetry run python -m benchmarks.llm_compare data/toy_contradictions.csv --stats")
        print("  2. Check generated metrics.yaml and metrics_plots.png")
        print("  3. Use --stats flag in all future benchmarks")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix before proceeding.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
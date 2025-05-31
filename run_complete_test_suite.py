#!/usr/bin/env python3
"""
Complete test suite for Kimera v0.7.x stabilization
"""
import subprocess
import sys
import os
import time
from datetime import datetime

def run_test_safe(cmd, description, timeout=120):
    """Safely run a test command"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    print(f"Command: {cmd}")
    print(f"Timeout: {timeout}s")
    print()
    
    start_time = time.time()
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        elapsed = time.time() - start_time
        
        success = result.returncode == 0
        status = "✅ PASSED" if success else "❌ FAILED"
        
        print(f"Status: {status}")
        print(f"Duration: {elapsed:.2f}s")
        print(f"Exit code: {result.returncode}")
        
        # Show output (truncated if too long)
        if result.stdout:
            lines = result.stdout.strip().split('\n')
            if len(lines) <= 15:
                print(f"\nOutput:\n{result.stdout}")
            else:
                print(f"\nOutput (first 15 lines):")
                for line in lines[:15]:
                    print(line)
                print(f"... ({len(lines)-15} more lines)")
        
        if result.stderr and not success:
            stderr_lines = result.stderr.strip().split('\n')
            if len(stderr_lines) <= 10:
                print(f"\nErrors:\n{result.stderr}")
            else:
                print(f"\nErrors (first 10 lines):")
                for line in stderr_lines[:10]:
                    print(line)
                print(f"... ({len(stderr_lines)-10} more lines)")
        
        return success, elapsed, result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start_time
        print(f"❌ TIMEOUT after {elapsed:.2f}s")
        return False, elapsed, "", "Timeout"
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ ERROR: {e}")
        return False, elapsed, "", str(e)

def check_critical_files():
    """Check that all critical files exist"""
    print(f"\n{'='*60}")
    print("📁 CRITICAL FILES CHECK")
    print(f"{'='*60}")
    
    critical_files = [
        "conftest.py",
        "src/kimera/__init__.py",
        "src/kimera/storage.py",
        "src/kimera/echoform.py",
        "src/kimera/reactor_mp.py",
        "src/kimera/cls.py",
        "tests/test_echoform_core.py",
        "tests/test_cls_integration.py",
        "tests/test_storage_metrics.py",
        "pyproject.toml",
    ]
    
    files_found = 0
    for filepath in critical_files:
        exists = os.path.exists(filepath)
        status = "✅" if exists else "❌"
        print(f"{status} {filepath}")
        if exists:
            files_found += 1
    
    print(f"\nFiles status: {files_found}/{len(critical_files)} critical files present")
    return files_found, len(critical_files)

def main():
    """Run complete test suite"""
    start_time = datetime.now()
    
    print("🚀 KIMERA v0.7.x COMPLETE TEST SUITE")
    print("=" * 60)
    print(f"Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Check critical files
    files_found, total_files = check_critical_files()
    
    # Define test suite
    test_suite = [
        # Quick validation tests
        ("python check_stabilization.py", "Basic Stabilization Check", 30),
        ("python test_quick_fixes.py", "Quick Fixes Validation", 60),
        ("python simple_test_runner.py", "Simple Test Runner", 30),
        
        # Core functionality tests
        ("python quick_test_phase193.py", "Phase 19.3 Tests", 60),
        ("python test_basic_functionality.py", "Basic Functionality", 60),
        
        # Pytest tests
        ("python -m pytest tests/test_echoform_core.py -v", "Core EchoForm Tests", 120),
        ("python -m pytest tests/test_cls_integration.py -v", "CLS Integration Tests", 120),
        ("python -m pytest tests/test_storage_metrics.py -v", "Storage Metrics Tests", 120),
        
        # Comprehensive validation
        ("python validate_all_fixes.py", "All Fixes Validation", 90),
        ("python run_focus_tests.py", "Focus Tests", 120),
    ]
    
    # Run tests
    print(f"\n{'='*60}")
    print("🧪 RUNNING TEST SUITE")
    print(f"{'='*60}")
    
    results = []
    total_duration = 0
    
    for cmd, description, timeout in test_suite:
        success, duration, stdout, stderr = run_test_safe(cmd, description, timeout)
        results.append((description, success, duration))
        total_duration += duration
    
    # Generate summary
    end_time = datetime.now()
    
    print(f"\n{'='*60}")
    print("📊 COMPLETE TEST SUMMARY")
    print(f"{'='*60}")
    
    print(f"\n⏱️  Timing:")
    print(f"   Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Ended: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Total Duration: {total_duration:.2f}s ({total_duration/60:.1f} minutes)")
    
    print(f"\n📁 Files:")
    print(f"   Critical Files: {files_found}/{total_files} ({files_found/total_files*100:.1f}%)")
    
    print(f"\n🧪 Tests:")
    passed_tests = 0
    for description, success, duration in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} {description} ({duration:.1f}s)")
        if success:
            passed_tests += 1
    
    total_tests = len(results)
    test_percentage = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\n📈 Overall Results:")
    print(f"   Files: {files_found}/{total_files} ({files_found/total_files*100:.1f}%)")
    print(f"   Tests: {passed_tests}/{total_tests} ({test_percentage:.1f}%)")
    
    # Determine final status
    files_ok = files_found >= total_files * 0.9
    tests_ok = passed_tests >= total_tests * 0.8
    
    if files_ok and tests_ok:
        print(f"\n🎉 STABILIZATION SUCCESSFUL!")
        print(f"   Kimera v0.7.x is stable and ready for use")
        print(f"   {test_percentage:.1f}% of tests passing")
        final_status = "SUCCESS"
    elif tests_ok:
        print(f"\n⚠️  MOSTLY SUCCESSFUL")
        print(f"   Core functionality works but some issues remain")
        print(f"   {test_percentage:.1f}% of tests passing")
        final_status = "PARTIAL"
    else:
        print(f"\n💥 STABILIZATION INCOMPLETE")
        print(f"   Significant issues remain")
        print(f"   Only {test_percentage:.1f}% of tests passing")
        final_status = "FAILED"
    
    # Write summary to file
    summary_file = "COMPLETE_TEST_RESULTS.md"
    with open(summary_file, 'w') as f:
        f.write(f"# Kimera v0.7.x Complete Test Results\n\n")
        f.write(f"**Status**: {final_status}\n")
        f.write(f"**Date**: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Duration**: {total_duration:.2f}s\n\n")
        f.write(f"## Summary\n")
        f.write(f"- Files: {files_found}/{total_files} ({files_found/total_files*100:.1f}%)\n")
        f.write(f"- Tests: {passed_tests}/{total_tests} ({test_percentage:.1f}%)\n\n")
        f.write(f"## Test Results\n")
        for description, success, duration in results:
            status = "✅ PASS" if success else "❌ FAIL"
            f.write(f"- {status} {description} ({duration:.1f}s)\n")
    
    print(f"\n📄 Results written to: {summary_file}")
    
    return final_status == "SUCCESS"

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
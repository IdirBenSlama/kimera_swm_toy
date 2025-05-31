#!/usr/bin/env python3
"""
Final test status check for v0.7.x stabilization
"""
import subprocess
import sys
import os
import time

def run_command_safe(cmd, description, timeout=60):
    """Safely run a command and return results"""
    print(f"\n{'='*50}")
    print(f"🧪 {description}")
    print(f"{'='*50}")
    
    start_time = time.time()
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        elapsed = time.time() - start_time
        
        success = result.returncode == 0
        status = "✅ PASS" if success else "❌ FAIL"
        
        print(f"Command: {cmd}")
        print(f"Status: {status}")
        print(f"Duration: {elapsed:.2f}s")
        print(f"Exit code: {result.returncode}")
        
        if result.stdout:
            # Show first few lines of output
            lines = result.stdout.strip().split('\n')
            if len(lines) <= 10:
                print(f"\nOutput:\n{result.stdout}")
            else:
                print(f"\nOutput (first 10 lines):")
                for line in lines[:10]:
                    print(line)
                print(f"... ({len(lines)-10} more lines)")
        
        if result.stderr and not success:
            print(f"\nErrors:\n{result.stderr}")
        
        return success, result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        print(f"❌ TIMEOUT ({timeout}s)")
        return False, "", "Timeout"
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False, "", str(e)

def check_file_exists(filepath):
    """Check if a file exists and show its status"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    print(f"{status} {filepath}")
    return exists

def main():
    """Run comprehensive status check"""
    print("🚀 Kimera v0.7.x Stabilization Status Check")
    print("=" * 60)
    
    # Check critical files exist
    print("\n📁 Critical Files Check:")
    critical_files = [
        "conftest.py",
        "src/kimera/storage.py", 
        "src/kimera/echoform.py",
        "src/kimera/reactor_mp.py",
        "tests/test_echoform_core.py",
        "tests/test_cls_integration.py",
    ]
    
    files_ok = 0
    for filepath in critical_files:
        if check_file_exists(filepath):
            files_ok += 1
    
    print(f"\nFiles status: {files_ok}/{len(critical_files)} critical files present")
    
    # Run key tests
    print("\n🧪 Running Key Tests:")
    
    test_commands = [
        ("python simple_test_runner.py", "Simple Fix Validation", 30),
        ("python test_quick_fixes.py", "Quick Fixes Test", 30),
        ("python -m pytest tests/test_echoform_core.py -v", "Core EchoForm Tests", 60),
        ("python quick_test_phase193.py", "Phase 19.3 Test", 30),
    ]
    
    test_results = []
    
    for cmd, desc, timeout in test_commands:
        success, stdout, stderr = run_command_safe(cmd, desc, timeout)
        test_results.append((desc, success))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 FINAL STATUS SUMMARY")
    print(f"{'='*60}")
    
    print(f"\n📁 Files: {files_ok}/{len(critical_files)} critical files present")
    
    print(f"\n🧪 Tests:")
    passed_tests = 0
    for desc, success in test_results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} {desc}")
        if success:
            passed_tests += 1
    
    total_tests = len(test_results)
    test_percentage = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\n📈 Overall Status:")
    print(f"   Files: {files_ok}/{len(critical_files)} ({files_ok/len(critical_files)*100:.1f}%)")
    print(f"   Tests: {passed_tests}/{total_tests} ({test_percentage:.1f}%)")
    
    # Determine overall status
    if files_ok == len(critical_files) and passed_tests >= total_tests * 0.8:
        print(f"\n🎉 STABILIZATION SUCCESS!")
        print(f"   v0.7.x appears to be stable with {test_percentage:.1f}% tests passing")
        overall_success = True
    elif passed_tests >= total_tests * 0.6:
        print(f"\n⚠️  PARTIAL SUCCESS")
        print(f"   Most functionality works but some issues remain")
        overall_success = True
    else:
        print(f"\n💥 STABILIZATION INCOMPLETE")
        print(f"   Significant issues remain to be resolved")
        overall_success = False
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
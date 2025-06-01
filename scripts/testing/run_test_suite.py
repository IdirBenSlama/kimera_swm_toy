#!/usr/bin/env python3
"""
Run the complete test suite
"""
import subprocess
import sys
import os

def run_test_suite():
    """Run the complete test suite"""
    print("🧪 RUNNING COMPLETE TEST SUITE")
    print("=" * 35)
    
    test_categories = [
        ("Unit Tests", "tests/unit/"),
        ("Integration Tests", "tests/integration/"),
        ("Archive Tests", "tests/archive/")
    ]
    
    results = []
    
    for category, path in test_categories:
        if os.path.exists(path):
            print(f"\n🔍 Running {category}...")
            
            # Count test files
            test_files = [f for f in os.listdir(path) if f.startswith('test_') and f.endswith('.py')]
            print(f"  Found {len(test_files)} test files")
            
            if test_files:
                try:
                    # Run pytest on the directory
                    result = subprocess.run([
                        sys.executable, '-m', 'pytest', path, '-v'
                    ], capture_output=True, text=True, timeout=120)
                    
                    if result.returncode == 0:
                        print(f"  ✅ {category} PASSED")
                        results.append((category, "PASSED", len(test_files)))
                    else:
                        print(f"  ❌ {category} FAILED")
                        print(f"  Error: {result.stderr[:200]}...")
                        results.append((category, "FAILED", len(test_files)))
                        
                except subprocess.TimeoutExpired:
                    print(f"  ⏰ {category} TIMEOUT")
                    results.append((category, "TIMEOUT", len(test_files)))
                except Exception as e:
                    print(f"  ❌ {category} ERROR: {e}")
                    results.append((category, "ERROR", len(test_files)))
            else:
                print(f"  ⚠️ No test files found")
                results.append((category, "NO_TESTS", 0))
        else:
            print(f"  ⚠️ {path} not found")
            results.append((category, "NOT_FOUND", 0))
    
    # Run individual test files in root if any
    root_tests = [f for f in os.listdir('.') if f.startswith('test_') and f.endswith('.py')]
    if root_tests:
        print(f"\n🔍 Running Root Tests...")
        print(f"  Found {len(root_tests)} test files")
        
        passed_root = 0
        for test_file in root_tests:
            try:
                result = subprocess.run([
                    sys.executable, test_file
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    print(f"  ✅ {test_file}")
                    passed_root += 1
                else:
                    print(f"  ❌ {test_file}")
            except Exception as e:
                print(f"  ❌ {test_file}: {e}")
        
        results.append(("Root Tests", "MIXED" if passed_root > 0 else "FAILED", len(root_tests)))
    
    # Summary
    total_tests = sum(count for _, _, count in results)
    passed_categories = sum(1 for _, status, _ in results if status == "PASSED")
    total_categories = len([r for r in results if r[1] != "NOT_FOUND"])
    
    print(f"\n📊 TEST SUITE SUMMARY:")
    print(f"  Total test files: {total_tests}")
    print(f"  Categories passed: {passed_categories}/{total_categories}")
    print(f"  Success rate: {(passed_categories/total_categories*100) if total_categories > 0 else 0:.1f}%")
    
    for category, status, count in results:
        if status != "NOT_FOUND":
            emoji = {"PASSED": "✅", "FAILED": "❌", "ERROR": "💥", "TIMEOUT": "⏰", "NO_TESTS": "⚠️", "MIXED": "🔶"}.get(status, "❓")
            print(f"  {emoji} {category}: {status} ({count} tests)")
    
    return passed_categories == total_categories if total_categories > 0 else False

if __name__ == "__main__":
    success = run_test_suite()
    sys.exit(0 if success else 1)
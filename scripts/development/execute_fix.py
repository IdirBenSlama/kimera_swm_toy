#!/usr/bin/env python3
"""
Execute system fixes
"""
import subprocess
import sys

def execute_fix():
    """Execute comprehensive system fixes"""
    print("🔧 EXECUTING SYSTEM FIXES")
    print("=" * 40)
    
    fixes = [
        ("Unicode Fix", "fix_unicode_encoding.py"),
        ("Import Fix", "fix_import_paths.py"), 
        ("Critical Issues", "fix_critical_issues.py")
    ]
    
    results = []
    for name, script in fixes:
        if os.path.exists(script):
            print(f"🔧 Running {name}...")
            try:
                result = subprocess.run([sys.executable, script], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ {name} completed successfully")
                    results.append((name, "SUCCESS"))
                else:
                    print(f"❌ {name} failed: {result.stderr}")
                    results.append((name, "FAILED"))
            except Exception as e:
                print(f"❌ {name} error: {e}")
                results.append((name, "ERROR"))
        else:
            print(f"⚠️ {script} not found")
            results.append((name, "NOT_FOUND"))
    
    print(f"\n📊 Fix Results:")
    for name, status in results:
        print(f"  {name}: {status}")
    
    return results

if __name__ == "__main__":
    import os
    execute_fix()
#!/usr/bin/env python3
"""
Run the complete reorganization process
"""
import subprocess
import sys
import os

def run_complete_reorganization():
    """Execute the complete reorganization"""
    print("🗂️ STARTING COMPLETE REORGANIZATION")
    print("=" * 50)
    
    # Run the main reorganization script
    if os.path.exists("execute_complete_reorganization.py"):
        print("🚀 Running complete reorganization...")
        try:
            result = subprocess.run([sys.executable, "execute_complete_reorganization.py"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Complete reorganization successful!")
                print(result.stdout)
            else:
                print("❌ Reorganization failed:")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ Error running reorganization: {e}")
            return False
    else:
        print("❌ execute_complete_reorganization.py not found")
        return False
    
    # Run verification
    if os.path.exists("verify_traceability_reorganization.py"):
        print("\n🔍 Running verification...")
        try:
            result = subprocess.run([sys.executable, "verify_traceability_reorganization.py"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Verification successful!")
                print(result.stdout)
            else:
                print("⚠️ Verification issues:")
                print(result.stderr)
                
        except Exception as e:
            print(f"⚠️ Error running verification: {e}")
    
    print("\n🎉 REORGANIZATION PROCESS COMPLETE!")
    return True

if __name__ == "__main__":
    success = run_complete_reorganization()
    sys.exit(0 if success else 1)
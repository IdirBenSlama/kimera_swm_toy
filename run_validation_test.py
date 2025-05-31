#!/usr/bin/env python3
"""
Execute validation and show results
"""
import subprocess
import sys
import os

def main():
    print("🔍 Executing Kimera 0.7.x Validation...")
    print("=" * 60)
    
    # Set environment
    env = os.environ.copy()
    env['KIMERA_DB_PATH'] = 'test_validation.db'
    
    # Clean up any existing test database
    if os.path.exists('test_validation.db'):
        os.remove('test_validation.db')
    
    try:
        # Run validation
        result = subprocess.run([sys.executable, "validate_all_fixes.py"], 
                              capture_output=True, text=True, timeout=120, env=env)
        
        print("VALIDATION OUTPUT:")
        print("-" * 40)
        print(result.stdout)
        
        if result.stderr:
            print("\nERRORS/WARNINGS:")
            print("-" * 40)
            print(result.stderr)
        
        print(f"\nExit Code: {result.returncode}")
        
        if result.returncode == 0:
            print("\n🎉 VALIDATION SUCCESSFUL!")
            print("All Kimera 0.7.x fixes are working correctly.")
        else:
            print("\n❌ VALIDATION FAILED!")
            print("Some fixes may need additional work.")
            
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ Validation timed out")
        return False
    except Exception as e:
        print(f"❌ Error running validation: {e}")
        return False
    finally:
        # Clean up test database
        if os.path.exists('test_validation.db'):
            try:
                os.remove('test_validation.db')
            except:
                pass

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
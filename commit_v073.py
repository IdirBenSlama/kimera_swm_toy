#!/usr/bin/env python3
"""
Commit script for Kimera v0.7.3 - CLS lattice write + decay weighting
"""
import subprocess
import sys

def safe_print(message):
    """Safe print function that handles Unicode issues on Windows"""
    try:
        print(message)
    except UnicodeEncodeError:
        # Fallback: replace problematic characters
        safe_message = message.encode('ascii', 'replace').decode('ascii')
        print(safe_message)

def run_command(cmd, description):
    """Run a command and handle errors"""
    safe_print(f"Running: {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout.strip():
            safe_print(f"   {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        safe_print(f"ERROR: {description} failed:")
        safe_print(f"   {e.stderr.strip()}")
        return False

def main():
    """Commit v0.7.3 changes"""
    safe_print("Kimera v0.7.3 Commit Process")
    safe_print("CLS Lattice Write + Time-Decay Weighting")
    safe_print("=" * 45)
    
    # Run tests first
    safe_print("\nRunning tests before commit...")
    if not run_command("python quick_test_phase192.py", "Quick Phase 19.2 tests"):
        safe_print("ERROR: Tests failed - aborting commit")
        return False
    
    # Git operations
    commands = [
        ("git add .", "Adding all changes"),
        ('git commit -m "v0.7.3: CLS lattice write + decay weighting\n\n• CLS lattice forms now stored and tracked in memory\n• cls_event terms append on every resonance call\n• Time-decay weighting with τ = 14 days in intensity_sum()\n• Updated tests for storage and time-decay functionality\n• Added docs/echoform_params.md for parameter documentation\n• Phase 19.2 complete - EchoForms now active in CLS lattice"', "Committing v0.7.3"),
        ("git tag v0.7.3", "Creating v0.7.3 tag"),
    ]
    
    for cmd, desc in commands:
        if not run_command(cmd, desc):
            safe_print(f"ERROR: Failed at: {desc}")
            return False
    
    safe_print("\nv0.7.3 committed successfully!")
    safe_print("\nReady to push:")
    safe_print("   git push")
    safe_print("   git push --tags")
    safe_print("\nv0.7.3 Summary:")
    safe_print("   • CLS lattice forms stored with cls_event tracking")
    safe_print("   • Time-decay weighting (τ = 14 days)")
    safe_print("   • Enhanced parameter documentation")
    safe_print("   • All tests green")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
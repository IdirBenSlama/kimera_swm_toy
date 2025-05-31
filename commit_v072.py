#!/usr/bin/env python3
"""
Commit and tag v0.7.2 with EchoForm core + explorer fix
"""
import subprocess
import sys

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} failed")
            print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"💥 {description} error: {e}")
        return False

def main():
    """Commit and tag the release"""
    print("🚀 Committing v0.7.2: EchoForm core + explorer fix")
    print("=" * 50)
    
    commands = [
        ("git add .", "Adding all changes"),
        ('git commit -m "v0.7.2: EchoForm core + explorer encoding fix"', "Committing changes"),
        ("git tag v0.7.2", "Creating tag v0.7.2")
    ]
    
    success_count = 0
    for cmd, desc in commands:
        if run_command(cmd, desc):
            success_count += 1
        else:
            break
    
    print(f"\n📊 Results: {success_count}/{len(commands)} operations completed")
    
    if success_count == len(commands):
        print("\n🎉 v0.7.2 successfully committed and tagged!")
        print("\nNext steps:")
        print("1. git push --tags (to push tags to remote)")
        print("2. Proceed to Phase 19.2 implementation")
        return True
    else:
        print("\n❌ Some operations failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
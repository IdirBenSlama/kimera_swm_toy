#!/usr/bin/env python3
"""
Commit script for v0.7.4 - Phase 19.3 Persistent Storage
"""
import subprocess
import sys


def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return None


def main():
    print("🚀 Committing Phase 19.3: Persistent Lattice Storage")
    print("=" * 55)
    
    # Check git status
    status = run_command("git status --porcelain", "Checking git status")
    if status is None:
        return False
    
    if not status.strip():
        print("No changes to commit")
        return True
    
    print("Changes to commit:")
    print(status)
    
    # Add all changes
    if not run_command("git add .", "Adding all changes"):
        return False
    
    # Commit with detailed message
    commit_message = """Phase 19.3: Persistent lattice storage with DuckDB

✨ New Features:
- DuckDB-based persistent storage for EchoForms
- CLI interface for lattice management
- Time-decay functionality with configurable τ
- Migration script for smooth transition

🔧 Technical Changes:
- Added src/kimera/storage.py with LatticeStorage class
- Updated src/kimera/cls.py to use persistent backend
- Added src/kimera/__main__.py for CLI commands
- Created scripts/migrate_lattice_to_db.py
- Added .github/workflows/ci.yml for automated testing

📊 Storage Features:
- JSON blob storage with metadata indexing
- Time-based queries and pruning
- Domain filtering and form counting
- Exponential time-decay (τ = 14 days default)

🧪 Testing:
- Comprehensive storage layer tests
- Updated CLS integration tests
- CLI command testing
- Migration script validation

🎯 Benefits:
- Process-persistent lattice forms
- Developer-friendly debugging tools
- Foundation for multi-process scaling
- Zero breaking changes from v0.7.3

Ready for Phase 19.4: Cross-form resonance and topology updates"""
    
    if not run_command(f'git commit -m "{commit_message}"', "Committing changes"):
        return False
    
    # Update version in pyproject.toml
    if not run_command('sed -i \'s/version = "0.7.0"/version = "0.7.4"/\' pyproject.toml', "Updating version"):
        # Try Windows version
        run_command('powershell -Command "(Get-Content pyproject.toml) -replace \'version = \\"0.7.0\\"\', \'version = \\"0.7.4\\"\' | Set-Content pyproject.toml"', "Updating version (Windows)")
    
    # Create tag
    if not run_command("git tag -a v0.7.4 -m 'Phase 19.3: Persistent lattice storage'", "Creating tag"):
        return False
    
    print("\n🎉 Phase 19.3 committed successfully!")
    print("📋 Summary:")
    print("  • Persistent DuckDB storage implemented")
    print("  • CLI management interface added")
    print("  • Time-decay and pruning functionality")
    print("  • Comprehensive test coverage")
    print("  • CI/CD pipeline with benchmarks")
    print("  • Zero breaking changes")
    
    print("\n🚀 Next steps:")
    print("  • git push origin main")
    print("  • git push origin v0.7.4")
    print("  • python quick_test_phase193.py")
    print("  • python -m kimera lattice list")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
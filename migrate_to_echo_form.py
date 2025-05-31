#!/usr/bin/env python3
"""
Migration script for echo-form implementation (v0.7.1)
"""
import sys
import os
from pathlib import Path

def clear_old_cache():
    """Clear the old cache to force regeneration with new echo-based keys"""
    print("🧹 Clearing old embedding cache...")
    
    cache_dir = Path(os.getenv("KIMERA_CACHE_DIR", ".cache"))
    
    if cache_dir.exists():
        cache_files = list(cache_dir.glob("*.pkl"))
        if cache_files:
            print(f"  Found {len(cache_files)} cache files to clear")
            for cache_file in cache_files:
                try:
                    cache_file.unlink()
                    print(f"  ✅ Removed {cache_file.name}")
                except Exception as e:
                    print(f"  ⚠️  Could not remove {cache_file.name}: {e}")
        else:
            print("  No cache files found")
    else:
        print("  Cache directory doesn't exist")

def test_echo_form():
    """Test the new echo-form implementation"""
    print("\n🧪 Testing echo-form implementation...")
    
    sys.path.insert(0, 'src')
    
    try:
        from kimera.geoid import init_geoid
        
        # Test basic functionality
        g1 = init_geoid(text="  Hello world  ", lang="en", tags=["test"])
        g2 = init_geoid(text="Hello world", lang="en", tags=["test"])
        
        print(f"  Raw 1: '{g1.raw}' -> Echo: '{g1.echo}' -> GID: {g1.gid}")
        print(f"  Raw 2: '{g2.raw}' -> Echo: '{g2.echo}' -> GID: {g2.gid}")
        
        # Verify echo trimming
        assert g1.echo == "Hello world", f"Expected 'Hello world', got '{g1.echo}'"
        assert g2.echo == "Hello world", f"Expected 'Hello world', got '{g2.echo}'"
        
        # Verify stable hashing
        assert g1.gid == g2.gid, f"Expected same GID, got {g1.gid} != {g2.gid}"
        
        # Verify deterministic hashing
        g3 = init_geoid(text="Hello world", lang="en", tags=["test"])
        assert g2.gid == g3.gid, f"Expected deterministic GID, got {g2.gid} != {g3.gid}"
        
        print("  ✅ Echo-form implementation working correctly!")
        return True
        
    except Exception as e:
        print(f"  ❌ Echo-form test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_basic_tests():
    """Run basic functionality tests"""
    print("\n🔧 Running basic functionality tests...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, "test_echo_form.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("  ✅ All echo-form tests passed!")
            return True
        else:
            print(f"  ❌ Tests failed:")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"  ❌ Could not run tests: {e}")
        return False

def main():
    """Run the migration to echo-form"""
    print("🚀 Kimera Echo-Form Migration (v0.7.1)")
    print("=" * 40)
    
    # Step 1: Clear old cache
    clear_old_cache()
    
    # Step 2: Test new implementation
    if not test_echo_form():
        print("\n❌ Migration failed - echo-form not working")
        return False
    
    # Step 3: Run comprehensive tests
    if not run_basic_tests():
        print("\n⚠️  Migration completed but some tests failed")
        return False
    
    print("\n🎉 Migration to echo-form completed successfully!")
    print("\n✨ Benefits now active:")
    print("  • Stable, deterministic geoid hashes")
    print("  • Whitespace-insensitive deduplication") 
    print("  • Enhanced observability in explorer")
    print("  • Improved cache efficiency")
    
    print("\n📋 Next steps:")
    print("  1. Run negation experiment: python test_fixes.py")
    print("  2. Execute full benchmark: poetry run python -m benchmarks.llm_compare")
    print("  3. Open tools/explorer.html to see echo columns")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
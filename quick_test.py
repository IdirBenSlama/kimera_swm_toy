#!/usr/bin/env python3
"""Quick test of basic functionality."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all imports work."""
    print("Testing imports...")
    
    try:
        from kimera.cache import embed_cache, resonance_cache, get_cache_stats, clear_embedding_cache
        print("✅ Cache imports work")
    except Exception as e:
        print(f"❌ Cache import failed: {e}")
        return False
    
    try:
        from kimera.geoid import init_geoid, sem_encoder, sym_encoder
        print("✅ Geoid imports work")
    except Exception as e:
        print(f"❌ Geoid import failed: {e}")
        return False
    
    try:
        import kimera
        print("✅ Main kimera import works")
    except Exception as e:
        print(f"❌ Main kimera import failed: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality."""
    print("\nTesting basic functionality...")
    
    try:
        from kimera import init_geoid, get_cache_stats, clear_embedding_cache
        
        # Clear cache
        clear_embedding_cache()
        
        # Create a geoid
        geoid = init_geoid("Hello world", "en", ["test"])
        print(f"✅ Created geoid: {geoid.gid[:8]}...")
        
        # Check cache stats
        stats = get_cache_stats()
        print(f"✅ Cache stats: {stats['embedding_cache_size']} embeddings")
        
        return True
    except Exception as e:
        print(f"❌ Basic functionality failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run quick tests."""
    print("🧪 Running quick tests...")
    
    if not test_imports():
        return 1
    
    if not test_basic_functionality():
        return 1
    
    print("\n🎉 All quick tests passed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
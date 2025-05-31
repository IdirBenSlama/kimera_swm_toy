#!/usr/bin/env python3
"""
Soak test for lattice storage system
Generates 100k random GeoID pairs and tests lattice_resolve performance
"""
import sys
import time
import random
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from kimera.geoid import init_geoid
from kimera.cls import lattice_resolve, clear_stored_forms
from kimera.storage import get_storage, close_storage


def monkey_patch_encoders():
    """Monkey patch sentence transformers to return zero vectors for speed"""
    try:
        from sentence_transformers import SentenceTransformer
        
        # Create a mock encode method that returns zero vectors
        def mock_encode(self, sentences, **kwargs):
            if isinstance(sentences, str):
                sentences = [sentences]
            # Return zero vectors of appropriate dimension (384 is common)
            import numpy as np
            return np.zeros((len(sentences), 384), dtype=np.float32)
        
        # Patch the encode method
        SentenceTransformer.encode = mock_encode
        print("[PATCH] Sentence transformer encode method patched for speed")
        return True
        
    except ImportError:
        print("[PATCH] sentence-transformers not available, skipping patch")
        return False


def generate_random_text_pairs(n_pairs):
    """Generate n random text pairs for testing"""
    print(f"[GEN] Generating {n_pairs:,} random text pairs...")
    
    # Word lists for generating random sentences
    subjects = ["cats", "dogs", "birds", "fish", "trees", "flowers", "cars", "books", "computers", "phones"]
    verbs = ["run", "jump", "fly", "swim", "grow", "bloom", "drive", "read", "compute", "ring"]
    objects = ["quickly", "slowly", "beautifully", "loudly", "quietly", "brightly", "darkly", "smoothly", "roughly", "gently"]
    
    pairs = []
    for i in range(n_pairs):
        # Generate two related but different sentences
        subj1, subj2 = random.sample(subjects, 2)
        verb1, verb2 = random.sample(verbs, 2)
        obj1, obj2 = random.sample(objects, 2)
        
        text1 = f"{subj1.title()} {verb1} {obj1}"
        text2 = f"{subj2.title()} {verb2} {obj2}"
        
        pairs.append((text1, text2))
        
        if (i + 1) % 10000 == 0:
            print(f"[GEN] Generated {i + 1:,} pairs...")
    
    print(f"[GEN] Generated {len(pairs):,} text pairs")
    return pairs


def setup_soak_storage():
    """Setup storage for soak testing"""
    # Use a dedicated soak test database
    soak_db = "soak_test_lattice.db"
    
    # Remove existing database
    if os.path.exists(soak_db):
        os.remove(soak_db)
        print(f"[SETUP] Removed existing {soak_db}")
    
    # Initialize fresh storage
    storage = get_storage(soak_db)
    clear_stored_forms()
    print(f"[SETUP] Initialized fresh storage: {soak_db}")
    
    return storage, soak_db


def run_soak_test(n_pairs=100000, dry_run=False):
    """Run the soak test"""
    print(f"🔥 Lattice Storage Soak Test")
    print(f"Target: {n_pairs:,} GeoID pairs")
    print(f"Mode: {'DRY RUN' if dry_run else 'FULL TEST'}")
    print("=" * 50)
    
    # Monkey patch for speed
    monkey_patch_encoders()
    
    # Adjust for dry run
    if dry_run:
        n_pairs = min(n_pairs, 500)
        print(f"[DRY RUN] Reduced to {n_pairs} pairs")
    
    # Setup storage
    storage, soak_db = setup_soak_storage()
    
    try:
        # Generate test data
        start_gen = time.perf_counter()
        pairs = generate_random_text_pairs(n_pairs)
        gen_time = time.perf_counter() - start_gen
        print(f"[TIMING] Text generation: {gen_time:.2f}s")
        
        # Convert to GeoIDs
        print(f"[GEOID] Converting {len(pairs):,} pairs to GeoIDs...")
        start_geoid = time.perf_counter()
        geoid_pairs = []
        
        for i, (text1, text2) in enumerate(pairs):
            geo1 = init_geoid(text1, "en", ["soak_test"])
            geo2 = init_geoid(text2, "en", ["soak_test"])
            geoid_pairs.append((geo1, geo2))
            
            if (i + 1) % 5000 == 0:
                print(f"[GEOID] Processed {i + 1:,} pairs...")
        
        geoid_time = time.perf_counter() - start_geoid
        print(f"[TIMING] GeoID creation: {geoid_time:.2f}s ({geoid_time/len(pairs)*1000:.1f}ms per pair)")
        
        # First lattice resolve pass
        print(f"[RESOLVE] First pass: {len(geoid_pairs):,} lattice_resolve calls...")
        start_resolve1 = time.perf_counter()
        
        for i, (geo1, geo2) in enumerate(geoid_pairs):
            intensity = lattice_resolve(geo1, geo2)
            
            if (i + 1) % 10000 == 0:
                print(f"[RESOLVE] First pass: {i + 1:,} calls completed...")
        
        resolve1_time = time.perf_counter() - start_resolve1
        qps1 = len(geoid_pairs) / resolve1_time
        print(f"[TIMING] First resolve pass: {resolve1_time:.2f}s ({qps1:.1f} QPS)")
        
        # Second lattice resolve pass (should hit existing forms)
        print(f"[RESOLVE] Second pass: {len(geoid_pairs):,} lattice_resolve calls...")
        start_resolve2 = time.perf_counter()
        
        for i, (geo1, geo2) in enumerate(geoid_pairs):
            intensity = lattice_resolve(geo1, geo2)
            
            if (i + 1) % 10000 == 0:
                print(f"[RESOLVE] Second pass: {i + 1:,} calls completed...")
        
        resolve2_time = time.perf_counter() - start_resolve2
        qps2 = len(geoid_pairs) / resolve2_time
        print(f"[TIMING] Second resolve pass: {resolve2_time:.2f}s ({qps2:.1f} QPS)")
        
        # Get final database size
        db_size = os.path.getsize(soak_db) if os.path.exists(soak_db) else 0
        db_size_mb = db_size / (1024 * 1024)
        
        # Calculate total time and overall QPS
        total_time = gen_time + geoid_time + resolve1_time + resolve2_time
        total_operations = len(pairs) * 4  # text gen + geoid + 2 resolves
        overall_qps = total_operations / total_time
        
        # Print summary
        print("\n" + "=" * 50)
        print("🎯 SOAK TEST RESULTS")
        print("=" * 50)
        print(f"Text pairs processed:     {len(pairs):,}")
        print(f"Total operations:         {total_operations:,}")
        print(f"Total time:               {total_time:.2f}s")
        print(f"Overall throughput:       {overall_qps:.1f} ops/sec")
        print()
        print("PHASE BREAKDOWN:")
        print(f"  Text generation:        {gen_time:.2f}s")
        print(f"  GeoID creation:         {geoid_time:.2f}s ({geoid_time/len(pairs)*1000:.1f}ms/pair)")
        print(f"  First resolve pass:     {resolve1_time:.2f}s ({qps1:.1f} QPS)")
        print(f"  Second resolve pass:    {resolve2_time:.2f}s ({qps2:.1f} QPS)")
        print()
        print(f"Final database size:      {db_size_mb:.2f} MB")
        print(f"Storage efficiency:       {db_size/len(pairs):.1f} bytes/pair")
        
        # Performance assessment
        print("\nPERFORMANCE ASSESSMENT:")
        if qps1 > 100:
            print("✅ First pass QPS: EXCELLENT")
        elif qps1 > 50:
            print("✅ First pass QPS: GOOD")
        elif qps1 > 10:
            print("⚠️  First pass QPS: ACCEPTABLE")
        else:
            print("❌ First pass QPS: POOR")
        
        if qps2 > qps1 * 1.5:
            print("✅ Second pass speedup: EXCELLENT (good caching)")
        elif qps2 > qps1:
            print("✅ Second pass speedup: GOOD")
        else:
            print("⚠️  Second pass speedup: MINIMAL")
        
        if db_size_mb < 100:
            print("✅ Database size: REASONABLE")
        elif db_size_mb < 500:
            print("⚠️  Database size: LARGE")
        else:
            print("❌ Database size: EXCESSIVE")
        
        return True
        
    except Exception as e:
        print(f"❌ Soak test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Cleanup
        close_storage()
        print(f"\n[CLEANUP] Storage closed")
        
        if not dry_run:
            # Keep the database for inspection
            print(f"[INFO] Database preserved: {soak_db}")
        else:
            # Remove test database in dry run
            if os.path.exists(soak_db):
                os.remove(soak_db)
                print(f"[CLEANUP] Removed test database: {soak_db}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Lattice storage soak test")
    parser.add_argument("--pairs", type=int, default=100000, 
                       help="Number of text pairs to test (default: 100000)")
    parser.add_argument("--dry-run", action="store_true",
                       help="Run with reduced dataset for testing (500 pairs)")
    
    args = parser.parse_args()
    
    success = run_soak_test(n_pairs=args.pairs, dry_run=args.dry_run)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
"""CLI demo: `python -m kimera.demo [csv_path] [--chunk N]`"""
import argparse
import os
import sys
from pathlib import Path
from .dataset import load_toy_dataset
from .reactor import reactor_cycle_batched


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", nargs="?", default=None, help="CSV dataset path")
    parser.add_argument("--chunk", type=int, default=200, help="Batch size")
    parser.add_argument("--mp", type=int, default=0, 
                       help="Use multiprocessing with N workers (0=off)")
    parser.add_argument("--no-cache", action="store_true", 
                       help="Disable embedding cache")
    args = parser.parse_args()

    # Handle cache disabling
    if args.no_cache:
        os.environ["KIMERA_CACHE_DIR"] = "_nocache_temp"

    csv_path = (
        Path(args.csv)
        if args.csv
        else Path(os.getenv("KIMERA_DATASET_PATH", "data/toy_contradictions.csv"))
    )
    if not csv_path.exists():
        sys.exit(f"Dataset not found: {csv_path}")

    geoids = load_toy_dataset(csv_path)
    
    # Show cache status
    if not args.no_cache:
        from .cache import get_cache_stats
        cache_stats = get_cache_stats()
        print(f"📦 Cache: {cache_stats['embedding_cache_size']} embeddings cached")
    
    # Choose processing mode based on --mp flag
    if args.mp > 0:
        from .reactor_mp import reactor_cycle_parallel
        print(f"🚀 Using parallel processing with {args.mp} workers")
        stats = reactor_cycle_parallel(geoids, workers=args.mp, chunk=args.chunk)
        print("Workers used   :", stats["workers"])
        print("Chunks processed:", stats["chunks"])
        print("Mode           :", stats["mode"])
        
        # Performance recommendations
        if stats["mode"] == "multiprocessing" and len(geoids) < 5000:
            print("💡 Tip: For smaller datasets, try threading mode or larger chunks")
        elif stats["mode"] == "threading" and len(geoids) > 10000:
            print("💡 Tip: For larger datasets, try multiprocessing with --chunk 1000+")
    else:
        print("🔄 Using single-threaded processing")
        stats = reactor_cycle_batched(geoids, chunk=args.chunk)
        print("Pairs processed:", stats["pairs"])

    print("Loaded", stats["geoids"], "geoids")
    print("Latency (ms):", stats["latency_ms"])
    print("Δ Memory (MB):", stats["mem_mb"])
    print("Scars logged :", stats["new_scars"])
    
    # Show final cache stats
    if not args.no_cache:
        from .cache import get_cache_stats
        cache_stats = get_cache_stats()
        print(f"📦 Final cache: {cache_stats['embedding_cache_size']} embeddings")
        if cache_stats.get('cache_file_size_mb', 0) > 0:
            print(f"💾 Cache file: {cache_stats['cache_file_size_mb']:.1f} MB")


if __name__ == "__main__":
    main()

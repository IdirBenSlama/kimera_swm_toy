#!/usr/bin/env python3
"""
Performance comparison script for v0.4.0 parallel processing.

This script demonstrates the performance characteristics of different processing modes
and provides recommendations for optimal settings.
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def run_performance_test():
    """Run performance comparison between different processing modes."""
    from kimera.geoid import init_geoid
    from kimera.reactor import reactor_cycle_batched
    from kimera.reactor_mp import reactor_cycle_parallel, reactor_cycle_threaded
    
    print("🚀 Performance Comparison: v0.4.0 Parallel Processing")
    print("=" * 60)
    
    # Create test dataset
    print("📊 Creating test dataset (1000 geoids)...")
    geoids = [init_geoid(f"Performance test text {i} with some content", "en", ["perf"]) 
              for i in range(1000)]
    
    print(f"✅ Created {len(geoids)} geoids\n")
    
    # Test 1: Single-threaded baseline
    print("🔄 Test 1: Single-threaded (baseline)")
    start = time.perf_counter()
    stats_single = reactor_cycle_batched(geoids, chunk=200)
    single_time = time.perf_counter() - start
    print(f"   Time: {single_time:.2f}s ({stats_single['latency_ms']:.1f}ms)")
    print(f"   Scars: {stats_single['new_scars']}")
    print(f"   Memory: {stats_single['mem_mb']:.1f}MB\n")
    
    # Test 2: Threading mode
    print("🧵 Test 2: Threading mode (4 workers)")
    stats_thread = reactor_cycle_threaded(geoids, workers=4, chunk=200)
    thread_time = stats_thread['latency_ms'] / 1000
    print(f"   Time: {thread_time:.2f}s ({stats_thread['latency_ms']:.1f}ms)")
    print(f"   Scars: {stats_thread['new_scars']}")
    print(f"   Memory: {stats_thread['mem_mb']:.1f}MB")
    print(f"   Speedup: {single_time/thread_time:.2f}x\n")
    
    # Test 3: Auto-detection mode
    print("🤖 Test 3: Auto-detection mode")
    stats_auto = reactor_cycle_parallel(geoids, workers=4, chunk=200)
    auto_time = stats_auto['latency_ms'] / 1000
    print(f"   Mode: {stats_auto['mode']}")
    print(f"   Time: {auto_time:.2f}s ({stats_auto['latency_ms']:.1f}ms)")
    print(f"   Scars: {stats_auto['new_scars']}")
    print(f"   Memory: {stats_auto['mem_mb']:.1f}MB")
    print(f"   Speedup: {single_time/auto_time:.2f}x\n")
    
    # Test 4: Multiprocessing mode (forced)
    print("⚡ Test 4: Multiprocessing mode (forced)")
    stats_mp = reactor_cycle_parallel(geoids, workers=2, chunk=500, use_threading=False)
    mp_time = stats_mp['latency_ms'] / 1000
    print(f"   Mode: {stats_mp['mode']}")
    print(f"   Time: {mp_time:.2f}s ({stats_mp['latency_ms']:.1f}ms)")
    print(f"   Scars: {stats_mp['new_scars']}")
    print(f"   Memory: {stats_mp['mem_mb']:.1f}MB")
    print(f"   Speedup: {single_time/mp_time:.2f}x\n")
    
    # Summary and recommendations
    print("📋 Performance Summary")
    print("=" * 40)
    print(f"Single-threaded:  {single_time:.2f}s (baseline)")
    print(f"Threading:        {thread_time:.2f}s ({single_time/thread_time:.2f}x speedup)")
    print(f"Auto-detection:   {auto_time:.2f}s ({single_time/auto_time:.2f}x speedup)")
    print(f"Multiprocessing:  {mp_time:.2f}s ({single_time/mp_time:.2f}x speedup)")
    
    print("\n💡 Recommendations:")
    if thread_time < mp_time:
        print("   • Threading mode is faster for this dataset size")
        print("   • Auto-detection correctly chose the optimal mode")
    else:
        print("   • Multiprocessing mode is faster for this dataset size")
        print("   • Consider larger chunk sizes for multiprocessing")
    
    print("   • For datasets <5k geoids: Use threading or auto-detection")
    print("   • For datasets >10k geoids: Use multiprocessing with chunk=1000+")
    print("   • On Windows: Threading often performs better due to spawn overhead")

def run_chunk_size_analysis():
    """Analyze optimal chunk sizes for different modes."""
    from kimera.geoid import init_geoid
    from kimera.reactor_mp import reactor_cycle_threaded
    
    print("\n🔍 Chunk Size Analysis (Threading Mode)")
    print("=" * 45)
    
    # Create smaller test dataset
    geoids = [init_geoid(f"Chunk test {i}", "en", ["chunk"]) for i in range(400)]
    chunk_sizes = [50, 100, 200, 400]
    
    print(f"Testing with {len(geoids)} geoids, 2 workers\n")
    
    for chunk in chunk_sizes:
        stats = reactor_cycle_threaded(geoids, workers=2, chunk=chunk)
        print(f"Chunk {chunk:3d}: {stats['latency_ms']:6.1f}ms, "
              f"{stats['chunks']} chunks, {stats['new_scars']} scars")
    
    print("\n💡 Chunk Size Guidelines:")
    print("   • Smaller chunks: Better load balancing, more overhead")
    print("   • Larger chunks: Less overhead, potential load imbalance")
    print("   • Sweet spot: 100-500 geoids per chunk for most datasets")

if __name__ == "__main__":
    try:
        run_performance_test()
        run_chunk_size_analysis()
        
        print("\n🎉 Performance analysis complete!")
        print("\nTo test with your own data:")
        print("  poetry run python -m kimera.demo your_data.csv --mp 4")
        print("  poetry run python -m kimera.demo your_data.csv --mp 4 --chunk 1000")
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        import traceback
        traceback.print_exc()
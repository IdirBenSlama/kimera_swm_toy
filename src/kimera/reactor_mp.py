"""
Multiprocessing-enabled reactor for parallel geoid processing.

This module provides parallel versions of reactor cycles using multiprocessing.Pool
to distribute work across multiple CPU cores for improved performance on large datasets.

Note: On Windows, multiprocessing has high overhead due to process spawning and model
reloading. For smaller datasets (<10k geoids), single-threaded processing may be faster.
Consider using threading mode or larger chunk sizes (1000+) for better performance.
"""

import time
import psutil
import os
import platform
from multiprocessing import Pool, cpu_count
from typing import List, Optional, Dict
from .reactor import reactor_cycle
from .geoid import Geoid

__all__ = ["reactor_cycle_parallel", "reactor_cycle_threaded"]


def _run_cycle(batch: List[Geoid]) -> int:
    """Worker function for multiprocessing pool.
    
    Args:
        batch: List of geoids to process in this worker
        
    Returns:
        Number of new scars created in this batch
    """
    reactor_cycle(batch)
    return sum(len(g.scars) for g in batch)


def reactor_cycle_threaded(geoids: List[Geoid], workers: Optional[int] = None, chunk: int = 200) -> Dict:
    """Thread-based parallel wrapper around `reactor_cycle`.
    
    Uses threading instead of multiprocessing to avoid Windows spawn overhead.
    Better for smaller datasets or Windows systems.

    Parameters
    ----------
    geoids : List[Geoid]
        Full list of geoids (should be even number for optimal pairing).
    workers : int | None
        Number of worker threads; default = `cpu_count()`.
    chunk : int
        Geoids per worker chunk.
        
    Returns
    -------
    dict : stats including latency_ms, mem_mb, new_scars, workers, geoids
    """
    from multiprocessing.dummy import Pool as ThreadPool
    
    if workers is None:
        workers = cpu_count()

    t0 = time.perf_counter()
    rss0 = psutil.Process(os.getpid()).memory_info().rss / (1024 ** 2)

    # Slice geoids into chunks for parallel processing
    batches = [geoids[i : i + chunk] for i in range(0, len(geoids), chunk)]

    # Process batches in parallel using threads
    with ThreadPool(workers) as pool:
        scar_counts = pool.map(_run_cycle, batches)

    # Calculate performance metrics
    delta_mem = psutil.Process(os.getpid()).memory_info().rss / (1024 ** 2) - rss0
    latency = (time.perf_counter() - t0) * 1000  # Convert to milliseconds

    return {
        "workers": workers,
        "geoids": len(geoids),
        "latency_ms": round(latency, 2),
        "mem_mb": round(delta_mem, 2),
        "new_scars": sum(scar_counts),
        "chunks": len(batches),
        "mode": "threading"
    }


def reactor_cycle_parallel(geoids: List[Geoid], workers: Optional[int] = None, chunk: int = 200, 
                          use_threading: Optional[bool] = None) -> Dict:
    """Parallel wrapper around `reactor_cycle`.

    Parameters
    ----------
    geoids : List[Geoid]
        Full list of geoids (should be even number for optimal pairing).
    workers : int | None
        Number of worker processes/threads; default = `cpu_count() - 1` (min 1) for processes,
        `cpu_count()` for threads.
    chunk : int
        Geoids per worker chunk. Recommended: 1000+ for multiprocessing, 200+ for threading.
    use_threading : bool | None
        If True, use threading instead of multiprocessing. If None, auto-detect based on
        platform and dataset size (Windows or <5000 geoids -> threading).
        
    Returns
    -------
    dict : stats including latency_ms, mem_mb, new_scars, workers, geoids, mode
    """
    # Auto-detect best mode if not specified
    if use_threading is None:
        is_windows = platform.system() == "Windows"
        small_dataset = len(geoids) < 5000
        use_threading = is_windows or small_dataset
    
    if use_threading:
        return reactor_cycle_threaded(geoids, workers, chunk)
    
    # Use multiprocessing
    if workers is None:
        workers = max(cpu_count() - 1, 1)

    t0 = time.perf_counter()
    rss0 = psutil.Process(os.getpid()).memory_info().rss / (1024 ** 2)

    # Slice geoids into chunks for parallel processing
    batches = [geoids[i : i + chunk] for i in range(0, len(geoids), chunk)]

    # Process batches in parallel
    with Pool(workers) as pool:
        scar_counts = pool.starmap(_run_cycle, [(batch,) for batch in batches])

    # Calculate performance metrics
    delta_mem = psutil.Process(os.getpid()).memory_info().rss / (1024 ** 2) - rss0
    latency = (time.perf_counter() - t0) * 1000  # Convert to milliseconds

    return {
        "workers": workers,
        "geoids": len(geoids),
        "latency_ms": round(latency, 2),
        "mem_mb": round(delta_mem, 2),
        "new_scars": sum(scar_counts),
        "chunks": len(batches),
        "mode": "multiprocessing"
    }
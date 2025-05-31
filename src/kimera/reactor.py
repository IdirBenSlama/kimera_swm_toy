import random
import random
import time
import psutil
import os
from typing import List
from tqdm import tqdm
from .resonance import resonance, THRESH
from .scar import create_scar

__all__ = ["reactor_cycle", "reactor_cycle_batched"]


def random_pairs(seq: List):
    items = list(seq)
    random.shuffle(items)
    for i in range(0, len(items) - 1, 2):
        yield items[i], items[i + 1]


def reactor_cycle(geoids, cycles: int = 1):
    """Single‑thread cycle for ≤ 1 K geoids (legacy)."""
    for _ in range(cycles):
        for g1, g2 in random_pairs(geoids):
            r = resonance(g1, g2)
            if r < THRESH:
                create_scar(g1, g2, 1 - r)


def reactor_cycle_batched(geoids, chunk: int = 200, verbose: bool = True):
    """Process *all* geoids in chunks, log latency & memory.

    Returns dict(stats).
    """
    start = time.perf_counter()
    rss0 = psutil.Process(os.getpid()).memory_info().rss / (1024 ** 2)

    scars_before = sum(len(g.scars) for g in geoids)
    pairs_proc = 0

    it = range(0, len(geoids), chunk)
    if verbose:
        it = tqdm(it, desc="Reactor cycles", unit="chunk")

    for offset in it:
        batch = geoids[offset : offset + chunk]
        reactor_cycle(batch)  # one internal cycle
        pairs_proc += len(batch) // 2

    delta_mem = psutil.Process(os.getpid()).memory_info().rss / (1024 ** 2) - rss0
    elapsed = (time.perf_counter() - start) * 1000  # ms

    scars_after = sum(len(g.scars) for g in geoids)
    return {
        "geoids": len(geoids),
        "pairs": pairs_proc,
        "latency_ms": round(elapsed, 2),
        "mem_mb": round(delta_mem, 2),
        "new_scars": scars_after - scars_before,
    }

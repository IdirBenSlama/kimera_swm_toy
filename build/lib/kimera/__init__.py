
"""Kimera‑SWM core package (toy)"""
# Core classes
from .echoform import EchoForm  # noqa: F401
from .identity import Identity  # noqa: F401

# Legacy imports for backward compatibility
try:
    from .geoid import Geoid, init_geoid  # noqa: F401
except ImportError:
    # Geoid might have external dependencies
    pass

try:
    from .reactor import reactor_cycle, reactor_cycle_batched    # noqa: F401
    from .reactor_mp import reactor_cycle_parallel, reactor_cycle_threaded  # noqa: F401
except ImportError:
    # Reactor might have external dependencies
    pass

try:
    from .cache import embed_cache, resonance_cache, get_cache_stats, clear_embedding_cache  # noqa: F401
except ImportError:
    # Cache might have external dependencies
    pass

# Storage (optional - requires DuckDB)
try:
    from .storage import LatticeStorage  # noqa: F401
except ImportError:
    # Storage requires DuckDB which might not be installed
    pass

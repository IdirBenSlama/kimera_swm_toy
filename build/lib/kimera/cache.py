"""Simple disk-backed embedding & resonance cache.

Usage
-----
from kimera.cache import embed_cache, resonance_cache
vec = embed_cache.get(lang, text)
embed_cache.set(lang, text, vec)

r = resonance_cache.get(gid1, gid2)  # None if missing
resonance_cache.set(gid1, gid2, value)
"""
from pathlib import Path
import hashlib
import joblib
import os
import numpy as np
from typing import Optional, Any

def get_cache_dir() -> Path:
    """Get the cache directory, respecting environment variable."""
    cache_dir = Path(os.getenv("KIMERA_CACHE_DIR", ".cache"))
    try:
        cache_dir.mkdir(exist_ok=True)
        return cache_dir
    except Exception:
        # Fallback to temp directory if cache dir creation fails
        import tempfile
        fallback_dir = Path(tempfile.gettempdir()) / "kimera_cache"
        fallback_dir.mkdir(exist_ok=True)
        return fallback_dir

# ---------- Embedding cache ----------

def _emb_key(lang: str, text: str) -> str:
    """Generate a unique key for embedding cache."""
    h = hashlib.sha256(f"{lang}:{text}".encode()).hexdigest()
    return h

class EmbeddingCache:
    """Simple file-based embedding cache using one file per vector."""
    
    def get(self, lang: str, text: str) -> Optional[np.ndarray]:
        """Get cached embedding vector."""
        try:
            path = get_cache_dir() / f"{_emb_key(lang, text)}.pkl"
            return joblib.load(path) if path.exists() else None
        except Exception:
            return None
    
    def set(self, lang: str, text: str, vec: np.ndarray) -> None:
        """Store embedding vector in cache."""
        try:
            path = get_cache_dir() / f"{_emb_key(lang, text)}.pkl"
            joblib.dump(vec.copy(), path)
        except Exception:
            pass
    
    def clear(self) -> None:
        """Clear the cache."""
        try:
            cache_dir = get_cache_dir()
            for pkl_file in cache_dir.glob("*.pkl"):
                pkl_file.unlink()
        except Exception:
            pass
    
    def _get_cache_size(self) -> int:
        """Get number of cached embeddings."""
        try:
            cache_dir = get_cache_dir()
            return len(list(cache_dir.glob("*.pkl")))
        except Exception:
            return 0

embed_cache = EmbeddingCache()

# ---------- Resonance cache ----------

def _res_key(gid1: str, gid2: str) -> str:
    """Generate a unique key for resonance cache."""
    return "|".join(sorted([gid1, gid2]))

class ResonanceCache:
    """In-memory resonance cache for current session."""
    
    def __init__(self):
        self._mem = {}
    
    def get(self, gid1: str, gid2: str) -> Optional[Any]:
        """Get cached resonance value."""
        return self._mem.get(_res_key(gid1, gid2))
    
    def set(self, gid1: str, gid2: str, value: Any) -> None:
        """Store resonance value in cache."""
        self._mem[_res_key(gid1, gid2)] = value
    
    def clear(self) -> None:
        """Clear all cached resonance values."""
        self._mem.clear()

resonance_cache = ResonanceCache()

# ---------- Cache utilities ----------

def clear_embedding_cache() -> None:
    """Clear the embedding cache."""
    embed_cache.clear()

def get_cache_stats() -> dict:
    """Get cache statistics."""
    cache_dir = get_cache_dir()
    embedding_count = embed_cache._get_cache_size()
    
    stats = {
        "embedding_cache_size": embedding_count,
        "resonance_cache_size": len(resonance_cache._mem),
        "cache_dir": str(cache_dir),
        "cache_file_exists": embedding_count > 0
    }
    
    # Calculate total cache size
    try:
        total_size = sum(f.stat().st_size for f in cache_dir.glob("*.pkl"))
        stats["cache_file_size_mb"] = total_size / (1024 * 1024)
    except Exception:
        stats["cache_file_size_mb"] = 0
    
    return stats
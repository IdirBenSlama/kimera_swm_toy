from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
import numpy as np

@dataclass
class Geoid:
    raw: str                    # Original text content
    echo: str                   # Trimmed text used for hashing and embedding
    gid: str
    lang_axis: str
    context_layers: List[str]
    sem_vec: np.ndarray
    sym_vec: np.ndarray
    vdr: float
    scars: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


# ---- helper functions ----

def calc_vdr(lang: str, layers: List[str]) -> float:
    """Dummy VDR function – uniform per language for toy demo."""
    base = {"en": 0.8, "fr": 0.75, "ar": 0.7}.get(lang, 0.6)
    return base * (1 + 0.05 * len(layers))


# External – simple sentence encoder (CPU) with caching
from sentence_transformers import SentenceTransformer
from .cache import embed_cache

_encoder = SentenceTransformer("all-MiniLM-L6-v2")


def _encode_cached(text: str, lang: str = "en"):
    """Encode text with caching support."""
    cached = embed_cache.get(lang, text)
    if cached is not None:
        return cached
    vec = _encoder.encode(text)
    embed_cache.set(lang, text, vec)
    return vec

def sem_encoder(text: str, lang: str = "en"):
    """Semantic encoder with cache."""
    return _encode_cached(text, lang)

def sym_encoder(text: str, lang: str = "en"):
    """Symbolic encoder with cache (alias for semantic encoder in toy prototype)."""
    return _encode_cached(text, lang)


def init_geoid(text: str = None, lang: str = "en", layers: List[str] = None, *, raw: str | None = None, tags=None, **_) -> Geoid:
    # Handle flexible calling patterns
    if text is None and raw is not None:
        text = raw  # Use raw as text for encoding
    elif text is None:
        raise ValueError("Either 'text' or 'raw' must be provided")
    
    if raw is None:
        raw = text
    
    if layers is None:
        layers = tags if tags else ["default"]
    
    # Create echo (trimmed text for hashing and embedding)
    echo = raw.strip() if raw is not None else text.strip()
    
    # Generate stable hash from lang + echo
    import hashlib
    gid_input = f"{lang}:{echo}"
    gid = hashlib.sha256(gid_input.encode()).hexdigest()[:16]  # 16-char hex
    
    # Use echo for encoding (consistent with cache key)
    sem_vec = sem_encoder(echo, lang)
    sym_vec = sym_encoder(echo, lang)
    
    return Geoid(
        raw=raw,               # Store original text (or provided raw)
        echo=echo,             # Trimmed text for hashing/embedding
        gid=gid,               # Stable hash from lang + echo
        lang_axis=lang,
        context_layers=layers,
        sem_vec=sem_vec,
        sym_vec=sym_vec,
        vdr=calc_vdr(lang, layers),
    )

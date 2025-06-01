import numpy as np
import re
import os
from sklearn.metrics.pairwise import cosine_similarity
from .rope import rope_buffer
from .scar import fetch_scars  # <- only fetch_scars now

THRESH = 0.3  # resonance threshold

# Control negation fix via environment variable
ENABLE_NEGATION_FIX = os.getenv("KIMERA_NEGATION_FIX", "1") == "1"

# --- Negation-aware distance -------------------------------------------
NEGATIONS = {"not", "no", "never", "cannot", "can't", "won't", "doesn't", "isn't", "aren't", "wasn't", "weren't", "don't", "didn't", "hasn't", "haven't", "hadn't"}

def _has_negation(tokens: list[str]) -> bool:
    return any(tok.lower() in NEGATIONS for tok in tokens)

def negation_mismatch(txt1: str, txt2: str) -> bool:
    t1 = re.findall(r"\w+", txt1)
    t2 = re.findall(r"\w+", txt2)
    return _has_negation(t1) ^ _has_negation(t2)   # XOR
# ------------------------------------------------------------------------


def resonance(a, b):
    """Return resonance score between two geoids (0–1)."""
    sim = cosine_similarity(a.sem_vec.reshape(1, -1), b.sem_vec.reshape(1, -1))[0][0]
    rope_buffer.push(a.gid, b.gid, sim)
    penalty = (np.mean([s.weight for s in fetch_scars(a, b)]) if (a.scars or b.scars) else 0.0)
    score = sim * (1 - penalty)
    
    # Apply negation mismatch penalty (if enabled)
    if ENABLE_NEGATION_FIX and negation_mismatch(a.raw, b.raw):
        score -= 0.25          # push them further apart
        score = max(-1.0, score)
    
    return score


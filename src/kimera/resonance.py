import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .rope import rope_buffer
from .scar import fetch_scars  # <- only fetch_scars now

THRESH = 0.3  # resonance threshold


def resonance(a, b):
    """Return resonance score between two geoids (0–1)."""
    sim = cosine_similarity(a.sem_vec.reshape(1, -1), b.sem_vec.reshape(1, -1))[0][0]
    rope_buffer.push(a.gid, b.gid, sim)
    penalty = (np.mean([s.weight for s in fetch_scars(a, b)]) if (a.scars or b.scars) else 0.0)
    return sim * (1 - penalty)


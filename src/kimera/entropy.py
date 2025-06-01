"""
Entropy calculation and adaptive time decay for Kimera identities.
Implements Shannon entropy over term intensity distributions and entropy-based tau scaling.
"""

import math
from typing import List, Dict, Any, Optional


def calculate_shannon_entropy(intensities: List[float]) -> float:
    """
    Calculate Shannon entropy over a list of intensity values.
    
    Args:
        intensities: List of intensity values (will be normalized to probabilities)
        
    Returns:
        Shannon entropy in bits (log base 2)
    """
    if not intensities:
        return 0.0
    
    # Filter out zero or negative values
    positive_intensities = [i for i in intensities if i > 0]
    if not positive_intensities:
        return 0.0
    
    # Normalize to probabilities
    total = sum(positive_intensities)
    if total == 0:
        return 0.0
    
    probs = [i / total for i in positive_intensities]
    
    # Calculate Shannon entropy: H = -Σ(p * log2(p))
    entropy = 0.0
    for p in probs:
        if p > 0:
            entropy -= p * math.log2(p)
    
    return entropy


def calculate_term_entropy(terms: List[Dict[str, Any]]) -> float:
    """
    Calculate entropy from a list of term dictionaries.
    
    Args:
        terms: List of term dicts with 'intensity' field
        
    Returns:
        Shannon entropy of term intensities
    """
    intensities = []
    for term in terms:
        if isinstance(term, dict) and 'intensity' in term:
            intensity = term['intensity']
            if isinstance(intensity, (int, float)) and intensity > 0:
                intensities.append(float(intensity))
    
    return calculate_shannon_entropy(intensities)


def calculate_relationship_entropy(related_ids: List[str], weight: float = 1.0) -> float:
    """
    Calculate entropy for relationship-based identities (scars).
    
    Args:
        related_ids: List of related identity IDs
        weight: Relationship weight
        
    Returns:
        Entropy based on relationship count and weight
    """
    if not related_ids:
        return 0.0
    
    n_relations = len(related_ids)
    if n_relations <= 1:
        return 0.0
    
    # Uniform distribution entropy as baseline, scaled by weight
    return math.log2(n_relations) * weight


def adaptive_tau(base_tau: float, entropy: float, k: float = 0.1) -> float:
    """
    Calculate adaptive time decay constant based on entropy.
    
    Higher entropy identities decay slower (they represent richer information).
    
    Args:
        base_tau: Base time decay constant (seconds)
        entropy: Shannon entropy of the identity
        k: Entropy scaling factor (default: 0.1)
        
    Returns:
        Effective tau adjusted for entropy
    """
    return base_tau * (1 + k * entropy)


def decay_factor(age_seconds: float, tau_seconds: float) -> float:
    """
    Calculate exponential decay factor.
    
    Args:
        age_seconds: Age of the item in seconds
        tau_seconds: Time decay constant in seconds
        
    Returns:
        Decay factor between 0 and 1
    """
    if tau_seconds <= 0:
        return 0.0
    
    return math.exp(-age_seconds / tau_seconds)


def entropy_weighted_decay(age_seconds: float, base_tau: float, entropy: float, k: float = 0.1) -> float:
    """
    Calculate decay factor with entropy-weighted tau.
    
    Args:
        age_seconds: Age of the item in seconds
        base_tau: Base time decay constant in seconds
        entropy: Shannon entropy of the identity
        k: Entropy scaling factor
        
    Returns:
        Entropy-weighted decay factor
    """
    effective_tau = adaptive_tau(base_tau, entropy, k)
    return decay_factor(age_seconds, effective_tau)


# Default time constants
DEFAULT_TAU_DAYS = 14.0
DEFAULT_TAU_SECONDS = DEFAULT_TAU_DAYS * 24 * 3600
DEFAULT_ENTROPY_SCALING = 0.1
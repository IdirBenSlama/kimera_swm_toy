"""
Contradiction Detection Module for Kimera
=========================================

This module implements logical contradiction detection as a separate
concern from resonance. While resonance measures structural similarity,
contradiction detection identifies logical incompatibility.
"""

import re
from typing import Tuple, List
from .geoid import Geoid
from .resonance import resonance

# Negation patterns
NEGATION_WORDS = {
    "not", "no", "never", "cannot", "can't", "won't", "doesn't", 
    "isn't", "aren't", "wasn't", "weren't", "don't", "didn't", 
    "hasn't", "haven't", "hadn't", "none", "neither", "nor"
}

# Antonym patterns (expandable)
ANTONYM_PAIRS = [
    ("hot", "cold"), ("cold", "hot"),
    ("black", "white"), ("white", "black"),
    ("true", "false"), ("false", "true"),
    ("round", "flat"), ("flat", "round"),
    ("can", "cannot"), ("cannot", "can"),
    ("is", "is not"), ("is not", "is"),
    ("are", "are not"), ("are not", "are"),
    ("fly", "cannot fly"), ("cannot fly", "fly"),
]

def extract_core_claim(text: str) -> Tuple[str, str, bool]:
    """
    Extract subject, predicate, and whether it's negated.
    Simple heuristic parser.
    """
    text = text.lower().strip()
    has_negation = any(neg in text for neg in NEGATION_WORDS)
    
    # Simple pattern matching for "X is Y" type statements
    patterns = [
        r"(\w+)\s+(?:is|are)\s+(.+)",
        r"(\w+)\s+(?:can|cannot)\s+(.+)",
        r"(\w+)\s+(?:have|has)\s+(.+)",
        r"(\w+)\s+(?:live|lives)\s+(.+)",
    ]
    
    for pattern in patterns:
        match = re.match(pattern, text)
        if match:
            subject = match.group(1)
            predicate = match.group(2)
            return subject, predicate, has_negation
    
    # Fallback
    words = text.split()
    if len(words) >= 2:
        return words[0], " ".join(words[1:]), has_negation
    return text, "", has_negation

def detect_antonym_contradiction(text1: str, text2: str) -> bool:
    """Check if texts contain antonymous predicates about the same subject."""
    subj1, pred1, neg1 = extract_core_claim(text1)
    subj2, pred2, neg2 = extract_core_claim(text2)
    
    # Same subject check (fuzzy)
    if subj1.lower() != subj2.lower():
        return False
    
    # Check for antonym pairs
    for ant1, ant2 in ANTONYM_PAIRS:
        if ant1 in pred1 and ant2 in pred2:
            return True
        if ant2 in pred1 and ant1 in pred2:
            return True
    
    return False

def detect_negation_contradiction(text1: str, text2: str) -> bool:
    """Check if one text negates the other."""
    # Remove common words to focus on content
    common_words = {"the", "a", "an", "is", "are", "in", "on", "at"}
    
    words1 = set(text1.lower().split()) - common_words
    words2 = set(text2.lower().split()) - common_words
    
    # Check if texts share significant content
    overlap = words1 & words2
    if len(overlap) < 2:  # Not about the same thing
        return False
    
    # Check if one has negation and the other doesn't
    has_neg1 = any(neg in text1.lower() for neg in NEGATION_WORDS)
    has_neg2 = any(neg in text2.lower() for neg in NEGATION_WORDS)
    
    return has_neg1 != has_neg2  # XOR - one negated, one not

def detect_contradiction(geoid1: Geoid, geoid2: Geoid) -> Tuple[bool, float, str]:
    """
    Detect logical contradiction between two geoids.
    
    Returns:
        (is_contradiction, confidence, reasoning)
    """
    text1 = geoid1.raw.lower()
    text2 = geoid2.raw.lower()
    
    # First check resonance - high resonance usually means no contradiction
    res_score = resonance(geoid1, geoid2)
    if res_score > 0.8:
        return False, 0.9, f"High resonance ({res_score:.3f}) indicates compatibility"
    
    # Check for antonym-based contradictions
    if detect_antonym_contradiction(text1, text2):
        confidence = 0.85 if res_score < 0.3 else 0.7
        return True, confidence, "Antonymous predicates about same subject"
    
    # Check for negation-based contradictions
    if detect_negation_contradiction(text1, text2):
        confidence = 0.75 if res_score < 0.4 else 0.6
        return True, confidence, "One statement negates the other"
    
    # Low resonance alone doesn't mean contradiction
    if res_score < 0.3:
        return False, 0.8, f"Low resonance ({res_score:.3f}) but no logical contradiction - just unrelated"
    
    return False, 0.7, f"No contradiction detected (resonance: {res_score:.3f})"


def is_contradiction(text1: str, text2: str, lang: str = "en") -> Tuple[bool, float, str]:
    """
    Convenience function for contradiction detection from raw texts.
    
    Args:
        text1: First statement
        text2: Second statement  
        lang: Language code
        
    Returns:
        (is_contradiction, confidence, reasoning)
    """
    from .geoid import init_geoid
    
    geoid1 = init_geoid(text1, lang, ["contradiction_check"])
    geoid2 = init_geoid(text2, lang, ["contradiction_check"])
    
    return detect_contradiction(geoid1, geoid2)
"""
Enhanced Resonance Module
========================

Combines semantic similarity with pattern-based analysis
for more accurate resonance detection aligned with SWM principles.
"""

from .geoid import Geoid
from .resonance import resonance as semantic_resonance
from .pattern_extraction import enhanced_resonance as pattern_enhanced_resonance
from .advanced_patterns import extract_patterns_advanced, calculate_pattern_similarity_advanced

def resonance_v2(geoid1: Geoid, geoid2: Geoid) -> float:
    """
    Enhanced resonance calculation that considers both
    semantic similarity and structural patterns.
    
    This is closer to the SWM vision of finding deep
    structural similarities across domains.
    """
    # Get base semantic resonance
    semantic_score = semantic_resonance(geoid1, geoid2)
    
    # Enhance with pattern analysis
    enhanced_score = pattern_enhanced_resonance(
        geoid1.raw, 
        geoid2.raw, 
        semantic_score
    )
    
    return enhanced_score

def resonance_v3(geoid1: Geoid, geoid2: Geoid) -> float:
    """
    Advanced resonance using all four SWM pattern types.
    
    This implements a more complete SWM-aligned resonance detection
    by analyzing functional, structural, dynamic, and relational patterns.
    """
    # Get base semantic resonance
    semantic_score = semantic_resonance(geoid1, geoid2)
    
    # Extract advanced patterns
    patterns1 = extract_patterns_advanced(geoid1.raw)
    patterns2 = extract_patterns_advanced(geoid2.raw)
    
    # Calculate pattern similarity
    pattern_score = calculate_pattern_similarity_advanced(patterns1, patterns2)
    
    # Combine scores with weights
    # Pattern matching is weighted more heavily for cross-domain resonance
    if pattern_score > 0:
        combined_score = (0.3 * semantic_score) + (0.7 * pattern_score)
    else:
        # If no patterns found, fall back to semantic score
        combined_score = semantic_score
    
    return combined_score
"""
Pattern Extraction Module for Enhanced Resonance Detection
=========================================================

This module implements basic pattern extraction to improve Kimera's
ability to detect structural similarities beyond surface semantics.
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class ExtractedPattern:
    """Represents an extracted pattern from text."""
    pattern_type: str  # functional, structural, dynamic, relational
    subject: Optional[str] = None
    action: Optional[str] = None
    object: Optional[str] = None
    attributes: Dict[str, str] = None
    
    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}

# Action verb patterns that indicate functions
FUNCTIONAL_VERBS = {
    "transmit", "send", "carry", "transport", "deliver", "convey",
    "pump", "push", "circulate", "flow", "move", "transfer",
    "protect", "defend", "guard", "shield", "secure", "safeguard",
    "grow", "expand", "develop", "increase", "evolve", "progress",
    "lead", "guide", "direct", "manage", "control", "govern",
    "build", "construct", "create", "design", "form", "make",
    "connect", "link", "join", "bind", "unite", "bridge"
}

# Prepositions indicating relationships
RELATIONAL_PREPS = {
    "through", "across", "between", "among", "within", "inside",
    "towards", "against", "from", "to", "into", "onto"
}

def extract_functional_pattern(text: str) -> Optional[ExtractedPattern]:
    """
    Extract functional patterns (what does it do?).
    Simple regex-based extraction for demonstration.
    """
    text = text.lower().strip()
    
    # Pattern 1: Subject + Verb + Object
    # e.g., "The heart pumps blood"
    pattern1 = r"(?:the\s+)?(\w+)\s+(\w+s?)\s+(.+?)(?:\.|$)"
    match = re.match(pattern1, text)
    
    if match:
        subject = match.group(1)
        verb = match.group(2)
        obj = match.group(3)
        
        # Check if verb is functional
        if verb in FUNCTIONAL_VERBS or any(v in verb for v in FUNCTIONAL_VERBS):
            return ExtractedPattern(
                pattern_type="functional",
                subject=subject,
                action=verb,
                object=obj,
                attributes={"verb_type": "action"}
            )
    
    # Pattern 2: Subject + Verb + Preposition + Object
    # e.g., "Information flows through networks"
    pattern2 = r"(?:the\s+)?(\w+)\s+(\w+s?)\s+(" + "|".join(RELATIONAL_PREPS) + r")\s+(.+?)(?:\.|$)"
    match = re.match(pattern2, text)
    
    if match:
        subject = match.group(1)
        verb = match.group(2)
        prep = match.group(3)
        obj = match.group(4)
        
        return ExtractedPattern(
            pattern_type="functional",
            subject=subject,
            action=f"{verb} {prep}",
            object=obj,
            attributes={"verb_type": "directional", "preposition": prep}
        )
    
    return None

def extract_structural_pattern(text: str) -> Optional[ExtractedPattern]:
    """
    Extract structural patterns (how is it organized?).
    """
    text = text.lower().strip()
    
    # Look for hierarchical structures
    hierarchy_words = ["leads", "manages", "controls", "governs", "heads"]
    for word in hierarchy_words:
        if word in text:
            parts = text.split(word)
            if len(parts) == 2:
                return ExtractedPattern(
                    pattern_type="structural",
                    subject=parts[0].strip(),
                    action="hierarchical_relation",
                    object=parts[1].strip(),
                    attributes={"structure": "hierarchy", "relation": word}
                )
    
    # Look for compositional structures
    comp_words = ["contains", "includes", "comprises", "consists of", "made of"]
    for word in comp_words:
        if word in text:
            parts = text.split(word)
            if len(parts) == 2:
                return ExtractedPattern(
                    pattern_type="structural",
                    subject=parts[0].strip(),
                    action="compositional_relation",
                    object=parts[1].strip(),
                    attributes={"structure": "composition", "relation": word}
                )
    
    return None

def calculate_pattern_similarity(p1: ExtractedPattern, p2: ExtractedPattern) -> float:
    """
    Calculate similarity between two extracted patterns.
    """
    if p1 is None or p2 is None:
        return 0.0
    
    # Different pattern types have lower similarity
    if p1.pattern_type != p2.pattern_type:
        return 0.2
    
    score = 0.0
    
    # Similar actions boost score significantly
    if p1.action and p2.action:
        # Exact match
        if p1.action == p2.action:
            score += 0.5
        # Partial match (e.g., "pump" in "pumps")
        elif p1.action in p2.action or p2.action in p1.action:
            score += 0.3
        # Both are functional verbs
        elif (any(v in p1.action for v in FUNCTIONAL_VERBS) and 
              any(v in p2.action for v in FUNCTIONAL_VERBS)):
            score += 0.2
    
    # Similar attributes
    if p1.attributes and p2.attributes:
        common_attrs = set(p1.attributes.keys()) & set(p2.attributes.keys())
        if common_attrs:
            attr_similarity = sum(
                1.0 if p1.attributes[k] == p2.attributes[k] else 0.5
                for k in common_attrs
            ) / len(common_attrs)
            score += 0.3 * attr_similarity
    
    # Bonus for same verb type
    if (p1.attributes.get("verb_type") == p2.attributes.get("verb_type") and
        p1.attributes.get("verb_type") is not None):
        score += 0.2
    
    return min(score, 1.0)

def extract_patterns(text: str) -> List[ExtractedPattern]:
    """
    Extract all identifiable patterns from text.
    """
    patterns = []
    
    # Try functional pattern extraction
    func_pattern = extract_functional_pattern(text)
    if func_pattern:
        patterns.append(func_pattern)
    
    # Try structural pattern extraction
    struct_pattern = extract_structural_pattern(text)
    if struct_pattern:
        patterns.append(struct_pattern)
    
    return patterns

def enhanced_resonance(text1: str, text2: str, semantic_score: float) -> float:
    """
    Calculate enhanced resonance by combining semantic similarity
    with structural pattern matching.
    
    Args:
        text1: First text
        text2: Second text
        semantic_score: Original semantic similarity score
        
    Returns:
        Enhanced resonance score
    """
    # Extract patterns from both texts
    patterns1 = extract_patterns(text1)
    patterns2 = extract_patterns(text2)
    
    # If no patterns found, return original score
    if not patterns1 or not patterns2:
        return semantic_score
    
    # Find best pattern match
    max_pattern_score = 0.0
    for p1 in patterns1:
        for p2 in patterns2:
            pattern_score = calculate_pattern_similarity(p1, p2)
            max_pattern_score = max(max_pattern_score, pattern_score)
    
    # Combine semantic and pattern scores
    # Weight pattern matching more heavily for structural similarity
    enhanced_score = (0.4 * semantic_score) + (0.6 * max_pattern_score)
    
    return enhanced_score
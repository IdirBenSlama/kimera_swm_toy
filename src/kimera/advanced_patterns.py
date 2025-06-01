"""
Advanced Pattern Extraction Module
==================================

Implements all four SWM pattern types:
- Functional Patterns (what it does)
- Structural Patterns (how it's organized)
- Dynamic Patterns (how it changes)
- Relational Patterns (how it connects)
"""

import re
from typing import List, Dict, Optional, Set, Tuple
from dataclasses import dataclass, field

@dataclass
class Pattern:
    """Base class for all pattern types."""
    pattern_type: str
    confidence: float = 1.0
    attributes: Dict[str, any] = field(default_factory=dict)

@dataclass
class FunctionalPattern(Pattern):
    """What does it do? Its purpose, actions, inputs/outputs."""
    pattern_type: str = "functional"
    action: Optional[str] = None
    agent: Optional[str] = None
    patient: Optional[str] = None  # What is acted upon
    purpose: Optional[str] = None  # Why/for what goal

@dataclass
class StructuralPattern(Pattern):
    """How is it built/organized? Components and relationships."""
    pattern_type: str = "structural"
    whole: Optional[str] = None
    parts: List[str] = field(default_factory=list)
    organization: Optional[str] = None  # hierarchical, network, linear, etc.

@dataclass
class DynamicPattern(Pattern):
    """How does it change/behave over time?"""
    pattern_type: str = "dynamic"
    process: Optional[str] = None
    temporal_nature: Optional[str] = None  # cyclic, linear, continuous, etc.
    direction: Optional[str] = None  # growth, decay, oscillation, etc.

@dataclass
class RelationalPattern(Pattern):
    """How does it relate to other things?"""
    pattern_type: str = "relational"
    entity1: Optional[str] = None
    entity2: Optional[str] = None
    relation_type: Optional[str] = None  # similarity, contrast, dependency, etc.

# Expanded verb categories for better pattern detection
VERB_CATEGORIES = {
    "transfer": {"transmit", "send", "deliver", "transport", "carry", "convey", "transfer", "pass"},
    "movement": {"flow", "flows", "move", "travel", "circulate", "stream", "run", "go"},
    "transformation": {"change", "transform", "convert", "turn", "become", "evolve", "develop"},
    "protection": {"protect", "protects", "defend", "defends", "guard", "shield", "secure", "safeguard"},
    "creation": {"create", "build", "make", "construct", "form", "generate", "produce"},
    "control": {"control", "manage", "lead", "leads", "direct", "govern", "regulate", "guide"},
    "growth": {"grow", "grows", "expand", "increase", "develop", "spread", "extend", "advance"},
    "connection": {"connect", "link", "join", "bind", "unite", "attach", "couple"},
    "containment": {"contain", "contains", "hold", "store", "house", "include", "comprise", "encompass"}
}

def extract_functional_pattern_simple(text: str) -> Optional[FunctionalPattern]:
    """Extract functional patterns using simple regex."""
    text_lower = text.lower()
    pattern = FunctionalPattern()
    
    # Pattern: Subject + Verb + Object
    # e.g., "The heart pumps blood"
    regex = r"(?:the\s+)?(\w+)\s+(\w+s?)\s+(.+?)(?:\s+(?:through|to|from|into|onto)\s+(.+?))?(?:\.|$)"
    match = re.match(regex, text_lower)
    
    if match:
        pattern.agent = match.group(1)
        verb = match.group(2)
        pattern.patient = match.group(3)
        
        # Check verb category
        for category, verbs in VERB_CATEGORIES.items():
            if verb in verbs:
                pattern.action = verb
                pattern.attributes["action_category"] = category
                return pattern
    
    return None

def extract_structural_pattern_simple(text: str) -> Optional[StructuralPattern]:
    """Extract structural patterns using simple regex."""
    text_lower = text.lower()
    pattern = StructuralPattern()
    
    # Hierarchical patterns
    hierarchy_verbs = ["leads", "manages", "controls", "governs", "commands"]
    for verb in hierarchy_verbs:
        if verb in text_lower:
            pattern.organization = "hierarchy"
            parts = text_lower.split(verb)
            if len(parts) == 2:
                pattern.whole = parts[0].strip()
                pattern.parts = [parts[1].strip()]
                return pattern
    
    # Compositional patterns
    comp_phrases = ["contains", "includes", "consists of", "made of", "composed of"]
    for phrase in comp_phrases:
        if phrase in text_lower:
            pattern.organization = "composition"
            parts = text_lower.split(phrase)
            if len(parts) == 2:
                pattern.whole = parts[0].strip()
                pattern.parts = [parts[1].strip()]
                return pattern
    
    return None

def extract_dynamic_pattern_simple(text: str) -> Optional[DynamicPattern]:
    """Extract dynamic patterns using simple regex."""
    text_lower = text.lower()
    pattern = DynamicPattern()
    
    # Movement/flow patterns
    flow_verbs = ["flow", "flows", "move", "moves", "travel", "travels", "circulate", "circulates"]
    for verb in flow_verbs:
        if verb in text_lower:
            pattern.process = verb.rstrip('s')  # Remove plural 's'
            pattern.temporal_nature = "continuous"
            
            # Check for direction
            if "through" in text_lower:
                pattern.direction = "through"
            elif "to" in text_lower or "towards" in text_lower:
                pattern.direction = "towards"
            elif "from" in text_lower:
                pattern.direction = "from"
            
            return pattern
    
    # Growth/change patterns
    growth_verbs = ["grow", "grows", "expand", "expands", "evolve", "evolves", "develop", "develops"]
    for verb in growth_verbs:
        if verb in text_lower:
            pattern.process = verb.rstrip('s')
            pattern.temporal_nature = "progressive"
            pattern.direction = "growth"
            return pattern
    
    return None

def extract_relational_pattern_simple(text: str) -> Optional[RelationalPattern]:
    """Extract relational patterns using simple regex."""
    text_lower = text.lower()
    pattern = RelationalPattern()
    
    # Dependency patterns
    if "depends on" in text_lower or "requires" in text_lower:
        pattern.relation_type = "dependency"
        parts = re.split(r"depends on|requires", text_lower)
        if len(parts) == 2:
            pattern.entity1 = parts[0].strip()
            pattern.entity2 = parts[1].strip()
            return pattern
    
    # Similarity patterns
    if "like" in text_lower or "similar to" in text_lower:
        pattern.relation_type = "similarity"
        return pattern
    
    # Contrast patterns
    if "unlike" in text_lower or "different from" in text_lower:
        pattern.relation_type = "contrast"
        return pattern
    
    return None

def extract_patterns_advanced(text: str) -> List[Pattern]:
    """Extract all pattern types from text."""
    patterns = []
    
    # Try to extract each pattern type
    func_pattern = extract_functional_pattern_simple(text)
    if func_pattern:
        patterns.append(func_pattern)
    
    struct_pattern = extract_structural_pattern_simple(text)
    if struct_pattern:
        patterns.append(struct_pattern)
    
    dyn_pattern = extract_dynamic_pattern_simple(text)
    if dyn_pattern:
        patterns.append(dyn_pattern)
    
    rel_pattern = extract_relational_pattern_simple(text)
    if rel_pattern:
        patterns.append(rel_pattern)
    
    return patterns

def calculate_pattern_similarity_advanced(patterns1: List[Pattern], patterns2: List[Pattern]) -> float:
    """Calculate similarity between two sets of patterns."""
    if not patterns1 or not patterns2:
        return 0.0
    
    max_similarity = 0.0
    
    for p1 in patterns1:
        for p2 in patterns2:
            if p1.pattern_type != p2.pattern_type:
                continue
            
            similarity = 0.0
            
            if isinstance(p1, FunctionalPattern) and isinstance(p2, FunctionalPattern):
                # Compare actions
                if p1.action == p2.action:
                    similarity += 0.5
                elif (p1.attributes.get("action_category") == 
                      p2.attributes.get("action_category") and 
                      p1.attributes.get("action_category") is not None):
                    similarity += 0.3
                
                # Bonus for same verb category
                if p1.attributes.get("action_category") == p2.attributes.get("action_category"):
                    similarity += 0.2
            
            elif isinstance(p1, StructuralPattern) and isinstance(p2, StructuralPattern):
                if p1.organization == p2.organization:
                    similarity += 0.7
            
            elif isinstance(p1, DynamicPattern) and isinstance(p2, DynamicPattern):
                if p1.process == p2.process:
                    similarity += 0.5
                if p1.temporal_nature == p2.temporal_nature:
                    similarity += 0.3
                if p1.direction == p2.direction:
                    similarity += 0.2
            
            elif isinstance(p1, RelationalPattern) and isinstance(p2, RelationalPattern):
                if p1.relation_type == p2.relation_type:
                    similarity += 0.8
            
            max_similarity = max(max_similarity, similarity)
    
    return min(max_similarity, 1.0)
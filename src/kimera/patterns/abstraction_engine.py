"""
Pattern Abstraction Engine for SWM

This module implements deep pattern extraction from Geoids according to 
the Spherical Word Methodology. It extracts four types of patterns:
- Functional: What does it DO?
- Structural: How is it BUILT?
- Dynamic: How does it CHANGE?
- Relational: How does it RELATE?
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set, Tuple
from datetime import datetime
import numpy as np
from enum import Enum
import re


class PatternType(Enum):
    """Types of patterns in SWM"""
    FUNCTIONAL = "functional"
    STRUCTURAL = "structural"
    DYNAMIC = "dynamic"
    RELATIONAL = "relational"


@dataclass
class FunctionalPattern:
    """
    Describes the purpose, role, action, or effect of a Geoid
    
    Core question: What does it DO?
    """
    primary_functions: List[str] = field(default_factory=list)
    performs_actions: List[str] = field(default_factory=list)
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    goals: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    contexts: List[str] = field(default_factory=list)
    enabling_factors: List[str] = field(default_factory=list)
    limiting_factors: List[str] = field(default_factory=list)
    alternative_functions: List[str] = field(default_factory=list)
    
    def to_vector(self) -> np.ndarray:
        """Convert pattern to vector representation"""
        # Simple implementation: count features
        feature_counts = [
            len(self.primary_functions),
            len(self.performs_actions),
            len(self.inputs),
            len(self.outputs),
            len(self.goals),
            len(self.constraints),
            len(self.enabling_factors),
            len(self.limiting_factors)
        ]
        return np.array(feature_counts, dtype=np.float32)
    
    def similarity(self, other: FunctionalPattern) -> float:
        """Calculate similarity with another functional pattern"""
        # Compare overlapping elements
        similarities = []
        
        # Compare lists
        for attr in ['primary_functions', 'performs_actions', 'inputs', 
                    'outputs', 'goals']:
            self_set = set(getattr(self, attr))
            other_set = set(getattr(other, attr))
            if self_set or other_set:
                overlap = len(self_set & other_set)
                total = len(self_set | other_set)
                similarities.append(overlap / total if total > 0 else 0)
        
        return np.mean(similarities) if similarities else 0.0


@dataclass
class StructuralPattern:
    """
    Describes the internal organization and composition of a Geoid
    
    Core question: How is it BUILT?
    """
    components: List[str] = field(default_factory=list)
    arrangement_type: str = ""  # hierarchical, network, linear, etc.
    connections: Dict[str, List[str]] = field(default_factory=dict)
    boundaries: str = ""  # clear, fuzzy, permeable, etc.
    interfaces: List[str] = field(default_factory=list)
    organization_principle: str = ""  # centralized, distributed, etc.
    layers: List[str] = field(default_factory=list)
    core_vs_periphery: Dict[str, List[str]] = field(default_factory=dict)
    
    def to_vector(self) -> np.ndarray:
        """Convert pattern to vector representation"""
        # Encode structural features
        arrangement_encoding = {
            'hierarchical': 1, 'network': 2, 'linear': 3,
            'matrix': 4, 'circular': 5, 'fractal': 6
        }
        
        boundary_encoding = {
            'clear': 1, 'fuzzy': 2, 'permeable': 3,
            'rigid': 4, 'dynamic': 5
        }
        
        features = [
            len(self.components),
            arrangement_encoding.get(self.arrangement_type, 0),
            len(self.connections),
            boundary_encoding.get(self.boundaries, 0),
            len(self.interfaces),
            len(self.layers)
        ]
        
        return np.array(features, dtype=np.float32)


@dataclass
class DynamicPattern:
    """
    Describes behavior, changes, and evolution of a Geoid over time
    
    Core question: How does it CHANGE?
    """
    states: List[str] = field(default_factory=list)
    transitions: List[Tuple[str, str]] = field(default_factory=list)
    triggers: Dict[str, str] = field(default_factory=dict)
    temporal_nature: str = ""  # cyclical, linear, sporadic, etc.
    rate_of_change: str = ""  # fast, slow, variable, etc.
    feedback_loops: List[Dict[str, Any]] = field(default_factory=list)
    evolution_path: List[str] = field(default_factory=list)
    stability_factors: List[str] = field(default_factory=list)
    change_drivers: List[str] = field(default_factory=list)
    
    def to_vector(self) -> np.ndarray:
        """Convert pattern to vector representation"""
        temporal_encoding = {
            'cyclical': 1, 'linear': 2, 'sporadic': 3,
            'oscillating': 4, 'exponential': 5, 'chaotic': 6
        }
        
        rate_encoding = {
            'fast': 1, 'slow': 2, 'variable': 3,
            'accelerating': 4, 'decelerating': 5
        }
        
        features = [
            len(self.states),
            len(self.transitions),
            temporal_encoding.get(self.temporal_nature, 0),
            rate_encoding.get(self.rate_of_change, 0),
            len(self.feedback_loops),
            len(self.evolution_path)
        ]
        
        return np.array(features, dtype=np.float32)


@dataclass
class RelationalPattern:
    """
    Describes how a Geoid relates to other entities
    
    Core question: How does it RELATE?
    """
    similar_to: List[str] = field(default_factory=list)
    opposite_to: List[str] = field(default_factory=list)
    part_of: List[str] = field(default_factory=list)
    contains: List[str] = field(default_factory=list)
    depends_on: List[str] = field(default_factory=list)
    influences: List[str] = field(default_factory=list)
    influenced_by: List[str] = field(default_factory=list)
    complements: List[str] = field(default_factory=list)
    conflicts_with: List[str] = field(default_factory=list)
    exchanges_with: Dict[str, str] = field(default_factory=dict)
    
    def to_vector(self) -> np.ndarray:
        """Convert pattern to vector representation"""
        features = [
            len(self.similar_to),
            len(self.opposite_to),
            len(self.part_of),
            len(self.contains),
            len(self.depends_on),
            len(self.influences),
            len(self.influenced_by),
            len(self.complements),
            len(self.conflicts_with),
            len(self.exchanges_with)
        ]
        
        return np.array(features, dtype=np.float32)


@dataclass
class AbstractedPatternSet:
    """Complete set of abstracted patterns for a Geoid"""
    geoid_id: str
    functional: FunctionalPattern
    structural: StructuralPattern
    dynamic: DynamicPattern
    relational: RelationalPattern
    extraction_timestamp: datetime = field(default_factory=datetime.utcnow)
    confidence_scores: Dict[PatternType, float] = field(default_factory=dict)
    
    def get_pattern(self, pattern_type: PatternType):
        """Get specific pattern by type"""
        mapping = {
            PatternType.FUNCTIONAL: self.functional,
            PatternType.STRUCTURAL: self.structural,
            PatternType.DYNAMIC: self.dynamic,
            PatternType.RELATIONAL: self.relational
        }
        return mapping.get(pattern_type)
    
    def to_composite_vector(self) -> np.ndarray:
        """Create composite vector from all patterns"""
        vectors = [
            self.functional.to_vector(),
            self.structural.to_vector(),
            self.dynamic.to_vector(),
            self.relational.to_vector()
        ]
        return np.concatenate(vectors)


class PatternAbstractionEngine:
    """
    Engine for extracting deep patterns from Geoids according to SWM methodology
    """
    
    def __init__(self):
        """Initialize the pattern abstraction engine"""
        self._init_extraction_rules()
        self._init_pattern_indicators()
    
    def _init_extraction_rules(self):
        """Initialize rules for pattern extraction"""
        # Action verbs for functional patterns
        self.action_verbs = {
            'protect', 'defend', 'create', 'destroy', 'transform',
            'connect', 'separate', 'filter', 'process', 'generate',
            'identify', 'analyze', 'synthesize', 'regulate', 'control',
            'enable', 'prevent', 'facilitate', 'inhibit', 'amplify'
        }
        
        # Structure indicators
        self.structure_words = {
            'system', 'network', 'hierarchy', 'layer', 'component',
            'module', 'interface', 'boundary', 'core', 'periphery',
            'node', 'link', 'cluster', 'group', 'collection'
        }
        
        # Change indicators
        self.change_words = {
            'evolve', 'adapt', 'grow', 'shrink', 'cycle', 'oscillate',
            'transform', 'transition', 'shift', 'develop', 'decay',
            'emerge', 'collapse', 'stabilize', 'fluctuate'
        }
        
        # Relation indicators
        self.relation_words = {
            'similar', 'different', 'opposite', 'related', 'connected',
            'depends', 'influences', 'contains', 'part', 'whole',
            'complements', 'conflicts', 'supports', 'opposes'
        }
    
    def _init_pattern_indicators(self):
        """Initialize pattern-specific indicators"""
        self.pattern_indicators = {
            PatternType.FUNCTIONAL: {
                'keywords': self.action_verbs,
                'questions': [
                    "What is its primary purpose?",
                    "What actions does it perform?",
                    "What inputs does it require?",
                    "What outputs does it produce?",
                    "What goals does it achieve?"
                ]
            },
            PatternType.STRUCTURAL: {
                'keywords': self.structure_words,
                'questions': [
                    "What are its main components?",
                    "How are the parts organized?",
                    "What defines its boundaries?",
                    "What are its interfaces?",
                    "What is its organizing principle?"
                ]
            },
            PatternType.DYNAMIC: {
                'keywords': self.change_words,
                'questions': [
                    "What states can it be in?",
                    "How does it change over time?",
                    "What triggers transitions?",
                    "What patterns of change exist?",
                    "What drives its evolution?"
                ]
            },
            PatternType.RELATIONAL: {
                'keywords': self.relation_words,
                'questions': [
                    "What is it similar to?",
                    "What does it depend on?",
                    "What does it influence?",
                    "What contains or is contained by it?",
                    "What does it exchange with?"
                ]
            }
        }
    
    def extract_patterns(self, geoid) -> AbstractedPatternSet:
        """
        Extract all pattern types from a Geoid
        
        Args:
            geoid: GeoidV2 instance to analyze
            
        Returns:
            AbstractedPatternSet with all extracted patterns
        """
        # Extract individual patterns
        functional = self.extract_functional_patterns(geoid)
        structural = self.extract_structural_patterns(geoid)
        dynamic = self.extract_dynamic_patterns(geoid)
        relational = self.extract_relational_patterns(geoid)
        
        # Calculate confidence scores
        confidence_scores = {
            PatternType.FUNCTIONAL: self._calculate_confidence(functional),
            PatternType.STRUCTURAL: self._calculate_confidence(structural),
            PatternType.DYNAMIC: self._calculate_confidence(dynamic),
            PatternType.RELATIONAL: self._calculate_confidence(relational)
        }
        
        return AbstractedPatternSet(
            geoid_id=geoid.gid,
            functional=functional,
            structural=structural,
            dynamic=dynamic,
            relational=relational,
            confidence_scores=confidence_scores
        )
    
    def extract_functional_patterns(self, geoid) -> FunctionalPattern:
        """
        Extract functional patterns: What does it DO?
        """
        pattern = FunctionalPattern()
        
        # Analyze text for functional elements
        text = geoid.raw.lower()
        words = text.split()
        
        # Extract action verbs
        for word in words:
            if word in self.action_verbs:
                pattern.performs_actions.append(word)
        
        # Extract purpose indicators
        purpose_patterns = [
            r'(?:purpose|goal|aim|objective) (?:is|are) (.*?)(?:\.|,|$)',
            r'(?:designed|meant|intended) (?:to|for) (.*?)(?:\.|,|$)',
            r'(?:in order to|so that|to) (.*?)(?:\.|,|$)'
        ]
        
        for regex in purpose_patterns:
            matches = re.findall(regex, text)
            pattern.goals.extend(matches)
        
        # Extract input/output patterns
        if 'from' in text:
            # Extract inputs (simplified)
            from_idx = text.index('from')
            input_text = text[from_idx:from_idx+30].split()[1:3]
            pattern.inputs.extend(input_text)
        
        if 'produce' in text or 'generate' in text or 'create' in text:
            # Extract outputs (simplified)
            pattern.outputs.append('generated_output')
        
        # Identify primary function from actions
        if pattern.performs_actions:
            pattern.primary_functions = pattern.performs_actions[:2]
        
        # Extract constraints
        constraint_words = ['must', 'cannot', 'should not', 'limited', 'restricted']
        for word in constraint_words:
            if word in text:
                pattern.constraints.append(f"{word}_constraint")
        
        return pattern
    
    def extract_structural_patterns(self, geoid) -> StructuralPattern:
        """
        Extract structural patterns: How is it BUILT?
        """
        pattern = StructuralPattern()
        
        text = geoid.raw.lower()
        words = text.split()
        
        # Extract components
        for word in words:
            if word in self.structure_words:
                pattern.components.append(word)
        
        # Determine arrangement type
        if 'hierarchy' in text or 'hierarchical' in text:
            pattern.arrangement_type = 'hierarchical'
        elif 'network' in text:
            pattern.arrangement_type = 'network'
        elif 'linear' in text or 'sequence' in text:
            pattern.arrangement_type = 'linear'
        elif 'distributed' in text:
            pattern.arrangement_type = 'distributed'
        else:
            pattern.arrangement_type = 'unknown'
        
        # Extract boundaries
        if 'boundary' in text or 'border' in text:
            if 'clear' in text:
                pattern.boundaries = 'clear'
            elif 'fuzzy' in text or 'unclear' in text:
                pattern.boundaries = 'fuzzy'
            else:
                pattern.boundaries = 'defined'
        
        # Extract interfaces
        interface_words = ['interface', 'connection', 'link', 'bridge']
        for word in interface_words:
            if word in text:
                pattern.interfaces.append(word)
        
        # Determine organization principle
        if 'central' in text or 'centralized' in text:
            pattern.organization_principle = 'centralized'
        elif 'distributed' in text or 'decentralized' in text:
            pattern.organization_principle = 'distributed'
        elif 'self-organizing' in text:
            pattern.organization_principle = 'self-organizing'
        
        return pattern
    
    def extract_dynamic_patterns(self, geoid) -> DynamicPattern:
        """
        Extract dynamic patterns: How does it CHANGE?
        """
        pattern = DynamicPattern()
        
        text = geoid.raw.lower()
        
        # Extract states
        state_indicators = ['state', 'phase', 'stage', 'mode', 'condition']
        for indicator in state_indicators:
            if indicator in text:
                pattern.states.append(f"{indicator}_detected")
        
        # Determine temporal nature
        if 'cycle' in text or 'cyclical' in text:
            pattern.temporal_nature = 'cyclical'
        elif 'linear' in text or 'progression' in text:
            pattern.temporal_nature = 'linear'
        elif 'random' in text or 'sporadic' in text:
            pattern.temporal_nature = 'sporadic'
        elif 'oscillate' in text:
            pattern.temporal_nature = 'oscillating'
        
        # Extract rate of change
        if 'rapid' in text or 'fast' in text or 'quick' in text:
            pattern.rate_of_change = 'fast'
        elif 'slow' in text or 'gradual' in text:
            pattern.rate_of_change = 'slow'
        elif 'variable' in text or 'changing' in text:
            pattern.rate_of_change = 'variable'
        
        # Extract change drivers
        for word in text.split():
            if word in self.change_words:
                pattern.change_drivers.append(word)
        
        # Detect feedback loops
        if 'feedback' in text:
            loop_type = 'positive' if 'positive' in text else 'negative'
            pattern.feedback_loops.append({
                'type': loop_type,
                'mechanism': 'detected_feedback'
            })
        
        return pattern
    
    def extract_relational_patterns(self, geoid) -> RelationalPattern:
        """
        Extract relational patterns: How does it RELATE?
        """
        pattern = RelationalPattern()
        
        text = geoid.raw.lower()
        
        # Extract similarity relations
        if 'similar' in text or 'like' in text:
            pattern.similar_to.append('similar_entity')
        
        # Extract opposition relations
        if 'opposite' in text or 'contrary' in text or 'versus' in text:
            pattern.opposite_to.append('opposing_entity')
        
        # Extract hierarchical relations
        if 'part of' in text or 'component of' in text:
            pattern.part_of.append('larger_system')
        
        if 'contains' in text or 'includes' in text:
            pattern.contains.append('sub_component')
        
        # Extract dependency relations
        if 'depends on' in text or 'requires' in text:
            pattern.depends_on.append('dependency')
        
        # Extract influence relations
        if 'influences' in text or 'affects' in text:
            pattern.influences.append('influenced_entity')
        
        if 'influenced by' in text or 'affected by' in text:
            pattern.influenced_by.append('influencing_entity')
        
        # Extract complementary relations
        if 'complements' in text or 'works with' in text:
            pattern.complements.append('complementary_entity')
        
        # Extract conflict relations
        if 'conflicts' in text or 'opposes' in text:
            pattern.conflicts_with.append('conflicting_entity')
        
        return pattern
    
    def _calculate_confidence(self, pattern) -> float:
        """Calculate confidence score for a pattern"""
        # Count non-empty attributes
        filled_attributes = 0
        total_attributes = 0
        
        for attr_name in dir(pattern):
            if not attr_name.startswith('_'):
                attr_value = getattr(pattern, attr_name)
                if callable(attr_value):
                    continue
                total_attributes += 1
                if attr_value:  # Non-empty
                    filled_attributes += 1
        
        return filled_attributes / total_attributes if total_attributes > 0 else 0.0
    
    def compare_patterns(self, pattern_set1: AbstractedPatternSet, 
                        pattern_set2: AbstractedPatternSet) -> Dict[PatternType, float]:
        """
        Compare two pattern sets and return similarity scores
        """
        similarities = {}
        
        # Compare functional patterns
        func_sim = pattern_set1.functional.similarity(pattern_set2.functional)
        similarities[PatternType.FUNCTIONAL] = func_sim
        
        # Compare structural patterns (vector similarity)
        struct_vec1 = pattern_set1.structural.to_vector()
        struct_vec2 = pattern_set2.structural.to_vector()
        struct_sim = np.dot(struct_vec1, struct_vec2) / (
            np.linalg.norm(struct_vec1) * np.linalg.norm(struct_vec2) + 1e-8
        )
        similarities[PatternType.STRUCTURAL] = float(struct_sim)
        
        # Compare dynamic patterns
        dyn_vec1 = pattern_set1.dynamic.to_vector()
        dyn_vec2 = pattern_set2.dynamic.to_vector()
        dyn_sim = np.dot(dyn_vec1, dyn_vec2) / (
            np.linalg.norm(dyn_vec1) * np.linalg.norm(dyn_vec2) + 1e-8
        )
        similarities[PatternType.DYNAMIC] = float(dyn_sim)
        
        # Compare relational patterns
        rel_vec1 = pattern_set1.relational.to_vector()
        rel_vec2 = pattern_set2.relational.to_vector()
        rel_sim = np.dot(rel_vec1, rel_vec2) / (
            np.linalg.norm(rel_vec1) * np.linalg.norm(rel_vec2) + 1e-8
        )
        similarities[PatternType.RELATIONAL] = float(rel_sim)
        
        return similarities
    
    def find_pattern_resonance(self, pattern_set1: AbstractedPatternSet,
                              pattern_set2: AbstractedPatternSet,
                              threshold: float = 0.7) -> Dict[str, Any]:
        """
        Find resonance between two pattern sets
        
        Returns detailed resonance analysis including:
        - Pattern similarities
        - Strongest resonances
        - Cross-pattern insights
        """
        similarities = self.compare_patterns(pattern_set1, pattern_set2)
        
        # Find strongest resonances
        strong_resonances = {
            ptype: score for ptype, score in similarities.items()
            if score >= threshold
        }
        
        # Calculate overall resonance score
        overall_score = np.mean(list(similarities.values()))
        
        # Identify cross-pattern insights
        insights = []
        
        # Check for functional-structural alignment
        if (similarities[PatternType.FUNCTIONAL] > 0.6 and 
            similarities[PatternType.STRUCTURAL] > 0.6):
            insights.append("Strong form-function alignment detected")
        
        # Check for dynamic-relational coupling
        if (similarities[PatternType.DYNAMIC] > 0.6 and 
            similarities[PatternType.RELATIONAL] > 0.6):
            insights.append("Coupled evolution and relationship patterns")
        
        return {
            'similarities': similarities,
            'strong_resonances': strong_resonances,
            'overall_score': overall_score,
            'insights': insights,
            'is_resonant': overall_score >= threshold
        }
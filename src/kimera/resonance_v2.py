"""
Enhanced Resonance Detection for SWM

This module implements pattern-based resonance detection that goes beyond
simple semantic similarity to find deep structural connections between Geoids.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import numpy as np
from enum import Enum

from .patterns import PatternAbstractionEngine, PatternType, AbstractedPatternSet
from .linguistics import MultiLanguageAnalyzer
from .dimensions.geoid_v2 import GeoidV2, DimensionType


class ResonanceType(Enum):
    """Types of resonance between Geoids"""
    SEMANTIC = "semantic"           # Surface meaning similarity
    FUNCTIONAL = "functional"       # Similar purpose/role
    STRUCTURAL = "structural"       # Similar organization
    DYNAMIC = "dynamic"            # Similar behavior/evolution
    RELATIONAL = "relational"      # Similar connections
    ARCHETYPAL = "archetypal"      # Deep symbolic resonance
    CROSS_DOMAIN = "cross_domain"  # Resonance across different fields


@dataclass
class ResonanceResult:
    """Result of resonance detection between two Geoids"""
    geoid1_id: str
    geoid2_id: str
    resonance_types: Dict[ResonanceType, float] = field(default_factory=dict)
    pattern_similarities: Dict[PatternType, float] = field(default_factory=dict)
    domain_distance: float = 0.0
    insight_potential: float = 0.0
    discovered_insights: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    @property
    def overall_resonance(self) -> float:
        """Calculate overall resonance score"""
        if not self.resonance_types:
            return 0.0
        return np.mean(list(self.resonance_types.values()))
    
    @property
    def is_cross_domain(self) -> bool:
        """Check if this is a cross-domain resonance"""
        return self.domain_distance > 0.7
    
    @property
    def strongest_resonance(self) -> Tuple[ResonanceType, float]:
        """Get the strongest type of resonance"""
        if not self.resonance_types:
            return None, 0.0
        return max(self.resonance_types.items(), key=lambda x: x[1])


class DomainClassifier:
    """Classifies Geoids into domains for cross-domain detection"""
    
    def __init__(self):
        """Initialize domain classifier with keyword mappings"""
        self.domain_keywords = {
            'biology': {'cell', 'organism', 'life', 'evolution', 'gene', 'species', 
                       'ecosystem', 'immune', 'organ', 'tissue'},
            'technology': {'computer', 'network', 'software', 'algorithm', 'data',
                          'system', 'digital', 'code', 'program', 'interface'},
            'physics': {'energy', 'force', 'particle', 'wave', 'quantum', 'field',
                       'matter', 'space', 'time', 'gravity'},
            'social': {'society', 'culture', 'community', 'people', 'group',
                      'organization', 'institution', 'relationship', 'behavior'},
            'economics': {'market', 'economy', 'trade', 'value', 'resource',
                         'production', 'consumption', 'supply', 'demand'},
            'psychology': {'mind', 'thought', 'emotion', 'behavior', 'consciousness',
                          'perception', 'memory', 'learning', 'personality'},
            'art': {'creative', 'aesthetic', 'expression', 'beauty', 'design',
                   'composition', 'style', 'form', 'artistic'},
            'philosophy': {'existence', 'reality', 'truth', 'knowledge', 'ethics',
                          'meaning', 'consciousness', 'being', 'logic'}
        }
    
    def classify(self, geoid: GeoidV2) -> str:
        """Classify a Geoid into a domain"""
        text = geoid.raw.lower()
        
        # Count keyword matches for each domain
        domain_scores = {}
        for domain, keywords in self.domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            domain_scores[domain] = score
        
        # Return domain with highest score
        if domain_scores:
            best_domain = max(domain_scores.items(), key=lambda x: x[1])
            if best_domain[1] > 0:
                return best_domain[0]
        
        return 'general'
    
    def calculate_domain_distance(self, domain1: str, domain2: str) -> float:
        """Calculate conceptual distance between domains"""
        if domain1 == domain2:
            return 0.0
        
        # Define domain relationships (simplified)
        close_domains = {
            ('biology', 'psychology'): 0.4,
            ('physics', 'technology'): 0.3,
            ('social', 'economics'): 0.3,
            ('psychology', 'philosophy'): 0.4,
            ('art', 'philosophy'): 0.5
        }
        
        # Check if domains are closely related
        key = tuple(sorted([domain1, domain2]))
        if key in close_domains:
            return close_domains[key]
        
        # Otherwise, consider them distant
        return 0.8


class EnhancedResonanceDetector:
    """
    Detects deep resonance between Geoids using pattern matching,
    multi-language analysis, and cross-domain detection.
    """
    
    def __init__(self):
        """Initialize the enhanced resonance detector"""
        self.pattern_engine = PatternAbstractionEngine()
        self.language_analyzer = MultiLanguageAnalyzer()
        self.domain_classifier = DomainClassifier()
    
    def detect_resonance(self, geoid1: GeoidV2, geoid2: GeoidV2,
                        analyze_languages: bool = True) -> ResonanceResult:
        """
        Detect all types of resonance between two Geoids
        
        Args:
            geoid1: First Geoid
            geoid2: Second Geoid
            analyze_languages: Whether to perform multi-language analysis
            
        Returns:
            ResonanceResult with detailed resonance information
        """
        result = ResonanceResult(
            geoid1_id=geoid1.gid,
            geoid2_id=geoid2.gid
        )
        
        # 1. Extract patterns from both Geoids
        patterns1 = self.pattern_engine.extract_patterns(geoid1)
        patterns2 = self.pattern_engine.extract_patterns(geoid2)
        
        # 2. Calculate pattern-based resonances
        pattern_resonance = self.pattern_engine.find_pattern_resonance(
            patterns1, patterns2, threshold=0.3
        )
        result.pattern_similarities = pattern_resonance['similarities']
        
        # Map pattern similarities to resonance types
        result.resonance_types[ResonanceType.FUNCTIONAL] = \
            pattern_resonance['similarities'][PatternType.FUNCTIONAL]
        result.resonance_types[ResonanceType.STRUCTURAL] = \
            pattern_resonance['similarities'][PatternType.STRUCTURAL]
        result.resonance_types[ResonanceType.DYNAMIC] = \
            pattern_resonance['similarities'][PatternType.DYNAMIC]
        result.resonance_types[ResonanceType.RELATIONAL] = \
            pattern_resonance['similarities'][PatternType.RELATIONAL]
        
        # 3. Calculate semantic resonance
        semantic_sim = self._calculate_semantic_similarity(geoid1, geoid2)
        result.resonance_types[ResonanceType.SEMANTIC] = semantic_sim
        
        # 4. Detect archetypal resonance (if language analysis enabled)
        if analyze_languages:
            archetypal_sim = self._detect_archetypal_resonance(geoid1, geoid2)
            result.resonance_types[ResonanceType.ARCHETYPAL] = archetypal_sim
        
        # 5. Calculate domain distance
        domain1 = self.domain_classifier.classify(geoid1)
        domain2 = self.domain_classifier.classify(geoid2)
        result.domain_distance = self.domain_classifier.calculate_domain_distance(
            domain1, domain2
        )
        
        # 6. Evaluate cross-domain resonance
        if result.is_cross_domain and result.overall_resonance > 0.5:
            result.resonance_types[ResonanceType.CROSS_DOMAIN] = \
                result.overall_resonance * result.domain_distance
        
        # 7. Calculate insight potential
        result.insight_potential = self._calculate_insight_potential(result)
        
        # 8. Generate insights
        result.discovered_insights = self._generate_insights(
            result, patterns1, patterns2, domain1, domain2
        )
        
        return result
    
    def _calculate_semantic_similarity(self, geoid1: GeoidV2, 
                                     geoid2: GeoidV2) -> float:
        """Calculate semantic similarity using vector representations"""
        # Use semantic vectors
        vec1 = geoid1.sem_vec
        vec2 = geoid2.sem_vec
        
        # Cosine similarity
        similarity = np.dot(vec1, vec2) / (
            np.linalg.norm(vec1) * np.linalg.norm(vec2) + 1e-8
        )
        
        return float(np.clip(similarity, 0, 1))
    
    def _detect_archetypal_resonance(self, geoid1: GeoidV2, 
                                   geoid2: GeoidV2) -> float:
        """Detect deep archetypal resonance using multi-language analysis"""
        # Analyze both texts
        insight1 = self.language_analyzer.analyze(geoid1.raw)
        insight2 = self.language_analyzer.analyze(geoid2.raw)
        
        # Compare archetypes
        archetypes1 = set(insight1.symbolic_layer.archetypes)
        archetypes2 = set(insight2.symbolic_layer.archetypes)
        
        if not archetypes1 and not archetypes2:
            return 0.0
        
        # Calculate overlap
        shared = archetypes1 & archetypes2
        total = archetypes1 | archetypes2
        
        if not total:
            return 0.0
        
        return len(shared) / len(total)
    
    def _calculate_insight_potential(self, result: ResonanceResult) -> float:
        """
        Calculate the potential for generating novel insights
        
        High insight potential comes from:
        - Strong resonance across distant domains
        - Multiple types of resonance
        - Balanced pattern similarities
        """
        factors = []
        
        # Factor 1: Cross-domain bonus
        if result.is_cross_domain:
            factors.append(result.domain_distance * result.overall_resonance)
        
        # Factor 2: Multi-resonance bonus
        active_resonances = sum(1 for score in result.resonance_types.values() 
                               if score > 0.3)
        factors.append(active_resonances / len(ResonanceType))
        
        # Factor 3: Pattern diversity
        pattern_scores = list(result.pattern_similarities.values())
        if pattern_scores:
            # Reward balanced similarities (not all high or all low)
            variance = np.var(pattern_scores)
            factors.append(variance * 2)  # Scale variance contribution
        
        # Factor 4: Archetypal resonance bonus
        if ResonanceType.ARCHETYPAL in result.resonance_types:
            factors.append(result.resonance_types[ResonanceType.ARCHETYPAL] * 0.5)
        
        return min(np.mean(factors) if factors else 0.0, 1.0)
    
    def _generate_insights(self, result: ResonanceResult,
                          patterns1: AbstractedPatternSet,
                          patterns2: AbstractedPatternSet,
                          domain1: str, domain2: str) -> List[str]:
        """Generate insights based on resonance analysis"""
        insights = []
        
        # Cross-domain insights
        if result.is_cross_domain and result.overall_resonance > 0.5:
            insights.append(
                f"Cross-domain resonance discovered between {domain1} and {domain2} "
                f"(distance: {result.domain_distance:.2f})"
            )
        
        # Pattern-specific insights
        strongest_pattern = max(result.pattern_similarities.items(), 
                               key=lambda x: x[1])
        if strongest_pattern[1] > 0.6:
            insights.append(
                f"Strong {strongest_pattern[0].value} pattern alignment "
                f"({strongest_pattern[1]:.2f})"
            )
        
        # Functional-structural coupling
        if (result.pattern_similarities.get(PatternType.FUNCTIONAL, 0) > 0.5 and
            result.pattern_similarities.get(PatternType.STRUCTURAL, 0) > 0.5):
            insights.append(
                "Form-function coupling detected: structure mirrors purpose"
            )
        
        # Dynamic-relational coupling
        if (result.pattern_similarities.get(PatternType.DYNAMIC, 0) > 0.5 and
            result.pattern_similarities.get(PatternType.RELATIONAL, 0) > 0.5):
            insights.append(
                "Co-evolution pattern: changes in one affect relationships with others"
            )
        
        # Archetypal insights
        if result.resonance_types.get(ResonanceType.ARCHETYPAL, 0) > 0.5:
            insights.append(
                "Deep archetypal resonance suggests universal pattern or principle"
            )
        
        # High insight potential
        if result.insight_potential > 0.7:
            insights.append(
                f"High potential for novel insights (score: {result.insight_potential:.2f})"
            )
        
        return insights
    
    def find_resonant_cluster(self, geoids: List[GeoidV2], 
                            threshold: float = 0.5) -> List[Tuple[str, str, float]]:
        """
        Find clusters of resonant Geoids
        
        Returns list of (geoid1_id, geoid2_id, resonance_score) tuples
        """
        resonant_pairs = []
        
        for i in range(len(geoids)):
            for j in range(i + 1, len(geoids)):
                result = self.detect_resonance(geoids[i], geoids[j], 
                                             analyze_languages=False)
                
                if result.overall_resonance >= threshold:
                    resonant_pairs.append(
                        (geoids[i].gid, geoids[j].gid, result.overall_resonance)
                    )
        
        # Sort by resonance strength
        resonant_pairs.sort(key=lambda x: x[2], reverse=True)
        
        return resonant_pairs
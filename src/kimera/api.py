"""
Kimera Unified API
==================

Simple, clear API for using Kimera's capabilities:
- Resonance detection (finding deep similarities)
- Contradiction detection (finding logical incompatibilities)
- Pattern extraction (understanding structure)
"""

from typing import Tuple, List, Dict, Optional
import asyncio
from .geoid import init_geoid, Geoid
from .resonance import resonance as basic_resonance
from .enhanced_resonance import resonance_v2, resonance_v3
from .contradiction import is_contradiction
from .advanced_patterns import extract_patterns_advanced, Pattern

class Kimera:
    """Main API class for Kimera functionality."""
    
    def __init__(self, lang: str = "en", resonance_version: int = 3, enable_multilingual: bool = False):
        """
        Initialize Kimera.
        
        Args:
            lang: Default language for analysis
            resonance_version: Which resonance algorithm to use (1, 2, or 3)
            enable_multilingual: Enable multi-language analysis features
        """
        self.lang = lang
        self.resonance_version = resonance_version
        self.enable_multilingual = enable_multilingual
        
        # Select resonance function
        self.resonance_funcs = {
            1: basic_resonance,
            2: resonance_v2,
            3: resonance_v3
        }
        self.resonance_func = self.resonance_funcs.get(resonance_version, resonance_v3)
        
        # Initialize multi-language analyzer if enabled
        self._ml_analyzer = None
        if enable_multilingual:
            try:
                from .linguistics.multi_language_analyzer import MultiLanguageAnalyzer
                self._ml_analyzer = MultiLanguageAnalyzer()
            except ImportError:
                print("Warning: Multi-language features not available. Configure translation services.")
    
    def find_resonance(self, text1: str, text2: str) -> Dict[str, any]:
        """
        Find resonance (deep similarity) between two texts.
        
        This is Kimera's core strength - finding hidden connections
        and structural similarities across different domains.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Dictionary with:
            - score: Resonance score (0-1, higher = more similar)
            - interpretation: Human-readable interpretation
            - patterns: Extracted patterns from both texts
        """
        # Create geoids
        g1 = init_geoid(text1, self.lang, ["resonance"])
        g2 = init_geoid(text2, self.lang, ["resonance"])
        
        # Calculate resonance
        score = self.resonance_func(g1, g2)
        
        # Extract patterns
        patterns1 = extract_patterns_advanced(text1)
        patterns2 = extract_patterns_advanced(text2)
        
        # Interpret score
        if score > 0.8:
            interpretation = "Very strong resonance - deep structural similarity"
        elif score > 0.6:
            interpretation = "Strong resonance - significant shared patterns"
        elif score > 0.4:
            interpretation = "Moderate resonance - some shared aspects"
        elif score > 0.2:
            interpretation = "Weak resonance - limited similarity"
        else:
            interpretation = "Low resonance - largely unrelated"
        
        return {
            "score": score,
            "interpretation": interpretation,
            "patterns": {
                "text1": [self._pattern_to_dict(p) for p in patterns1],
                "text2": [self._pattern_to_dict(p) for p in patterns2]
            }
        }
    
    def detect_contradiction(self, text1: str, text2: str) -> Dict[str, any]:
        """
        Detect logical contradiction between two texts.
        
        This is a separate concern from resonance - it identifies
        when two statements cannot both be true.
        
        Args:
            text1: First statement
            text2: Second statement
            
        Returns:
            Dictionary with:
            - is_contradiction: Boolean
            - confidence: Confidence score (0-1)
            - reasoning: Explanation of the decision
        """
        is_contra, confidence, reasoning = is_contradiction(text1, text2, self.lang)
        
        return {
            "is_contradiction": is_contra,
            "confidence": confidence,
            "reasoning": reasoning
        }
    
    def extract_patterns(self, text: str) -> List[Dict[str, any]]:
        """
        Extract all SWM patterns from text.
        
        Patterns reveal the underlying structure of concepts:
        - Functional: What it does
        - Structural: How it's organized
        - Dynamic: How it changes
        - Relational: How it connects
        
        Args:
            text: Text to analyze
            
        Returns:
            List of pattern dictionaries
        """
        patterns = extract_patterns_advanced(text)
        return [self._pattern_to_dict(p) for p in patterns]
    
    def find_cross_domain_insights(self, concept: str, 
                                  knowledge_base: List[str], 
                                  threshold: float = 0.5) -> List[Dict[str, any]]:
        """
        Find insights by discovering resonances with a knowledge base.
        
        This is useful for:
        - Finding analogies for problem-solving
        - Discovering hidden connections
        - Generating creative insights
        
        Args:
            concept: The concept to explore
            knowledge_base: List of texts to search for resonances
            threshold: Minimum resonance score to include
            
        Returns:
            List of insights sorted by resonance score
        """
        concept_geoid = init_geoid(concept, self.lang, ["insight"])
        insights = []
        
        for knowledge in knowledge_base:
            knowledge_geoid = init_geoid(knowledge, self.lang, ["insight"])
            score = self.resonance_func(concept_geoid, knowledge_geoid)
            
            if score >= threshold:
                patterns = extract_patterns_advanced(knowledge)
                insights.append({
                    "text": knowledge,
                    "resonance_score": score,
                    "patterns": [self._pattern_to_dict(p) for p in patterns],
                    "potential_insight": self._generate_insight(concept, knowledge, patterns)
                })
        
        # Sort by score
        insights.sort(key=lambda x: x["resonance_score"], reverse=True)
        return insights
    
    def _pattern_to_dict(self, pattern: Pattern) -> Dict[str, any]:
        """Convert a Pattern object to a dictionary."""
        result = {
            "type": pattern.pattern_type,
            "confidence": pattern.confidence
        }
        
        # Add pattern-specific fields
        if hasattr(pattern, 'action'):
            result["action"] = pattern.action
        if hasattr(pattern, 'agent'):
            result["agent"] = pattern.agent
        if hasattr(pattern, 'patient'):
            result["patient"] = pattern.patient
        if hasattr(pattern, 'organization'):
            result["organization"] = pattern.organization
        if hasattr(pattern, 'process'):
            result["process"] = pattern.process
        if hasattr(pattern, 'temporal_nature'):
            result["temporal_nature"] = pattern.temporal_nature
        if hasattr(pattern, 'relation_type'):
            result["relation_type"] = pattern.relation_type
        
        if pattern.attributes:
            result["attributes"] = pattern.attributes
            
        return result
    
    def _generate_insight(self, concept: str, analogy: str, patterns: List[Pattern]) -> str:
        """Generate a potential insight from a resonance."""
        if not patterns:
            return "Consider the structural similarities"
        
        pattern = patterns[0]  # Use first pattern
        
        if pattern.pattern_type == "functional":
            return f"Study how '{pattern.action}' works in this domain"
        elif pattern.pattern_type == "structural":
            return f"Apply the '{pattern.organization}' organization pattern"
        elif pattern.pattern_type == "dynamic":
            return f"Examine the '{pattern.process}' process for insights"
        elif pattern.pattern_type == "relational":
            return f"Consider the '{pattern.relation_type}' relationship"
        else:
            return "Explore the underlying patterns"
    
    def analyze_multilingual(self, text: str, target_languages: Optional[List[str]] = None) -> Dict[str, any]:
        """
        Analyze text across multiple languages to find universal patterns.
        
        This advanced feature reveals patterns that transcend linguistic boundaries.
        
        Args:
            text: Text to analyze
            target_languages: Languages to analyze (default: major languages)
            
        Returns:
            Dictionary with multi-lingual analysis results
        """
        if not self._ml_analyzer:
            return {
                "error": "Multi-language analysis not enabled. Initialize with enable_multilingual=True"
            }
        
        # Run async analysis in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            analysis = loop.run_until_complete(
                self._ml_analyzer.analyze(text, self.lang)
            )
            
            return {
                "original_text": analysis.original_text,
                "original_language": analysis.original_language,
                "translations": {
                    lang: {
                        "text": result.translated_text,
                        "confidence": result.confidence
                    }
                    for lang, result in analysis.translations.items()
                },
                "patterns_by_language": {
                    lang: [self._pattern_to_dict(p) for p in patterns]
                    for lang, patterns in analysis.patterns.items()
                },
                "cross_lingual_resonances": analysis.cross_lingual_resonances,
                "universal_patterns": self._extract_universal_patterns(analysis.patterns)
            }
        finally:
            loop.close()
    
    def find_linguistic_invariants(self, concepts: List[str]) -> List[Dict[str, any]]:
        """
        Find patterns that remain constant across languages.
        
        These invariants reveal the deep structure of concepts that
        transcends linguistic and cultural boundaries.
        
        Args:
            concepts: List of concepts to analyze
            
        Returns:
            List of linguistic invariants found
        """
        if not self._ml_analyzer:
            return [{
                "error": "Multi-language analysis not enabled. Initialize with enable_multilingual=True"
            }]
        
        # Run async analysis
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            invariants = loop.run_until_complete(
                self._ml_analyzer.find_multilingual_insights(concepts)
            )
            
            return [{
                "concept": inv["concept"],
                "invariant": inv.get("linguistic_invariant", "No clear invariant found"),
                "languages_analyzed": inv["languages_analyzed"],
                "confidence": inv["top_resonance"]["combined_score"] if inv.get("top_resonance") else 0.0,
                "unique_patterns": inv.get("unique_patterns", [])
            } for inv in invariants]
        finally:
            loop.close()
    
    def _extract_universal_patterns(self, patterns_by_lang: Dict[str, List[Pattern]]) -> List[str]:
        """Extract patterns that appear across multiple languages."""
        pattern_counts = {}
        
        for lang, patterns in patterns_by_lang.items():
            for pattern in patterns:
                if hasattr(pattern, 'action') and pattern.action:
                    pattern_counts[pattern.action] = pattern_counts.get(pattern.action, 0) + 1
        
        # Find patterns that appear in 50%+ of languages
        threshold = len(patterns_by_lang) * 0.5
        universal = [
            action for action, count in pattern_counts.items()
            if count >= threshold
        ]
        
        return universal


# Convenience functions for direct use
def find_resonance(text1: str, text2: str, lang: str = "en") -> float:
    """Quick function to get just the resonance score."""
    kimera = Kimera(lang)
    return kimera.find_resonance(text1, text2)["score"]

def detect_contradiction(text1: str, text2: str, lang: str = "en") -> bool:
    """Quick function to check if texts contradict."""
    kimera = Kimera(lang)
    return kimera.detect_contradiction(text1, text2)["is_contradiction"]

def extract_patterns(text: str, lang: str = "en") -> List[Dict]:
    """Quick function to extract patterns."""
    kimera = Kimera(lang)
    return kimera.extract_patterns(text)
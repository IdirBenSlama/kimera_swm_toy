"""
Contradiction Detection V2: Fixed Version
========================================

Fixed version of contradiction detection with proper regex handling.
"""

import re
import numpy as np
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass

from .geoid import Geoid
from .resonance import resonance


@dataclass
class ContradictionAnalysis:
    """Detailed analysis of potential contradiction."""
    is_contradiction: bool
    confidence: float
    contradiction_type: Optional[str]
    shared_topic: Optional[str]
    opposing_claims: Optional[Tuple[str, str]]
    reasoning: str


class ContradictionDetectorV2:
    """Fixed contradiction detection."""
    
    def __init__(self):
        # Simple negation words
        self.negation_words = {
            'not', 'no', 'never', 'cannot', "can't", "won't", "doesn't", 
            "isn't", "aren't", "wasn't", "weren't", "don't", "didn't", 
            "hasn't", "haven't", "hadn't", 'none', 'neither', 'nor'
        }
        
        self.antonym_pairs = [
            ('true', 'false'), ('false', 'true'),
            ('hot', 'cold'), ('cold', 'hot'),
            ('black', 'white'), ('white', 'black'),
            ('blue', 'red'), ('red', 'blue'),
            ('good', 'bad'), ('bad', 'good'),
            ('right', 'wrong'), ('wrong', 'right'),
            ('positive', 'negative'), ('negative', 'positive'),
            ('on', 'off'), ('off', 'on'),
            ('open', 'closed'), ('closed', 'open'),
            ('alive', 'dead'), ('dead', 'alive'),
            ('wet', 'dry'), ('dry', 'wet'),
            ('light', 'dark'), ('dark', 'light'),
            ('fast', 'slow'), ('slow', 'fast'),
            ('high', 'low'), ('low', 'high'),
            ('big', 'small'), ('small', 'big'),
        ]
        
        # Color exclusions
        self.color_words = {'red', 'blue', 'green', 'yellow', 'black', 'white', 'purple', 'orange'}
    
    def has_negation(self, text: str) -> bool:
        """Check if text contains negation."""
        words = set(text.lower().split())
        return bool(words & self.negation_words)
    
    def remove_negation(self, text: str) -> str:
        """Remove negation words from text."""
        words = text.lower().split()
        filtered = [w for w in words if w not in self.negation_words]
        return ' '.join(filtered)
    
    def extract_content_words(self, text: str) -> set:
        """Extract content words (non-stopwords)."""
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'it', 'this', 'that'}
        words = set(text.lower().split()) - stopwords - self.negation_words
        return words
    
    def similar_content(self, text1: str, text2: str) -> float:
        """Calculate content similarity between texts."""
        words1 = self.extract_content_words(text1)
        words2 = self.extract_content_words(text2)
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        return len(intersection) / len(union) if union else 0.0
    
    def detect_negation_contradiction(self, text1: str, text2: str) -> Optional[ContradictionAnalysis]:
        """Detect negation-based contradictions."""
        neg1 = self.has_negation(text1)
        neg2 = self.has_negation(text2)
        
        # One negated, one not
        if neg1 != neg2:
            # Remove negations and compare content
            core1 = self.remove_negation(text1)
            core2 = self.remove_negation(text2)
            
            similarity = self.similar_content(core1, core2)
            
            if similarity > 0.5:  # Similar content
                return ContradictionAnalysis(
                    is_contradiction=True,
                    confidence=0.85,
                    contradiction_type="negation",
                    shared_topic=core1 if len(core1) < len(core2) else core2,
                    opposing_claims=(text1, text2),
                    reasoning="Direct negation of the same claim"
                )
        
        return None
    
    def detect_antonym_contradiction(self, text1: str, text2: str) -> Optional[ContradictionAnalysis]:
        """Detect antonym-based contradictions."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        # Check for antonym pairs
        for ant1, ant2 in self.antonym_pairs:
            if ant1 in words1 and ant2 in words2:
                # Check if they're talking about the same subject
                content_sim = self.similar_content(text1, text2)
                if content_sim > 0.3:  # Some shared content
                    return ContradictionAnalysis(
                        is_contradiction=True,
                        confidence=0.80,
                        contradiction_type="antonym",
                        shared_topic=f"antonyms: {ant1} vs {ant2}",
                        opposing_claims=(ant1, ant2),
                        reasoning=f"Antonymous terms: {ant1} vs {ant2}"
                    )
        
        return None
    
    def detect_color_contradiction(self, text1: str, text2: str) -> Optional[ContradictionAnalysis]:
        """Detect color contradictions (special case of mutual exclusion)."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        colors1 = words1 & self.color_words
        colors2 = words2 & self.color_words
        
        if colors1 and colors2 and colors1 != colors2:
            # Check if same subject
            content_sim = self.similar_content(text1, text2)
            if content_sim > 0.4:  # Shared subject
                return ContradictionAnalysis(
                    is_contradiction=True,
                    confidence=0.75,
                    contradiction_type="color_exclusion",
                    shared_topic="color properties",
                    opposing_claims=(list(colors1)[0], list(colors2)[0]),
                    reasoning=f"Conflicting colors: {colors1} vs {colors2}"
                )
        
        return None
    
    def analyze_contradiction(self, geoid1: Geoid, geoid2: Geoid) -> ContradictionAnalysis:
        """Main contradiction analysis."""
        text1 = geoid1.raw
        text2 = geoid2.raw
        
        # Check semantic similarity first
        semantic_similarity = resonance(geoid1, geoid2)
        
        # If very low similarity, they're unrelated
        if semantic_similarity < 0.2:
            return ContradictionAnalysis(
                is_contradiction=False,
                confidence=0.9,
                contradiction_type=None,
                shared_topic=None,
                opposing_claims=None,
                reasoning=f"Unrelated topics (similarity: {semantic_similarity:.3f})"
            )
        
        # Check for negation contradictions
        negation_result = self.detect_negation_contradiction(text1, text2)
        if negation_result:
            if semantic_similarity > 0.6:
                negation_result.confidence = min(0.95, negation_result.confidence + 0.1)
            return negation_result
        
        # Check for antonym contradictions
        antonym_result = self.detect_antonym_contradiction(text1, text2)
        if antonym_result:
            if semantic_similarity > 0.6:
                antonym_result.confidence = min(0.90, antonym_result.confidence + 0.1)
            return antonym_result
        
        # Check for color contradictions
        color_result = self.detect_color_contradiction(text1, text2)
        if color_result:
            if semantic_similarity > 0.6:
                color_result.confidence = min(0.85, color_result.confidence + 0.1)
            return color_result
        
        # No contradiction detected
        shared_words = self.extract_content_words(text1) & self.extract_content_words(text2)
        shared_topic = ' '.join(sorted(shared_words)) if shared_words else None
        
        return ContradictionAnalysis(
            is_contradiction=False,
            confidence=0.8,
            contradiction_type=None,
            shared_topic=shared_topic,
            opposing_claims=None,
            reasoning=f"No logical contradiction detected (similarity: {semantic_similarity:.3f})"
        )


# Global instance
_detector = ContradictionDetectorV2()


def analyze_contradiction(geoid1: Geoid, geoid2: Geoid) -> ContradictionAnalysis:
    """Analyze contradiction between two geoids."""
    return _detector.analyze_contradiction(geoid1, geoid2)


def detect_contradiction_v2(geoid1: Geoid, geoid2: Geoid) -> Tuple[bool, float, str]:
    """Backward-compatible interface."""
    analysis = analyze_contradiction(geoid1, geoid2)
    return analysis.is_contradiction, analysis.confidence, analysis.reasoning
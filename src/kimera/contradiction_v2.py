"""
Contradiction Detection V2: Rigorous Semantic Opposition
=======================================================

This module implements scientifically grounded contradiction detection based on:
1. Semantic similarity (topics must be related)
2. Polarity opposition (claims must be opposing)
3. Logical incompatibility (both cannot be true simultaneously)

Key principles:
- High similarity + opposite polarity = strong contradiction
- Low similarity = unrelated, not contradictory
- Validated against linguistic datasets
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
    contradiction_type: Optional[str]  # negation, antonym, mutual_exclusion, etc.
    shared_topic: Optional[str]
    opposing_claims: Optional[Tuple[str, str]]
    reasoning: str


class ContradictionDetectorV2:
    """
    Rigorous contradiction detection based on linguistic principles.
    
    A contradiction requires:
    1. Shared topic/subject (high semantic similarity)
    2. Opposing claims (negation, antonyms, mutual exclusion)
    3. Logical incompatibility
    """
    
    def __init__(self):
        # Linguistic resources
        self.negation_patterns = [
            (r'\b(is|are|was|were)\s+not\b', r'\b(is|are|was|were)\b'),
            (r'\b(can|could|will|would)\s+not\b', r'\b(can|could|will|would)\b'),
            (r'\b(has|have|had)\s+not\b', r'\b(has|have|had)\b'),
            (r'\bnever\b', r'\balways\b'),
            (r'\bnone\b', r'\ball\b|some\b'),
            (r'\bnobody\b', r'\beverybody\b|somebody\b'),
        ]
        
        self.antonym_pairs = [
            ('true', 'false'), ('false', 'true'),
            ('hot', 'cold'), ('cold', 'hot'),
            ('black', 'white'), ('white', 'black'),
            ('good', 'bad'), ('bad', 'good'),
            ('right', 'wrong'), ('wrong', 'right'),
            ('positive', 'negative'), ('negative', 'positive'),
            ('increase', 'decrease'), ('decrease', 'increase'),
            ('up', 'down'), ('down', 'up'),
            ('inside', 'outside'), ('outside', 'inside'),
            ('before', 'after'), ('after', 'before'),
            ('alive', 'dead'), ('dead', 'alive'),
            ('open', 'closed'), ('closed', 'open'),
            ('wet', 'dry'), ('dry', 'wet'),
            ('light', 'dark'), ('dark', 'light'),
            ('heavy', 'light'), ('light', 'heavy'),
            ('fast', 'slow'), ('slow', 'fast'),
            ('high', 'low'), ('low', 'high'),
            ('big', 'small'), ('small', 'big'),
            ('long', 'short'), ('short', 'long'),
            ('thick', 'thin'), ('thin', 'thick'),
        ]
        
        # Mutual exclusion patterns
        self.mutual_exclusions = [
            # Colors
            {'red', 'blue', 'green', 'yellow', 'black', 'white', 'purple', 'orange'},
            # States
            {'solid', 'liquid', 'gas', 'plasma'},
            # Directions
            {'north', 'south', 'east', 'west'},
            # Binary states
            {'on', 'off'}, {'open', 'closed'}, {'alive', 'dead'},
            # Quantities
            {'all', 'none', 'some'},
        ]
    
    def extract_subject_predicate(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract subject and predicate from a statement."""
        text = text.lower().strip()
        
        # Common patterns
        patterns = [
            # "X is Y"
            r'^(the\s+)?(\w+(?:\s+\w+)*?)\s+(is|are|was|were)\s+(.+)$',
            # "X can/will Y"
            r'^(the\s+)?(\w+(?:\s+\w+)*?)\s+(can|could|will|would)\s+(.+)$',
            # "X has Y"
            r'^(the\s+)?(\w+(?:\s+\w+)*?)\s+(has|have|had)\s+(.+)$',
        ]
        
        for pattern in patterns:
            match = re.match(pattern, text)
            if match:
                subject = match.group(2)
                predicate = match.group(3) + ' ' + match.group(4)
                return subject, predicate
        
        # Fallback: first noun phrase as subject
        words = text.split()
        if len(words) >= 2:
            return words[0], ' '.join(words[1:])
        
        return None, None
    
    def detect_negation_contradiction(self, text1: str, text2: str) -> Optional[ContradictionAnalysis]:
        """Detect contradictions based on negation patterns."""
        text1_lower = text1.lower()
        text2_lower = text2.lower()
        
        # Check each negation pattern
        for neg_pattern, pos_pattern in self.negation_patterns:
            # Check if one has negation and other has positive
            if re.search(neg_pattern, text1_lower) and re.search(pos_pattern, text2_lower):
                # Remove negation from text1 to compare core content
                core1 = re.sub(neg_pattern, r'\1', text1_lower)
                if self._similar_content(core1, text2_lower):
                    return ContradictionAnalysis(
                        is_contradiction=True,
                        confidence=0.85,
                        contradiction_type="negation",
                        shared_topic=self._extract_shared_topic(text1, text2),
                        opposing_claims=(text1, text2),
                        reasoning="Direct negation of the same claim"
                    )
            
            # Check reverse
            if re.search(neg_pattern, text2_lower) and re.search(pos_pattern, text1_lower):
                core2 = re.sub(neg_pattern, r'\1', text2_lower)
                if self._similar_content(text1_lower, core2):
                    return ContradictionAnalysis(
                        is_contradiction=True,
                        confidence=0.85,
                        contradiction_type="negation",
                        shared_topic=self._extract_shared_topic(text1, text2),
                        opposing_claims=(text1, text2),
                        reasoning="Direct negation of the same claim"
                    )
        
        return None
    
    def detect_antonym_contradiction(self, text1: str, text2: str) -> Optional[ContradictionAnalysis]:
        """Detect contradictions based on antonym pairs."""
        subj1, pred1 = self.extract_subject_predicate(text1)
        subj2, pred2 = self.extract_subject_predicate(text2)
        
        if not (subj1 and subj2 and pred1 and pred2):
            return None
        
        # Subjects must be similar
        if not self._similar_subjects(subj1, subj2):
            return None
        
        # Check for antonyms in predicates
        for ant1, ant2 in self.antonym_pairs:
            if ant1 in pred1 and ant2 in pred2:
                return ContradictionAnalysis(
                    is_contradiction=True,
                    confidence=0.80,
                    contradiction_type="antonym",
                    shared_topic=subj1,
                    opposing_claims=(pred1, pred2),
                    reasoning=f"Antonymous predicates: {ant1} vs {ant2}"
                )
            if ant2 in pred1 and ant1 in pred2:
                return ContradictionAnalysis(
                    is_contradiction=True,
                    confidence=0.80,
                    contradiction_type="antonym",
                    shared_topic=subj1,
                    opposing_claims=(pred1, pred2),
                    reasoning=f"Antonymous predicates: {ant2} vs {ant1}"
                )
        
        return None
    
    def detect_mutual_exclusion(self, text1: str, text2: str) -> Optional[ContradictionAnalysis]:
        """Detect contradictions based on mutually exclusive categories."""
        text1_words = set(text1.lower().split())
        text2_words = set(text2.lower().split())
        
        for exclusion_set in self.mutual_exclusions:
            matches1 = text1_words & exclusion_set
            matches2 = text2_words & exclusion_set
            
            if matches1 and matches2 and matches1 != matches2:
                # Same subject but different mutually exclusive properties
                subj1, _ = self.extract_subject_predicate(text1)
                subj2, _ = self.extract_subject_predicate(text2)
                
                if subj1 and subj2 and self._similar_subjects(subj1, subj2):
                    return ContradictionAnalysis(
                        is_contradiction=True,
                        confidence=0.75,
                        contradiction_type="mutual_exclusion",
                        shared_topic=subj1,
                        opposing_claims=(list(matches1)[0], list(matches2)[0]),
                        reasoning=f"Mutually exclusive properties: {matches1} vs {matches2}"
                    )
        
        return None
    
    def _similar_content(self, text1: str, text2: str) -> bool:
        """Check if two texts have similar content (for negation detection)."""
        # Remove common words
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'not', 'no'}
        words1 = set(text1.lower().split()) - stopwords
        words2 = set(text2.lower().split()) - stopwords
        
        if not words1 or not words2:
            return False
        
        # Jaccard similarity
        intersection = words1 & words2
        union = words1 | words2
        similarity = len(intersection) / len(union) if union else 0
        
        return similarity > 0.5
    
    def _similar_subjects(self, subj1: str, subj2: str) -> bool:
        """Check if two subjects refer to the same entity."""
        # Exact match
        if subj1.lower() == subj2.lower():
            return True
        
        # One contained in other (e.g., "sky" and "the sky")
        if subj1.lower() in subj2.lower() or subj2.lower() in subj1.lower():
            return True
        
        # Could add more sophisticated matching (synonyms, etc.)
        return False
    
    def _extract_shared_topic(self, text1: str, text2: str) -> str:
        """Extract the shared topic between two texts."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        # Remove stopwords
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'not', 'no', 'it', 'this', 'that'}
        content1 = words1 - stopwords
        content2 = words2 - stopwords
        
        shared = content1 & content2
        if shared:
            return ' '.join(sorted(shared))
        
        # Try to extract subject
        subj1, _ = self.extract_subject_predicate(text1)
        return subj1 or "unknown"
    
    def analyze_contradiction(self, geoid1: Geoid, geoid2: Geoid) -> ContradictionAnalysis:
        """
        Comprehensive contradiction analysis between two geoids.
        
        Returns detailed analysis including type, confidence, and reasoning.
        """
        text1 = geoid1.raw
        text2 = geoid2.raw
        
        # First check semantic similarity - contradictions require related topics
        semantic_similarity = resonance(geoid1, geoid2)
        
        # If very low similarity, they're unrelated, not contradictory
        if semantic_similarity < 0.2:
            return ContradictionAnalysis(
                is_contradiction=False,
                confidence=0.9,
                contradiction_type=None,
                shared_topic=None,
                opposing_claims=None,
                reasoning=f"Unrelated topics (similarity: {semantic_similarity:.3f})"
            )
        
        # Check for various types of contradictions
        
        # 1. Negation contradiction
        negation_result = self.detect_negation_contradiction(text1, text2)
        if negation_result:
            # Boost confidence if high semantic similarity
            if semantic_similarity > 0.6:
                negation_result.confidence = min(0.95, negation_result.confidence + 0.1)
            return negation_result
        
        # 2. Antonym contradiction
        antonym_result = self.detect_antonym_contradiction(text1, text2)
        if antonym_result:
            if semantic_similarity > 0.6:
                antonym_result.confidence = min(0.90, antonym_result.confidence + 0.1)
            return antonym_result
        
        # 3. Mutual exclusion
        exclusion_result = self.detect_mutual_exclusion(text1, text2)
        if exclusion_result:
            if semantic_similarity > 0.6:
                exclusion_result.confidence = min(0.85, exclusion_result.confidence + 0.1)
            return exclusion_result
        
        # No contradiction detected
        return ContradictionAnalysis(
            is_contradiction=False,
            confidence=0.8,
            contradiction_type=None,
            shared_topic=self._extract_shared_topic(text1, text2),
            opposing_claims=None,
            reasoning=f"No logical contradiction detected (similarity: {semantic_similarity:.3f})"
        )


# Global instance for convenience
_detector = ContradictionDetectorV2()


def detect_contradiction_v2(geoid1: Geoid, geoid2: Geoid) -> Tuple[bool, float, str]:
    """
    Backward-compatible interface for contradiction detection.
    
    Returns: (is_contradiction, confidence, reasoning)
    """
    analysis = _detector.analyze_contradiction(geoid1, geoid2)
    return analysis.is_contradiction, analysis.confidence, analysis.reasoning


def analyze_contradiction(geoid1: Geoid, geoid2: Geoid) -> ContradictionAnalysis:
    """
    Full contradiction analysis with detailed results.
    """
    return _detector.analyze_contradiction(geoid1, geoid2)
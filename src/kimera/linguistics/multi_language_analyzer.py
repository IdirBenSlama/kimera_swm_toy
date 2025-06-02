"""
Multi-Language Analyzer for SWM "1+3+1" Rule Implementation

This module implements Idir Ben Slama's linguistic heuristic:
- 1 Root Language (primary analysis language)
- 3 Unrelated Languages (maximally different perspectives)
- 1 Symbolic/Chaos Layer (non-linguistic patterns and paradoxes)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Set
from enum import Enum
import numpy as np
from datetime import datetime
import hashlib
import json
import logging

# Set up logging
logger = logging.getLogger(__name__)


class LanguageFamily(Enum):
    """Major language families for diversity calculation"""
    INDO_EUROPEAN = "indo_european"
    SINO_TIBETAN = "sino_tibetan"
    AFRO_ASIATIC = "afro_asiatic"
    NIGER_CONGO = "niger_congo"
    AUSTRONESIAN = "austronesian"
    DRAVIDIAN = "dravidian"
    TURKIC = "turkic"
    JAPONIC = "japonic"
    KOREANIC = "koreanic"
    URALIC = "uralic"
    SEMITIC = "semitic"
    BANTU = "bantu"
    ISOLATE = "isolate"


# Language metadata including family, script, and conceptual characteristics
LANGUAGE_METADATA = {
    'en': {
        'name': 'English',
        'family': LanguageFamily.INDO_EUROPEAN,
        'script': 'latin',
        'word_order': 'SVO',
        'morphology': 'analytic',
        'tense_system': 'complex',
        'conceptual_features': ['individualistic', 'future-oriented', 'explicit']
    },
    'zh': {
        'name': 'Chinese (Mandarin)',
        'family': LanguageFamily.SINO_TIBETAN,
        'script': 'chinese',
        'word_order': 'SVO',
        'morphology': 'isolating',
        'tense_system': 'aspectual',
        'conceptual_features': ['collective', 'context-dependent', 'implicit']
    },
    'ar': {
        'name': 'Arabic',
        'family': LanguageFamily.AFRO_ASIATIC,
        'script': 'arabic',
        'word_order': 'VSO',
        'morphology': 'fusional',
        'tense_system': 'tripartite',
        'conceptual_features': ['formal-register', 'root-based', 'metaphorical']
    },
    'sw': {
        'name': 'Swahili',
        'family': LanguageFamily.NIGER_CONGO,
        'script': 'latin',
        'word_order': 'SVO',
        'morphology': 'agglutinative',
        'tense_system': 'complex',
        'conceptual_features': ['communal', 'respectful', 'oral-tradition']
    },
    'ja': {
        'name': 'Japanese',
        'family': LanguageFamily.JAPONIC,
        'script': 'mixed',
        'word_order': 'SOV',
        'morphology': 'agglutinative',
        'tense_system': 'simple',
        'conceptual_features': ['hierarchical', 'indirect', 'contextual']
    },
    'hi': {
        'name': 'Hindi',
        'family': LanguageFamily.INDO_EUROPEAN,
        'script': 'devanagari',
        'word_order': 'SOV',
        'morphology': 'fusional',
        'tense_system': 'complex',
        'conceptual_features': ['honorific', 'aspectual', 'philosophical']
    },
    'yo': {
        'name': 'Yoruba',
        'family': LanguageFamily.NIGER_CONGO,
        'script': 'latin',
        'word_order': 'SVO',
        'morphology': 'isolating',
        'tense_system': 'aspectual',
        'conceptual_features': ['tonal', 'proverbial', 'spiritual']
    },
    'fi': {
        'name': 'Finnish',
        'family': LanguageFamily.URALIC,
        'script': 'latin',
        'word_order': 'SVO',
        'morphology': 'agglutinative',
        'tense_system': 'simple',
        'conceptual_features': ['case-rich', 'nature-oriented', 'precise']
    },
    'tr': {
        'name': 'Turkish',
        'family': LanguageFamily.TURKIC,
        'script': 'latin',
        'word_order': 'SOV',
        'morphology': 'agglutinative',
        'tense_system': 'evidential',
        'conceptual_features': ['evidential', 'vowel-harmony', 'respectful']
    },
    'ko': {
        'name': 'Korean',
        'family': LanguageFamily.KOREANIC,
        'script': 'hangul',
        'word_order': 'SOV',
        'morphology': 'agglutinative',
        'tense_system': 'simple',
        'conceptual_features': ['honorific', 'topic-prominent', 'hierarchical']
    }
}


@dataclass
class LanguageAnalysis:
    """Results from analyzing text in a specific language"""
    language: str
    text: str
    translated_text: Optional[str] = None
    key_concepts: List[str] = field(default_factory=list)
    unique_expressions: List[str] = field(default_factory=list)
    metaphors: List[str] = field(default_factory=list)
    cultural_context: Dict[str, Any] = field(default_factory=dict)
    grammatical_insights: Dict[str, Any] = field(default_factory=dict)
    semantic_field: List[str] = field(default_factory=list)
    confidence: float = 1.0


@dataclass
class SymbolicLayer:
    """The +1 layer: symbolic meanings and chaos patterns"""
    archetypes: List[str] = field(default_factory=list)
    paradoxes: List[Dict[str, Any]] = field(default_factory=list)
    chaos_patterns: List[str] = field(default_factory=list)
    emergent_symbols: List[str] = field(default_factory=list)
    contradictions: List[Tuple[str, str]] = field(default_factory=list)
    liminal_concepts: List[str] = field(default_factory=list)
    transformation_potential: float = 0.0


@dataclass
class MultiLanguageInsight:
    """Combined insights from multi-language analysis"""
    root_analysis: LanguageAnalysis
    unrelated_analyses: List[LanguageAnalysis]
    symbolic_layer: SymbolicLayer
    cross_linguistic_patterns: Dict[str, List[str]] = field(default_factory=dict)
    unique_perspectives: Dict[str, Any] = field(default_factory=dict)
    convergent_meanings: List[str] = field(default_factory=list)
    divergent_meanings: List[str] = field(default_factory=list)
    insight_score: float = 0.0
    timestamp: datetime = field(default_factory=datetime.utcnow)


def calculate_language_distance(lang1: str, lang2: str) -> float:
    """
    Calculate conceptual distance between two languages
    
    Returns a value between 0 (identical) and 1 (maximally different)
    """
    if lang1 == lang2:
        return 0.0
    
    meta1 = LANGUAGE_METADATA.get(lang1, {})
    meta2 = LANGUAGE_METADATA.get(lang2, {})
    
    if not meta1 or not meta2:
        return 0.5  # Default distance for unknown languages
    
    distance_factors = []
    
    # Language family distance
    if meta1.get('family') == meta2.get('family'):
        distance_factors.append(0.2)
    else:
        distance_factors.append(0.8)
    
    # Script system distance
    if meta1.get('script') == meta2.get('script'):
        distance_factors.append(0.1)
    else:
        distance_factors.append(0.9)
    
    # Word order distance
    if meta1.get('word_order') == meta2.get('word_order'):
        distance_factors.append(0.2)
    else:
        distance_factors.append(0.7)
    
    # Morphological type distance
    if meta1.get('morphology') == meta2.get('morphology'):
        distance_factors.append(0.3)
    else:
        distance_factors.append(0.7)
    
    # Conceptual features overlap
    features1 = set(meta1.get('conceptual_features', []))
    features2 = set(meta2.get('conceptual_features', []))
    if features1 and features2:
        overlap = len(features1 & features2) / len(features1 | features2)
        distance_factors.append(1.0 - overlap)
    
    return np.mean(distance_factors)


def select_unrelated_languages(root_lang: str, available_langs: Optional[List[str]] = None, 
                              n: int = 3) -> List[str]:
    """
    Select n maximally unrelated languages to the root language
    
    Implements the "3 unrelated languages" part of the 1+3+1 rule
    """
    if available_langs is None:
        available_langs = list(LANGUAGE_METADATA.keys())
    
    # Remove root language from candidates
    candidates = [lang for lang in available_langs if lang != root_lang]
    
    if len(candidates) <= n:
        return candidates
    
    # Calculate distances from root language
    distances = [(lang, calculate_language_distance(root_lang, lang)) 
                 for lang in candidates]
    
    # Sort by distance (descending) and diversity
    selected = []
    remaining = sorted(distances, key=lambda x: x[1], reverse=True)
    
    # Greedy selection for maximum diversity
    while len(selected) < n and remaining:
        # Take the most distant language
        next_lang, _ = remaining.pop(0)
        selected.append(next_lang)
        
        # Re-sort remaining by minimum distance to any selected language
        if remaining and len(selected) < n:
            remaining = sorted(remaining, 
                             key=lambda x: min(calculate_language_distance(x[0], s) 
                                             for s in selected), 
                             reverse=True)
    
    return selected


class MultiLanguageAnalyzer:
    """
    Implements the SWM "1+3+1" rule for multi-perspective analysis
    
    This analyzer provides deep multi-linguistic analysis of concepts
    to uncover hidden patterns and meanings across cultural contexts.
    """
    
    def __init__(self, translation_backend: Optional[str] = None):
        """
        Initialize the analyzer
        
        Args:
            translation_backend: Backend to use for translation 
                               ('google', 'local', or None for mock)
        """
        self.translation_backend = translation_backend
        self._init_translation_service()
        self._init_analysis_tools()
    
    def _init_translation_service(self):
        """Initialize translation service based on backend"""
        if self.translation_backend == 'google':
            try:
                from googletrans import Translator
                self.translator = Translator()
            except ImportError:
                logger.warning("googletrans not available, using mock translations")
                self.translator = None
        else:
            self.translator = None
    
    def _init_analysis_tools(self):
        """Initialize language analysis tools"""
        # Placeholder for language-specific analyzers
        self.analyzers = {}
    
    def analyze(self, text: str, root_lang: str = 'en', 
                target_langs: Optional[List[str]] = None) -> MultiLanguageInsight:
        """
        Perform full "1+3+1" analysis on text
        
        Args:
            text: Text to analyze
            root_lang: Root language code
            target_langs: Optional list of target languages 
                         (if None, will auto-select unrelated languages)
        
        Returns:
            MultiLanguageInsight with complete analysis
        """
        # 1. Analyze in root language
        root_analysis = self._analyze_root_language(text, root_lang)
        
        # 2. Select unrelated languages if not provided
        if target_langs is None:
            target_langs = select_unrelated_languages(root_lang, n=3)
        
        # 3. Analyze in unrelated languages
        unrelated_analyses = []
        for lang in target_langs:
            analysis = self._analyze_in_language(text, root_lang, lang)
            unrelated_analyses.append(analysis)
        
        # 4. Extract symbolic/chaos layer (+1)
        all_analyses = [root_analysis] + unrelated_analyses
        symbolic_layer = self._extract_symbolic_layer(text, all_analyses)
        
        # 5. Synthesize cross-linguistic insights
        insight = self._synthesize_insights(
            root_analysis, unrelated_analyses, symbolic_layer
        )
        
        return insight
    
    def _analyze_root_language(self, text: str, lang: str) -> LanguageAnalysis:
        """Analyze text in its root language"""
        analysis = LanguageAnalysis(
            language=lang,
            text=text,
            translated_text=None  # No translation needed for root
        )
        
        # Extract key concepts (mock implementation)
        words = text.lower().split()
        analysis.key_concepts = list(set(w for w in words if len(w) > 4))[:5]
        
        # Extract metaphors (simplified)
        metaphor_indicators = ['like', 'as', 'is', 'are']
        for indicator in metaphor_indicators:
            if indicator in words:
                idx = words.index(indicator)
                if idx > 0 and idx < len(words) - 1:
                    analysis.metaphors.append(f"{words[idx-1]} {indicator} {words[idx+1]}")
        
        # Add grammatical insights
        analysis.grammatical_insights = {
            'word_count': len(words),
            'avg_word_length': np.mean([len(w) for w in words]),
            'sentence_structure': 'simple' if len(words) < 10 else 'complex'
        }
        
        # Cultural context (mock)
        lang_meta = LANGUAGE_METADATA.get(lang, {})
        analysis.cultural_context = {
            'conceptual_features': lang_meta.get('conceptual_features', []),
            'morphology': lang_meta.get('morphology', 'unknown')
        }
        
        return analysis
    
    def _analyze_in_language(self, text: str, source_lang: str, 
                           target_lang: str) -> LanguageAnalysis:
        """Analyze text translated into target language"""
        # Translate text
        translated = self._translate(text, source_lang, target_lang)
        
        analysis = LanguageAnalysis(
            language=target_lang,
            text=text,
            translated_text=translated
        )
        
        # Language-specific analysis
        if translated:
            # Extract unique expressions
            analysis.unique_expressions = self._find_unique_expressions(
                translated, target_lang
            )
            
            # Extract semantic field
            analysis.semantic_field = self._extract_semantic_field(
                translated, target_lang
            )
            
            # Add language-specific insights
            lang_meta = LANGUAGE_METADATA.get(target_lang, {})
            analysis.cultural_context = {
                'conceptual_features': lang_meta.get('conceptual_features', []),
                'word_order': lang_meta.get('word_order', 'unknown'),
                'unique_perspective': self._get_unique_perspective(target_lang)
            }
        
        return analysis
    
    def _translate(self, text: str, source: str, target: str) -> Optional[str]:
        """Translate text between languages"""
        if self.translator:
            try:
                result = self.translator.translate(text, src=source, dest=target)
                return result.text
            except Exception as e:
                logger.error(f"Translation failed: {e}")
                return None
        else:
            # Mock translation for testing
            return f"[{target}] {text}"
    
    def _find_unique_expressions(self, text: str, lang: str) -> List[str]:
        """Find expressions unique to the target language"""
        # Simplified implementation
        expressions = []
        
        # Language-specific patterns
        if lang == 'ja':
            expressions.append("wa/ga distinction")
        elif lang == 'ar':
            expressions.append("root-pattern morphology")
        elif lang == 'zh':
            expressions.append("measure words")
        
        return expressions
    
    def _extract_semantic_field(self, text: str, lang: str) -> List[str]:
        """Extract semantic field in target language"""
        # Simplified implementation
        words = text.lower().split()
        
        # Mock semantic field based on language characteristics
        if lang in ['zh', 'ja']:
            return ['holistic', 'contextual', 'implicit']
        elif lang in ['ar', 'hi']:
            return ['formal', 'respectful', 'traditional']
        else:
            return ['explicit', 'direct', 'analytical']
    
    def _get_unique_perspective(self, lang: str) -> str:
        """Get unique perspective offered by language"""
        perspectives = {
            'zh': 'Emphasizes collective harmony and implicit understanding',
            'ar': 'Rich metaphorical expressions and formal registers',
            'ja': 'Hierarchical relationships and contextual nuance',
            'sw': 'Community-oriented with oral tradition influences',
            'fi': 'Precise spatial relationships through case system',
            'yo': 'Tonal variations convey emotional nuance'
        }
        return perspectives.get(lang, 'Unique grammatical and cultural perspective')
    
    def _extract_symbolic_layer(self, text: str, 
                               analyses: List[LanguageAnalysis]) -> SymbolicLayer:
        """
        Extract the +1 symbolic/chaos layer
        
        This identifies archetypes, paradoxes, and emergent patterns
        that transcend linguistic boundaries.
        """
        layer = SymbolicLayer()
        
        # Extract archetypes based on common patterns
        all_concepts = []
        for analysis in analyses:
            all_concepts.extend(analysis.key_concepts)
        
        # Identify archetypal patterns
        archetype_patterns = {
            'protection': ['protect', 'defend', 'guard', 'shield', 'safe'],
            'transformation': ['change', 'evolve', 'transform', 'become', 'shift'],
            'connection': ['link', 'connect', 'relate', 'bind', 'unite'],
            'conflict': ['fight', 'oppose', 'conflict', 'battle', 'struggle'],
            'creation': ['create', 'make', 'build', 'generate', 'produce'],
            'destruction': ['destroy', 'break', 'end', 'collapse', 'ruin']
        }
        
        for archetype, patterns in archetype_patterns.items():
            if any(p in ' '.join(all_concepts).lower() for p in patterns):
                layer.archetypes.append(archetype)
        
        # Find paradoxes and contradictions
        layer.paradoxes = self._find_paradoxes(analyses)
        layer.contradictions = self._find_contradictions(analyses)
        
        # Identify chaos patterns
        layer.chaos_patterns = self._identify_chaos_patterns(text, analyses)
        
        # Extract emergent symbols
        layer.emergent_symbols = self._extract_emergent_symbols(analyses)
        
        # Calculate transformation potential
        layer.transformation_potential = self._calculate_transformation_potential(
            layer
        )
        
        return layer
    
    def _find_paradoxes(self, analyses: List[LanguageAnalysis]) -> List[Dict[str, Any]]:
        """Find paradoxical concepts across languages"""
        paradoxes = []
        
        # Look for concepts that have opposing meanings in different languages
        for i, analysis1 in enumerate(analyses):
            for j, analysis2 in enumerate(analyses[i+1:], i+1):
                # Compare semantic fields
                field1 = set(analysis1.semantic_field)
                field2 = set(analysis2.semantic_field)
                
                # Check for opposing concepts
                opposites = {
                    ('individual', 'collective'),
                    ('explicit', 'implicit'),
                    ('direct', 'indirect'),
                    ('formal', 'informal')
                }
                
                for opp1, opp2 in opposites:
                    if (opp1 in field1 and opp2 in field2) or \
                       (opp2 in field1 and opp1 in field2):
                        paradoxes.append({
                            'type': 'semantic_opposition',
                            'languages': [analysis1.language, analysis2.language],
                            'concepts': [opp1, opp2],
                            'description': f'{opp1} vs {opp2} perspective'
                        })
        
        return paradoxes
    
    def _find_contradictions(self, analyses: List[LanguageAnalysis]) -> List[Tuple[str, str]]:
        """Find contradictory interpretations"""
        contradictions = []
        
        # Simple implementation: look for opposing metaphors
        all_metaphors = []
        for analysis in analyses:
            all_metaphors.extend([(analysis.language, m) for m in analysis.metaphors])
        
        # Check for contradictory metaphors
        for i, (lang1, met1) in enumerate(all_metaphors):
            for lang2, met2 in all_metaphors[i+1:]:
                if self._are_contradictory(met1, met2):
                    contradictions.append((f"{lang1}: {met1}", f"{lang2}: {met2}"))
        
        return contradictions
    
    def _are_contradictory(self, metaphor1: str, metaphor2: str) -> bool:
        """Check if two metaphors are contradictory"""
        # Simplified check
        opposites = [
            ('up', 'down'), ('in', 'out'), ('open', 'closed'),
            ('light', 'dark'), ('fast', 'slow'), ('hard', 'soft')
        ]
        
        for opp1, opp2 in opposites:
            if (opp1 in metaphor1 and opp2 in metaphor2) or \
               (opp2 in metaphor1 and opp1 in metaphor2):
                return True
        
        return False
    
    def _identify_chaos_patterns(self, text: str, 
                                analyses: List[LanguageAnalysis]) -> List[str]:
        """Identify chaotic or emergent patterns"""
        patterns = []
        
        # Check for recursive structures
        if text.count(text.split()[0]) > 2:
            patterns.append('recursive_emphasis')
        
        # Check for high conceptual diversity
        all_concepts = set()
        for analysis in analyses:
            all_concepts.update(analysis.key_concepts)
        
        if len(all_concepts) > len(analyses) * 3:
            patterns.append('high_conceptual_divergence')
        
        # Check for transformation indicators
        transform_words = ['become', 'transform', 'evolve', 'emerge']
        if any(word in text.lower() for word in transform_words):
            patterns.append('transformation_potential')
        
        return patterns
    
    def _extract_emergent_symbols(self, analyses: List[LanguageAnalysis]) -> List[str]:
        """Extract symbols that emerge from cross-linguistic analysis"""
        symbols = []
        
        # Find concepts that appear in multiple languages with different forms
        concept_variations = {}
        for analysis in analyses:
            for concept in analysis.key_concepts:
                key = concept.lower()[:4]  # Simple stemming
                if key not in concept_variations:
                    concept_variations[key] = []
                concept_variations[key].append((analysis.language, concept))
        
        # Symbols emerge from concepts with multiple variations
        for key, variations in concept_variations.items():
            if len(variations) >= 3:
                symbols.append(f"emergent_{key}")
        
        return symbols
    
    def _calculate_transformation_potential(self, layer: SymbolicLayer) -> float:
        """Calculate the transformation potential of the symbolic layer"""
        factors = [
            len(layer.archetypes) * 0.1,
            len(layer.paradoxes) * 0.2,
            len(layer.chaos_patterns) * 0.3,
            len(layer.emergent_symbols) * 0.15,
            len(layer.contradictions) * 0.25
        ]
        
        # Normalize to 0-1 range
        potential = min(sum(factors), 1.0)
        return potential
    
    def _synthesize_insights(self, root: LanguageAnalysis,
                           unrelated: List[LanguageAnalysis],
                           symbolic: SymbolicLayer) -> MultiLanguageInsight:
        """Synthesize all analyses into final insights"""
        insight = MultiLanguageInsight(
            root_analysis=root,
            unrelated_analyses=unrelated,
            symbolic_layer=symbolic
        )
        
        # Extract cross-linguistic patterns
        insight.cross_linguistic_patterns = self._extract_cross_patterns(
            [root] + unrelated
        )
        
        # Identify unique perspectives
        insight.unique_perspectives = self._identify_unique_perspectives(
            [root] + unrelated
        )
        
        # Find convergent and divergent meanings
        insight.convergent_meanings, insight.divergent_meanings = \
            self._find_meaning_convergence([root] + unrelated)
        
        # Calculate insight score
        insight.insight_score = self._calculate_insight_score(insight)
        
        return insight
    
    def _extract_cross_patterns(self, analyses: List[LanguageAnalysis]) -> Dict[str, List[str]]:
        """Extract patterns that appear across languages"""
        patterns = {
            'shared_concepts': [],
            'unique_expressions': [],
            'grammatical_convergence': [],
            'metaphorical_bridges': []
        }
        
        # Find shared concepts
        concept_sets = [set(a.key_concepts) for a in analyses]
        if concept_sets:
            shared = concept_sets[0]
            for s in concept_sets[1:]:
                shared = shared.intersection(s)
            patterns['shared_concepts'] = list(shared)
        
        # Collect unique expressions
        for analysis in analyses:
            patterns['unique_expressions'].extend(
                [f"{analysis.language}: {expr}" for expr in analysis.unique_expressions]
            )
        
        # Find grammatical convergence
        word_orders = [a.cultural_context.get('word_order') for a in analyses]
        if word_orders:
            most_common = max(set(word_orders), key=word_orders.count)
            if word_orders.count(most_common) > 1:
                patterns['grammatical_convergence'].append(f"word_order: {most_common}")
        
        return patterns
    
    def _identify_unique_perspectives(self, analyses: List[LanguageAnalysis]) -> Dict[str, Any]:
        """Identify unique perspectives from each language"""
        perspectives = {}
        
        for analysis in analyses:
            lang = analysis.language
            perspectives[lang] = {
                'cultural_features': analysis.cultural_context.get('conceptual_features', []),
                'unique_concepts': [c for c in analysis.key_concepts 
                                  if not any(c in a.key_concepts 
                                           for a in analyses if a != analysis)],
                'perspective': analysis.cultural_context.get('unique_perspective', '')
            }
        
        return perspectives
    
    def _find_meaning_convergence(self, analyses: List[LanguageAnalysis]) -> Tuple[List[str], List[str]]:
        """Find convergent and divergent meanings across languages"""
        convergent = []
        divergent = []
        
        # Compare semantic fields
        semantic_fields = [set(a.semantic_field) for a in analyses]
        
        if semantic_fields:
            # Convergent: appear in most languages
            all_fields = set().union(*semantic_fields)
            for field in all_fields:
                count = sum(1 for s in semantic_fields if field in s)
                if count >= len(analyses) * 0.7:
                    convergent.append(field)
                elif count == 1:
                    divergent.append(field)
        
        return convergent, divergent
    
    def _calculate_insight_score(self, insight: MultiLanguageInsight) -> float:
        """Calculate overall insight score"""
        factors = [
            len(insight.cross_linguistic_patterns.get('shared_concepts', [])) * 0.1,
            len(insight.unique_perspectives) * 0.15,
            len(insight.convergent_meanings) * 0.1,
            len(insight.divergent_meanings) * 0.2,
            insight.symbolic_layer.transformation_potential * 0.45
        ]
        
        return min(sum(factors), 1.0)
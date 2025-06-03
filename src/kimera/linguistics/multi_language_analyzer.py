"""
Multi-Language Analyzer for Kimera SWM
======================================

Integrates real translation services into Kimera's analysis pipeline,
enabling true cross-linguistic pattern detection and resonance finding.
"""

import asyncio
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import logging

from ..geoid import Geoid
from ..resonance import find_resonance
from ..pattern_extraction import extract_patterns, enhanced_resonance
from .translation_service import create_translation_service, TranslationResult
from .translation_config import get_config

logger = logging.getLogger(__name__)


@dataclass
class MultiLingualAnalysis:
    """Results of multi-lingual analysis."""
    original_text: str
    original_language: str
    translations: Dict[str, TranslationResult]
    patterns: Dict[str, List[Any]]  # Patterns per language
    geoids: Dict[str, Geoid]  # Geoids per language
    cross_lingual_resonances: List[Dict[str, Any]]


class MultiLanguageAnalyzer:
    """
    Analyzes text across multiple languages to find deep patterns
    and resonances that transcend linguistic boundaries.
    """
    
    def __init__(self, translation_service=None, target_languages=None):
        """
        Initialize multi-language analyzer.
        
        Args:
            translation_service: Translation service to use (or auto-create)
            target_languages: List of languages to analyze (default: major languages)
        """
        # Get configuration
        self.config = get_config()
        
        # Set up translation service
        if translation_service is None:
            service_type = self.config.get_default_service()
            if service_type == "mock" and "google" in self.config.get_available_services():
                service_type = "google"  # Prefer real service if available
            
            self.translator = create_translation_service(
                service_type=service_type,
                enable_cache=True
            )
        else:
            self.translator = translation_service
        
        # Set target languages
        if target_languages is None:
            # Default to major languages that are well-supported
            self.target_languages = ["en", "es", "fr", "de", "zh", "ja", "ar"]
        else:
            self.target_languages = target_languages
        
        logger.info(f"Initialized MultiLanguageAnalyzer with {len(self.target_languages)} languages")
    
    async def analyze(self, text: str, source_language: Optional[str] = None) -> MultiLingualAnalysis:
        """
        Perform comprehensive multi-lingual analysis.
        
        Args:
            text: Text to analyze
            source_language: Source language (auto-detect if None)
            
        Returns:
            MultiLingualAnalysis with translations, patterns, and resonances
        """
        # Detect source language if not provided
        if not source_language:
            source_language, _ = await self.translator.detect_language(text)
            if source_language == "unknown":
                source_language = "en"  # Default fallback
        
        # Translate to all target languages
        translations = await self._translate_to_all(text, source_language)
        
        # Extract patterns from each translation
        patterns = self._extract_patterns_all(text, translations)
        
        # Create geoids for each language version
        geoids = self._create_geoids_all(text, translations)
        
        # Find cross-lingual resonances
        resonances = self._find_cross_lingual_resonances(geoids, patterns)
        
        return MultiLingualAnalysis(
            original_text=text,
            original_language=source_language,
            translations=translations,
            patterns=patterns,
            geoids=geoids,
            cross_lingual_resonances=resonances
        )
    
    async def _translate_to_all(self, text: str, source_language: str) -> Dict[str, TranslationResult]:
        """Translate text to all target languages."""
        translations = {source_language: TranslationResult(
            source_text=text,
            translated_text=text,
            source_language=source_language,
            target_language=source_language,
            confidence=1.0
        )}
        
        # Prepare translation tasks
        tasks = []
        for lang in self.target_languages:
            if lang != source_language:
                tasks.append((lang, self.translator.translate(text, lang, source_language)))
        
        # Execute translations concurrently
        if tasks:
            results = await asyncio.gather(*[task[1] for task in tasks], return_exceptions=True)
            
            for (lang, _), result in zip(tasks, results):
                if isinstance(result, Exception):
                    logger.error(f"Translation to {lang} failed: {result}")
                    # Create fallback result
                    translations[lang] = TranslationResult(
                        source_text=text,
                        translated_text=f"[{lang}]{text}",
                        source_language=source_language,
                        target_language=lang,
                        confidence=0.0
                    )
                else:
                    translations[lang] = result
        
        return translations
    
    def _extract_patterns_all(self, original_text: str, translations: Dict[str, TranslationResult]) -> Dict[str, List[Any]]:
        """Extract patterns from all translations."""
        patterns = {}
        
        # Extract patterns from original
        patterns[translations[list(translations.keys())[0]].source_language] = extract_patterns(original_text)
        
        # Extract patterns from each translation
        for lang, result in translations.items():
            if result.confidence > 0.5:  # Only use confident translations
                patterns[lang] = extract_patterns(result.translated_text)
        
        return patterns
    
    def _create_geoids_all(self, original_text: str, translations: Dict[str, TranslationResult]) -> Dict[str, Geoid]:
        """Create geoids for each language version."""
        geoids = {}
        
        for lang, result in translations.items():
            if result.confidence > 0.5:
                geoid = Geoid(result.translated_text)
                geoid.metadata["language"] = lang
                geoid.metadata["translation_confidence"] = result.confidence
                geoids[lang] = geoid
        
        return geoids
    
    def _find_cross_lingual_resonances(self, geoids: Dict[str, Geoid], patterns: Dict[str, List[Any]]) -> List[Dict[str, Any]]:
        """Find resonances across different language versions."""
        resonances = []
        languages = list(geoids.keys())
        
        # Compare each pair of languages
        for i in range(len(languages)):
            for j in range(i + 1, len(languages)):
                lang1, lang2 = languages[i], languages[j]
                
                # Calculate semantic resonance
                semantic_score = find_resonance(
                    geoids[lang1].content,
                    geoids[lang2].content
                )
                
                # Calculate pattern-based resonance
                pattern_score = 0.0
                if lang1 in patterns and lang2 in patterns:
                    pattern_score = enhanced_resonance(
                        geoids[lang1].content,
                        geoids[lang2].content,
                        semantic_score
                    )
                
                # Record significant resonances
                if semantic_score > 0.3 or pattern_score > 0.4:
                    resonances.append({
                        "languages": (lang1, lang2),
                        "semantic_score": semantic_score,
                        "pattern_score": pattern_score,
                        "combined_score": (semantic_score + pattern_score) / 2,
                        "patterns_found": {
                            lang1: len(patterns.get(lang1, [])),
                            lang2: len(patterns.get(lang2, []))
                        }
                    })
        
        # Sort by combined score
        resonances.sort(key=lambda x: x["combined_score"], reverse=True)
        
        return resonances
    
    async def find_multilingual_insights(self, concepts: List[str], threshold: float = 0.5) -> List[Dict[str, Any]]:
        """
        Find insights by analyzing concepts across multiple languages.
        
        Args:
            concepts: List of concepts to analyze
            threshold: Minimum resonance threshold
            
        Returns:
            List of cross-linguistic insights
        """
        insights = []
        
        # Analyze each concept
        for concept in concepts:
            analysis = await self.analyze(concept)
            
            # Look for interesting patterns
            if analysis.cross_lingual_resonances:
                top_resonance = analysis.cross_lingual_resonances[0]
                
                if top_resonance["combined_score"] > threshold:
                    # Extract unique patterns across languages
                    unique_patterns = set()
                    for lang, patterns in analysis.patterns.items():
                        for pattern in patterns:
                            if hasattr(pattern, 'action'):
                                unique_patterns.add(pattern.action)
                    
                    insights.append({
                        "concept": concept,
                        "languages_analyzed": len(analysis.translations),
                        "top_resonance": top_resonance,
                        "unique_patterns": list(unique_patterns),
                        "linguistic_invariant": self._find_invariant_meaning(analysis)
                    })
        
        return insights
    
    def _find_invariant_meaning(self, analysis: MultiLingualAnalysis) -> Optional[str]:
        """
        Find meaning that remains constant across translations.
        
        This identifies the core semantic content that transcends
        linguistic boundaries.
        """
        # Look for patterns that appear in multiple languages
        pattern_counts = {}
        
        for lang, patterns in analysis.patterns.items():
            for pattern in patterns:
                if hasattr(pattern, 'action') and pattern.action:
                    key = pattern.action
                    pattern_counts[key] = pattern_counts.get(key, 0) + 1
        
        # Find most common pattern
        if pattern_counts:
            most_common = max(pattern_counts.items(), key=lambda x: x[1])
            if most_common[1] >= len(analysis.patterns) * 0.5:  # Appears in 50%+ of languages
                return f"Core action: {most_common[0]}"
        
        return None
    
    async def translate_and_analyze_batch(self, texts: List[str], source_language: Optional[str] = None) -> List[MultiLingualAnalysis]:
        """
        Analyze multiple texts efficiently.
        
        Args:
            texts: List of texts to analyze
            source_language: Source language for all texts
            
        Returns:
            List of analysis results
        """
        # Create analysis tasks
        tasks = []
        for text in texts:
            tasks.append(self.analyze(text, source_language))
        
        # Execute concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out errors
        analyses = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Analysis failed for text {i}: {result}")
            else:
                analyses.append(result)
        
        return analyses


# Convenience functions for integration
async def analyze_multilingual(text: str, languages: Optional[List[str]] = None) -> MultiLingualAnalysis:
    """
    Quick function to analyze text across multiple languages.
    
    Args:
        text: Text to analyze
        languages: Target languages (uses defaults if None)
        
    Returns:
        Multi-lingual analysis results
    """
    analyzer = MultiLanguageAnalyzer(target_languages=languages)
    return await analyzer.analyze(text)


async def find_linguistic_invariants(concepts: List[str]) -> List[Dict[str, Any]]:
    """
    Find patterns that remain constant across languages.
    
    Args:
        concepts: List of concepts to analyze
        
    Returns:
        List of linguistic invariants found
    """
    analyzer = MultiLanguageAnalyzer()
    insights = await analyzer.find_multilingual_insights(concepts)
    
    # Filter for strong invariants
    invariants = []
    for insight in insights:
        if insight.get("linguistic_invariant"):
            invariants.append({
                "concept": insight["concept"],
                "invariant": insight["linguistic_invariant"],
                "confidence": insight["top_resonance"]["combined_score"],
                "languages": insight["languages_analyzed"]
            })
    
    return invariants
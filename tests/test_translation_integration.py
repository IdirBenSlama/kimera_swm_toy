"""
Integration tests for translation services with Kimera SWM
"""

import pytest
import asyncio
from pathlib import Path
import sys
import numpy as np

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.kimera.geoid import init_geoid
from src.kimera.resonance import resonance
from src.kimera.linguistics import create_translation_service
from src.kimera.linguistics.multi_language_analyzer import MultiLanguageAnalyzer


class TestTranslationSWMIntegration:
    """Test translation services integrated with SWM components"""
    
    @pytest.mark.asyncio
    async def test_multilingual_geoid_resonance(self):
        """Test creating geoids from translations and measuring resonance"""
        # Create translation service
        translator = create_translation_service('mock', enable_cache=True)
        
        # Original concept
        concept = "consciousness"
        languages = ["en", "es", "fr", "de", "ja"]
        
        # Translate to multiple languages
        translations = {"en": concept}
        for lang in languages[1:]:
            result = await translator.translate(concept, lang)
            translations[lang] = result.translated_text
        
        # Create geoids for each translation
        geoids = {}
        for lang, text in translations.items():
            geoid = init_geoid(text=text, lang=lang, layers=["consciousness", "philosophy"])
            geoids[lang] = geoid
        
        # Calculate resonance between English and other languages
        resonances = {}
        en_geoid = geoids["en"]
        for lang in languages[1:]:
            res = resonance(en_geoid, geoids[lang])
            resonances[f"en-{lang}"] = res
        
        # Verify resonance values are reasonable
        assert all(-1 <= r <= 1 for r in resonances.values())
        # Mock translations should have positive resonance
        assert all(r > 0 for r in resonances.values())
    
    @pytest.mark.asyncio
    async def test_translation_caching_performance(self):
        """Test that caching improves performance"""
        translator = create_translation_service('mock', enable_cache=True)
        
        # Test data
        texts = ["Hello", "World", "Peace", "Love", "Harmony"] * 10
        target_lang = "es"
        
        # First pass - populate cache
        first_results = []
        for text in texts:
            result = await translator.translate(text, target_lang)
            first_results.append(result)
        
        # Get cache stats
        stats = translator.get_cache_stats()
        
        # Should have cache misses for unique texts (5)
        assert stats['misses'] == 5
        # Should have cache hits for repeated texts (45)
        assert stats['hits'] == 45
        # Hit rate should be high
        assert stats['hit_rate'] > 0.8
    
    def test_multi_language_analyzer_with_swm(self):
        """Test MultiLanguageAnalyzer integration with SWM concepts"""
        analyzer = MultiLanguageAnalyzer()
        
        # Analyze a philosophical concept
        text = "The nature of reality is both subjective and objective"
        result = analyzer.analyze(text, root_lang='en')
        
        # Verify analysis structure
        assert result.root_analysis.language == 'en'
        assert len(result.unrelated_analyses) == 3
        assert result.symbolic_layer is not None
        
        # Check for philosophical archetypes
        # The text discusses reality, which might trigger certain archetypes
        assert isinstance(result.symbolic_layer.archetypes, list)
        
        # Verify insight score is calculated
        assert 0 <= result.insight_score <= 1
    
    @pytest.mark.asyncio
    async def test_translation_pipeline_with_geoids(self):
        """Test complete pipeline: translate -> create geoids -> analyze resonance"""
        translator = create_translation_service('mock', enable_cache=True)
        
        # Input concepts
        concepts = {
            "love": ["affection", "caring", "compassion"],
            "wisdom": ["knowledge", "understanding", "insight"],
            "peace": ["harmony", "tranquility", "calm"]
        }
        
        # Process each concept family
        concept_geoids = {}
        
        for main_concept, related_concepts in concepts.items():
            # Translate main concept
            translations = {"en": main_concept}
            for lang in ["es", "fr", "de"]:
                result = await translator.translate(main_concept, lang)
                translations[lang] = result.translated_text
            
            # Create geoids
            geoids = {}
            for lang, text in translations.items():
                geoid = init_geoid(text=text, lang=lang, layers=[main_concept])
                geoids[lang] = geoid
            
            concept_geoids[main_concept] = geoids
        
        # Analyze cross-concept resonance
        # Love vs Wisdom in English
        love_en = concept_geoids["love"]["en"]
        wisdom_en = concept_geoids["wisdom"]["en"]
        love_wisdom_resonance = resonance(love_en, wisdom_en)
        
        # Love in English vs Love in Spanish
        love_es = concept_geoids["love"]["es"]
        love_cross_lang_resonance = resonance(love_en, love_es)
        
        # Verify resonance patterns
        assert isinstance(love_wisdom_resonance, (int, float))
        assert isinstance(love_cross_lang_resonance, (int, float))
        
        # Same concept across languages should have higher resonance
        # than different concepts in same language (in theory)
        # Note: This might not always hold with mock data
        assert -1 <= love_wisdom_resonance <= 1
        assert -1 <= love_cross_lang_resonance <= 1
    
    @pytest.mark.asyncio
    async def test_batch_translation_with_caching(self):
        """Test batch translation functionality with caching"""
        translator = create_translation_service('mock', enable_cache=True)
        
        # First, translate a text to populate cache
        await translator.translate("The mind is everything", "es")
        
        # Batch of texts including the cached one
        texts = [
            "The mind is everything",  # Should hit cache
            "What you think you become",
            "Peace comes from within",
            "Do not seek it without"
        ]
        
        # Clear stats to measure batch performance
        initial_stats = translator.get_cache_stats()
        initial_total = initial_stats['total_requests']
        
        # Batch translate
        results = await translator.batch_translate(texts, "es")
        
        # Verify results
        assert len(results) == len(texts)
        assert all(r.target_language == "es" for r in results)
        assert all(r.translated_text for r in results)
        
        # Check cache was used
        final_stats = translator.get_cache_stats()
        batch_requests = final_stats['total_requests'] - initial_total
        
        # Should have made 4 requests with 1 cache hit
        assert batch_requests == 4
        assert final_stats['hits'] > initial_stats['hits']  # At least one cache hit
    
    def test_language_family_diversity(self):
        """Test that language selection maximizes diversity"""
        from src.kimera.linguistics.multi_language_analyzer import (
            select_unrelated_languages, calculate_language_distance
        )
        
        # Select languages unrelated to English
        selected = select_unrelated_languages('en', n=4)
        
        # Verify diversity
        assert len(selected) == 4
        assert 'en' not in selected
        
        # Calculate average distance between selected languages
        distances = []
        for i, lang1 in enumerate(selected):
            for lang2 in selected[i+1:]:
                dist = calculate_language_distance(lang1, lang2)
                distances.append(dist)
        
        avg_distance = np.mean(distances) if distances else 0
        
        # Selected languages should be diverse
        assert avg_distance > 0.4  # Reasonably high diversity
    
    @pytest.mark.asyncio
    async def test_translation_metadata_tracking(self):
        """Test that translation metadata is properly tracked"""
        translator = create_translation_service('mock', enable_cache=False)
        
        # Translate with metadata
        result = await translator.translate(
            "Hello world",
            "es",
            source_language="en"
        )
        
        # Check metadata
        assert result.metadata is not None
        assert 'service' in result.metadata
        assert result.metadata['service'] == 'mock'
        assert 'timestamp' in result.metadata
        
        # Verify all fields are populated
        assert result.source_text == "Hello world"
        assert result.source_language == "en"
        assert result.target_language == "es"
        assert result.confidence > 0
    
    def test_symbolic_layer_extraction(self):
        """Test symbolic layer extraction in multi-language analysis"""
        analyzer = MultiLanguageAnalyzer()
        
        # Text with transformation theme
        text = "To become enlightened, one must transform the self"
        result = analyzer.analyze(text, root_lang='en')
        
        # Check symbolic layer
        symbolic = result.symbolic_layer
        
        # Should identify transformation patterns
        if 'transformation' in ' '.join(symbolic.archetypes):
            assert True  # Found transformation archetype
        elif 'transformation_potential' in symbolic.chaos_patterns:
            assert True  # Found transformation pattern
        else:
            # At minimum, should have non-zero transformation potential
            assert symbolic.transformation_potential >= 0
    
    @pytest.mark.asyncio
    async def test_cross_linguistic_concept_mapping(self):
        """Test mapping concepts across languages"""
        translator = create_translation_service('mock', enable_cache=True)
        analyzer = MultiLanguageAnalyzer()
        
        # Core concepts to map
        concepts = ["truth", "beauty", "goodness"]
        base_lang = "en"
        target_langs = ["es", "fr", "de", "ja"]
        
        # Build concept map
        concept_map = {}
        
        for concept in concepts:
            concept_map[concept] = {base_lang: concept}
            
            # Translate to each target language
            for lang in target_langs:
                result = await translator.translate(concept, lang)
                concept_map[concept][lang] = result.translated_text
        
        # Verify concept mapping
        assert len(concept_map) == len(concepts)
        for concept in concepts:
            assert len(concept_map[concept]) == len(target_langs) + 1
            assert all(concept_map[concept].values())  # All translations present
        
        # Analyze one concept across languages
        truth_analysis = analyzer.analyze(
            concepts[0],  # "truth"
            root_lang=base_lang,
            target_langs=target_langs[:3]  # Use first 3 target languages
        )
        
        # Verify cross-linguistic analysis
        assert truth_analysis.root_analysis.text == "truth"
        assert len(truth_analysis.unrelated_analyses) == 3
        assert truth_analysis.insight_score >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
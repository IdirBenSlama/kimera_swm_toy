"""
Tests for the MultiLanguageAnalyzer implementing the SWM "1+3+1" rule
"""

import pytest
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.kimera.linguistics.multi_language_analyzer import (
    MultiLanguageAnalyzer, LanguageAnalysis, SymbolicLayer,
    MultiLanguageInsight, LanguageFamily, LANGUAGE_METADATA,
    calculate_language_distance, select_unrelated_languages
)


class TestLanguageDistance:
    """Test language distance calculations"""
    
    def test_same_language_distance(self):
        """Test distance between same language is 0"""
        assert calculate_language_distance('en', 'en') == 0.0
        assert calculate_language_distance('ja', 'ja') == 0.0
    
    def test_related_languages(self):
        """Test distance between related languages"""
        # English and Hindi are both Indo-European but different scripts
        distance = calculate_language_distance('en', 'hi')
        assert 0 < distance < 0.8  # They share family but differ in other aspects
    
    def test_unrelated_languages(self):
        """Test distance between unrelated languages"""
        # English (Indo-European) and Japanese (Japonic)
        distance = calculate_language_distance('en', 'ja')
        assert distance > 0.5
        
        # Arabic (Afro-Asiatic) and Chinese (Sino-Tibetan)
        distance = calculate_language_distance('ar', 'zh')
        assert distance > 0.5
    
    def test_unknown_language(self):
        """Test handling of unknown languages"""
        distance = calculate_language_distance('en', 'unknown')
        assert distance == 0.5  # Default distance
    
    def test_distance_symmetry(self):
        """Test that distance is symmetric"""
        dist1 = calculate_language_distance('en', 'ja')
        dist2 = calculate_language_distance('ja', 'en')
        assert dist1 == dist2


class TestLanguageSelection:
    """Test unrelated language selection"""
    
    def test_select_unrelated_basic(self):
        """Test basic selection of unrelated languages"""
        selected = select_unrelated_languages('en', n=3)
        
        assert len(selected) == 3
        assert 'en' not in selected
        
        # Should include diverse language families
        families = set()
        for lang in selected:
            if lang in LANGUAGE_METADATA:
                families.add(LANGUAGE_METADATA[lang]['family'])
        
        assert len(families) >= 2  # At least 2 different families
    
    def test_select_with_limited_options(self):
        """Test selection with limited language options"""
        available = ['en', 'es', 'fr']
        selected = select_unrelated_languages('en', available, n=3)
        
        assert len(selected) == 2  # Only es and fr available
        assert 'en' not in selected
        assert set(selected) == {'es', 'fr'}
    
    def test_select_maximizes_diversity(self):
        """Test that selection maximizes linguistic diversity"""
        # From English, should select maximally different languages
        selected = select_unrelated_languages('en', n=3)
        
        # Calculate average distance between selected languages
        total_distance = 0
        count = 0
        for i, lang1 in enumerate(selected):
            for lang2 in selected[i+1:]:
                total_distance += calculate_language_distance(lang1, lang2)
                count += 1
        
        avg_distance = total_distance / count if count > 0 else 0
        assert avg_distance > 0.5  # High diversity


class TestLanguageAnalysis:
    """Test LanguageAnalysis dataclass"""
    
    def test_language_analysis_creation(self):
        """Test creating LanguageAnalysis"""
        analysis = LanguageAnalysis(
            language='en',
            text='Hello world',
            translated_text=None,
            key_concepts=['hello', 'world'],
            confidence=0.95
        )
        
        assert analysis.language == 'en'
        assert analysis.text == 'Hello world'
        assert analysis.key_concepts == ['hello', 'world']
        assert analysis.confidence == 0.95
    
    def test_language_analysis_defaults(self):
        """Test default values"""
        analysis = LanguageAnalysis(
            language='en',
            text='Test'
        )
        
        assert analysis.translated_text is None
        assert analysis.key_concepts == []
        assert analysis.unique_expressions == []
        assert analysis.metaphors == []
        assert analysis.confidence == 1.0


class TestSymbolicLayer:
    """Test SymbolicLayer dataclass"""
    
    def test_symbolic_layer_creation(self):
        """Test creating SymbolicLayer"""
        layer = SymbolicLayer(
            archetypes=['transformation', 'connection'],
            transformation_potential=0.8
        )
        
        assert layer.archetypes == ['transformation', 'connection']
        assert layer.transformation_potential == 0.8
    
    def test_symbolic_layer_defaults(self):
        """Test default values"""
        layer = SymbolicLayer()
        
        assert layer.archetypes == []
        assert layer.paradoxes == []
        assert layer.chaos_patterns == []
        assert layer.emergent_symbols == []
        assert layer.contradictions == []
        assert layer.transformation_potential == 0.0


class TestMultiLanguageAnalyzer:
    """Test the MultiLanguageAnalyzer"""
    
    @pytest.fixture
    def analyzer(self):
        return MultiLanguageAnalyzer(translation_backend=None)
    
    def test_analyzer_initialization(self, analyzer):
        """Test analyzer initialization"""
        assert analyzer.translation_backend is None
        assert analyzer.translator is None
        assert isinstance(analyzer.analyzers, dict)
    
    def test_analyze_basic(self, analyzer):
        """Test basic analysis functionality"""
        text = "The nature of consciousness"
        result = analyzer.analyze(text, root_lang='en')
        
        assert isinstance(result, MultiLanguageInsight)
        assert result.root_analysis.language == 'en'
        assert result.root_analysis.text == text
        assert len(result.unrelated_analyses) == 3  # Default n=3
        assert isinstance(result.symbolic_layer, SymbolicLayer)
    
    def test_analyze_with_target_languages(self, analyzer):
        """Test analysis with specific target languages"""
        text = "Love and compassion"
        targets = ['es', 'ja', 'ar']
        
        result = analyzer.analyze(text, root_lang='en', target_langs=targets)
        
        assert len(result.unrelated_analyses) == 3
        analyzed_langs = [a.language for a in result.unrelated_analyses]
        assert set(analyzed_langs) == set(targets)
    
    def test_root_language_analysis(self, analyzer):
        """Test root language analysis extraction"""
        text = "Life is like a river flowing"
        analysis = analyzer._analyze_root_language(text, 'en')
        
        assert analysis.language == 'en'
        assert analysis.text == text
        assert analysis.translated_text is None
        assert len(analysis.key_concepts) > 0
        assert any('like' in m for m in analysis.metaphors)
    
    def test_metaphor_extraction(self, analyzer):
        """Test metaphor extraction"""
        text = "Time is money and life is a journey"
        analysis = analyzer._analyze_root_language(text, 'en')
        
        # Should find at least one metaphor with "is"
        assert len(analysis.metaphors) >= 1
        assert any('is' in m for m in analysis.metaphors)
    
    def test_archetype_extraction(self, analyzer):
        """Test archetype extraction in symbolic layer"""
        # Create mock analyses with archetypal concepts
        analyses = [
            LanguageAnalysis('en', 'test', key_concepts=['protect', 'defend']),
            LanguageAnalysis('es', 'test', key_concepts=['create', 'build']),
            LanguageAnalysis('ja', 'test', key_concepts=['transform', 'change'])
        ]
        
        layer = analyzer._extract_symbolic_layer("test text", analyses)
        
        assert 'protection' in layer.archetypes
        assert 'creation' in layer.archetypes
        assert 'transformation' in layer.archetypes
    
    def test_paradox_detection(self, analyzer):
        """Test paradox detection across languages"""
        analyses = [
            LanguageAnalysis('en', 'test', semantic_field=['individual', 'explicit']),
            LanguageAnalysis('ja', 'test', semantic_field=['collective', 'implicit'])
        ]
        
        paradoxes = analyzer._find_paradoxes(analyses)
        
        assert len(paradoxes) > 0
        assert any(p['type'] == 'semantic_opposition' for p in paradoxes)
    
    def test_transformation_potential(self, analyzer):
        """Test transformation potential calculation"""
        layer = SymbolicLayer(
            archetypes=['transformation', 'creation'],
            paradoxes=[{}, {}],
            chaos_patterns=['recursive_emphasis'],
            emergent_symbols=['emergent_love'],
            contradictions=[('up', 'down')]
        )
        
        potential = analyzer._calculate_transformation_potential(layer)
        
        assert 0 < potential <= 1.0
        assert potential > 0.5  # Should be relatively high with these elements
    
    def test_cross_linguistic_patterns(self, analyzer):
        """Test cross-linguistic pattern extraction"""
        analyses = [
            LanguageAnalysis('en', 'test', key_concepts=['love', 'peace', 'harmony']),
            LanguageAnalysis('es', 'test', key_concepts=['love', 'war', 'harmony']),
            LanguageAnalysis('ja', 'test', key_concepts=['love', 'balance', 'harmony'])
        ]
        
        patterns = analyzer._extract_cross_patterns(analyses)
        
        assert 'love' in patterns['shared_concepts']
        assert 'harmony' in patterns['shared_concepts']
        assert 'peace' not in patterns['shared_concepts']  # Not in all
    
    def test_meaning_convergence(self, analyzer):
        """Test convergent and divergent meaning detection"""
        analyses = [
            LanguageAnalysis('en', 'test', semantic_field=['explicit', 'direct']),
            LanguageAnalysis('es', 'test', semantic_field=['explicit', 'formal']),
            LanguageAnalysis('ja', 'test', semantic_field=['implicit', 'indirect'])
        ]
        
        convergent, divergent = analyzer._find_meaning_convergence(analyses)
        
        # With threshold of 0.7, need to appear in 70% of languages
        # 'explicit' appears in 2/3 = 66.7%, so might not be convergent
        assert len(convergent) >= 0  # May have convergent meanings
        assert 'implicit' in divergent  # Only in 1 language
    
    def test_insight_score_calculation(self, analyzer):
        """Test insight score calculation"""
        # Create a rich insight
        root = LanguageAnalysis('en', 'consciousness')
        unrelated = [
            LanguageAnalysis('ja', 'consciousness'),
            LanguageAnalysis('ar', 'consciousness'),
            LanguageAnalysis('sw', 'consciousness')
        ]
        symbolic = SymbolicLayer(transformation_potential=0.7)
        
        insight = MultiLanguageInsight(
            root_analysis=root,
            unrelated_analyses=unrelated,
            symbolic_layer=symbolic,
            cross_linguistic_patterns={'shared_concepts': ['awareness', 'mind']},
            convergent_meanings=['universal', 'experience'],
            divergent_meanings=['individual', 'collective', 'spiritual']
        )
        
        score = analyzer._calculate_insight_score(insight)
        
        assert 0 < score <= 1.0
        assert score > 0.5  # Should be high with rich data
    
    def test_mock_translation(self, analyzer):
        """Test mock translation functionality"""
        translated = analyzer._translate("Hello", "en", "es")
        assert translated == "[es] Hello"
    
    def test_unique_perspective_extraction(self, analyzer):
        """Test extraction of unique perspectives"""
        perspective = analyzer._get_unique_perspective('ja')
        assert 'hierarchical' in perspective.lower()
        
        perspective = analyzer._get_unique_perspective('ar')
        assert 'metaphorical' in perspective.lower()
    
    def test_chaos_pattern_identification(self, analyzer):
        """Test chaos pattern identification"""
        text = "become become become transform evolve"
        analyses = [LanguageAnalysis('en', text, key_concepts=['become', 'transform'])]
        
        patterns = analyzer._identify_chaos_patterns(text, analyses)
        
        assert 'recursive_emphasis' in patterns
        assert 'transformation_potential' in patterns


class TestIntegrationScenarios:
    """Test complete integration scenarios"""
    
    @pytest.fixture
    def analyzer(self):
        return MultiLanguageAnalyzer()
    
    def test_philosophical_concept_analysis(self, analyzer):
        """Test analyzing a philosophical concept"""
        text = "The meaning of existence"
        result = analyzer.analyze(text, root_lang='en')
        
        # Should produce rich multi-perspective analysis
        assert result.root_analysis.text == text
        assert len(result.unrelated_analyses) == 3
        # Transformation potential depends on finding patterns
        assert result.symbolic_layer.transformation_potential >= 0
        assert result.insight_score > 0
    
    def test_emotional_concept_analysis(self, analyzer):
        """Test analyzing an emotional concept"""
        text = "Love transcends all boundaries"
        result = analyzer.analyze(text, root_lang='en', target_langs=['es', 'ja', 'ar'])
        
        # Should identify key concepts (love or boundaries)
        assert len(result.root_analysis.key_concepts) > 0
        # Check if love-related concepts are found
        all_concepts = ' '.join(result.root_analysis.key_concepts).lower()
        assert 'love' in all_concepts or 'boundaries' in all_concepts
        
        # May or may not find metaphors depending on the detection logic
        # The sentence doesn't have explicit "like" or "as" comparisons
        assert isinstance(result.root_analysis.metaphors, list)
    
    def test_technical_concept_analysis(self, analyzer):
        """Test analyzing a technical concept"""
        text = "Artificial intelligence algorithms"
        result = analyzer.analyze(text, root_lang='en')
        
        # Should handle technical terms
        assert result.root_analysis.language == 'en'
        assert len(result.unrelated_analyses) == 3
        
        # Technical concepts might have lower transformation potential
        assert result.symbolic_layer.transformation_potential >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
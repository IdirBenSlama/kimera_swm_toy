"""
NLP module for advanced pattern extraction using spaCy.

This module provides comprehensive NLP pattern extraction capabilities including:
- Basic pattern extraction (entities, noun chunks)
- Advanced pattern matching using spaCy's Matcher
- Dependency-based pattern extraction
- Semantic similarity and clustering
- Pattern visualization
"""

import spacy
from typing import List, Dict, Any, Optional

# Import submodules
from .patterns import PatternExtractor
from .similarity import SemanticPatternExtractor
from .visualization import PatternVisualizer

# Load the default English model (can be parameterized later)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Model is not installed
    nlp = None


def ensure_spacy_model(model_name: str = "en_core_web_sm"):
    """Ensure a spaCy model is installed."""
    try:
        return spacy.load(model_name)
    except OSError:
        raise RuntimeError(
            f"spaCy model '{model_name}' is not installed. "
            f"Install it with: python -m spacy download {model_name}"
        )


def extract_patterns(text: str, patterns: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Extracts patterns from text using spaCy.
    If patterns is None, extracts named entities and noun chunks by default.
    If patterns is provided, it should be a list of spaCy pattern types (e.g., ['PERSON', 'ORG']).
    """
    model = ensure_spacy_model()
    doc = model(text)
    result = {}

    # Extract named entities
    if patterns is None or any(p.isupper() for p in (patterns or [])):
        ents = [
            {"text": ent.text, "label": ent.label_}
            for ent in doc.ents
            if patterns is None or ent.label_ in patterns
        ]
        result["entities"] = ents

    # Extract noun chunks
    if patterns is None or "NOUN_CHUNK" in (patterns or []):
        noun_chunks = [chunk.text for chunk in doc.noun_chunks]
        result["noun_chunks"] = noun_chunks

    # Add more pattern extraction as needed
    return result


def extract_comprehensive_patterns(text: str, 
                                 include_semantic: bool = False,
                                 semantic_model: str = "en_core_web_md") -> Dict[str, Any]:
    """
    Extract comprehensive patterns from text using all available extractors.
    
    Args:
        text: Input text to analyze
        include_semantic: Whether to include semantic patterns (requires medium/large model)
        semantic_model: Model to use for semantic analysis
    
    Returns:
        Dictionary containing all extracted patterns
    """
    # Basic patterns
    basic_patterns = extract_patterns(text)
    
    # Advanced patterns
    pattern_extractor = PatternExtractor()
    advanced_patterns = pattern_extractor.extract_all_patterns(text)
    
    # Combine results
    results = {
        "basic": basic_patterns,
        "advanced": advanced_patterns
    }
    
    # Semantic patterns (if requested and model supports it)
    if include_semantic:
        try:
            semantic_extractor = SemanticPatternExtractor(semantic_model)
            semantic_patterns = semantic_extractor.extract_all_semantic_patterns(text)
            results["semantic"] = semantic_patterns
        except (RuntimeError, ValueError) as e:
            results["semantic_error"] = str(e)
    
    return results


# Export main classes and functions
__all__ = [
    "extract_patterns",
    "extract_comprehensive_patterns",
    "PatternExtractor",
    "SemanticPatternExtractor", 
    "PatternVisualizer",
    "ensure_spacy_model"
]

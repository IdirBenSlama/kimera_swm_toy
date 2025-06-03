"""
Example script to demonstrate enhanced NLP pattern extraction with spaCy integration.
"""

import json
from . import (
    extract_patterns, 
    extract_comprehensive_patterns,
    PatternExtractor,
    PatternVisualizer
)

def demo_basic_extraction():
    """Demonstrate basic pattern extraction."""
    print("=" * 60)
    print("BASIC PATTERN EXTRACTION")
    print("=" * 60)
    
    sample_text = (
        "Apple is looking at buying U.K. startup for $1 billion. "
        "Elon Musk founded SpaceX in 2002. "
        "The innovative technology company developed artificial intelligence systems."
    )
    
    print("Sample text:")
    print(sample_text)
    print("\nExtracted patterns:")
    patterns = extract_patterns(sample_text)
    print(json.dumps(patterns, indent=2))

def demo_advanced_extraction():
    """Demonstrate advanced pattern extraction."""
    print("\n" + "=" * 60)
    print("ADVANCED PATTERN EXTRACTION")
    print("=" * 60)
    
    sample_text = (
        "The CEO announced that the company will invest heavily in research. "
        "Scientists discovered a new method for analyzing complex data. "
        "The research team collaborated with international partners on the project."
    )
    
    print("Sample text:")
    print(sample_text)
    
    # Create pattern extractor
    extractor = PatternExtractor()
    
    # Extract all patterns
    patterns = extractor.extract_all_patterns(sample_text)
    
    print("\nToken patterns:")
    print(json.dumps(patterns["token_patterns"], indent=2))
    
    print("\nSyntactic patterns:")
    print(json.dumps(patterns["syntactic_patterns"], indent=2))
    
    print("\nSemantic roles:")
    print(json.dumps(patterns["semantic_roles"], indent=2))

def demo_comprehensive_extraction():
    """Demonstrate comprehensive pattern extraction."""
    print("\n" + "=" * 60)
    print("COMPREHENSIVE PATTERN EXTRACTION")
    print("=" * 60)
    
    sample_text = (
        "Natural language processing enables computers to understand human language. "
        "Machine learning algorithms process vast amounts of textual data. "
        "Deep learning models have revolutionized language understanding tasks."
    )
    
    print("Sample text:")
    print(sample_text)
    
    # Extract comprehensive patterns (without semantic - requires larger model)
    patterns = extract_comprehensive_patterns(sample_text, include_semantic=False)
    
    print("\nComprehensive patterns extracted:")
    print(f"Basic patterns: {len(patterns['basic'].get('entities', []))} entities, "
          f"{len(patterns['basic'].get('noun_chunks', []))} noun chunks")
    print(f"Advanced patterns: {len(patterns['advanced']['token_patterns'])} token patterns, "
          f"{len(patterns['advanced']['semantic_roles'])} semantic roles")

def demo_visualization():
    """Demonstrate pattern visualization."""
    print("\n" + "=" * 60)
    print("PATTERN VISUALIZATION")
    print("=" * 60)
    
    sample_text = "The artificial intelligence system analyzed complex patterns in the data."
    
    # Create visualizer
    visualizer = PatternVisualizer()
    
    # Extract patterns for visualization
    extractor = PatternExtractor()
    patterns = extractor.extract_all_patterns(sample_text)
    
    # Generate report
    report_path = "pattern_analysis_report.html"
    visualizer.generate_pattern_report(sample_text, patterns, report_path)
    print(f"Pattern analysis report saved to: {report_path}")
    
    # Export patterns as JSON
    json_path = "extracted_patterns.json"
    visualizer.export_patterns_json(patterns, json_path)
    print(f"Patterns exported to: {json_path}")

if __name__ == "__main__":
    # Run all demos
    demo_basic_extraction()
    demo_advanced_extraction()
    demo_comprehensive_extraction()
    demo_visualization()
    
    print("\n" + "=" * 60)
    print("All demos completed!")
    print("=" * 60)

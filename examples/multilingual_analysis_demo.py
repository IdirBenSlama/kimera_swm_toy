"""
Multi-Language Analysis Demo
===========================

Demonstrates Kimera's ability to find patterns and resonances
across multiple languages, revealing deep structural similarities
that transcend linguistic boundaries.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from kimera.linguistics.multi_language_analyzer import (
    MultiLanguageAnalyzer, analyze_multilingual, find_linguistic_invariants
)


async def demo_basic_translation():
    """Demonstrate basic multi-language translation and analysis."""
    print("\n" + "="*70)
    print("DEMO 1: Basic Multi-Language Analysis")
    print("="*70)
    
    # Analyze a simple concept across languages
    text = "The heart pumps blood through the body"
    
    print(f"\nAnalyzing: '{text}'")
    print("-" * 50)
    
    # Use subset of languages for demo
    analyzer = MultiLanguageAnalyzer(target_languages=["en", "es", "fr", "de"])
    analysis = await analyzer.analyze(text)
    
    # Show translations
    print("\nTranslations:")
    for lang, result in analysis.translations.items():
        if lang != analysis.original_language:
            print(f"  {lang}: {result.translated_text}")
            print(f"       (confidence: {result.confidence:.2f})")
    
    # Show patterns found
    print("\nPatterns extracted per language:")
    for lang, patterns in analysis.patterns.items():
        print(f"  {lang}: {len(patterns)} patterns found")
        for pattern in patterns[:2]:  # Show first 2
            if hasattr(pattern, 'action'):
                print(f"    - Action: {pattern.action}")
    
    # Show cross-lingual resonances
    print("\nCross-lingual resonances:")
    for resonance in analysis.cross_lingual_resonances[:3]:
        lang1, lang2 = resonance["languages"]
        print(f"  {lang1} <-> {lang2}:")
        print(f"    Semantic: {resonance['semantic_score']:.3f}")
        print(f"    Pattern:  {resonance['pattern_score']:.3f}")
        print(f"    Combined: {resonance['combined_score']:.3f}")


async def demo_linguistic_invariants():
    """Find patterns that remain constant across languages."""
    print("\n" + "="*70)
    print("DEMO 2: Linguistic Invariants")
    print("="*70)
    print("Finding patterns that transcend linguistic boundaries...")
    print("-" * 50)
    
    # Concepts that should have strong invariant patterns
    concepts = [
        "Rivers flow to the ocean",
        "The sun rises in the east",
        "Plants grow towards light",
        "Fire produces heat",
        "Leaders guide their people"
    ]
    
    invariants = await find_linguistic_invariants(concepts)
    
    print("\nLinguistic invariants found:")
    for inv in invariants:
        print(f"\nConcept: '{inv['concept']}'")
        print(f"  Invariant: {inv['invariant']}")
        print(f"  Confidence: {inv['confidence']:.3f}")
        print(f"  Verified across {inv['languages']} languages")


async def demo_cross_domain_multilingual():
    """Demonstrate cross-domain insights enhanced by multi-language analysis."""
    print("\n" + "="*70)
    print("DEMO 3: Cross-Domain Multi-Lingual Insights")
    print("="*70)
    print("Finding deep patterns across domains AND languages...")
    print("-" * 50)
    
    # Analyze concepts from different domains
    analyzer = MultiLanguageAnalyzer(target_languages=["en", "es", "fr"])
    
    domain_concepts = {
        "Biology": "The heart circulates blood through vessels",
        "Technology": "The router distributes data through networks",
        "Sociology": "The leader spreads influence through communities",
        "Economics": "The bank circulates money through markets"
    }
    
    # Analyze each concept
    analyses = {}
    for domain, concept in domain_concepts.items():
        print(f"\nAnalyzing {domain}: '{concept}'")
        analyses[domain] = await analyzer.analyze(concept)
    
    # Find cross-domain patterns
    print("\n" + "-"*50)
    print("Cross-domain patterns (language-independent):")
    
    # Compare Biology vs Technology
    bio_patterns = set()
    tech_patterns = set()
    
    for lang, patterns in analyses["Biology"].patterns.items():
        for p in patterns:
            if hasattr(p, 'action'):
                bio_patterns.add(p.action)
    
    for lang, patterns in analyses["Technology"].patterns.items():
        for p in patterns:
            if hasattr(p, 'action'):
                tech_patterns.add(p.action)
    
    common_patterns = bio_patterns & tech_patterns
    if common_patterns:
        print(f"\nBiology <-> Technology:")
        print(f"  Common patterns: {common_patterns}")
        print("  Insight: Both involve circulation/distribution through networks")
    
    # Show how different languages reveal different aspects
    print("\n" + "-"*50)
    print("Language-specific insights:")
    
    for domain, analysis in analyses.items():
        print(f"\n{domain}:")
        unique_by_lang = {}
        for lang, patterns in analysis.patterns.items():
            unique_by_lang[lang] = len(patterns)
        
        richest_lang = max(unique_by_lang.items(), key=lambda x: x[1])
        print(f"  Richest pattern extraction: {richest_lang[0]} ({richest_lang[1]} patterns)")


async def demo_translation_quality():
    """Demonstrate how translation quality affects analysis."""
    print("\n" + "="*70)
    print("DEMO 4: Translation Quality Impact")
    print("="*70)
    
    # Complex philosophical concept
    text = "Knowledge emerges from the intersection of experience and reflection"
    
    print(f"\nAnalyzing complex concept: '{text}'")
    print("-" * 50)
    
    analysis = await analyze_multilingual(text, languages=["en", "es", "fr", "de", "ja"])
    
    # Show how confidence varies
    print("\nTranslation confidence by language:")
    for lang, result in analysis.translations.items():
        if lang != "en":
            print(f"  {lang}: {result.confidence:.3f}")
            if result.confidence < 0.8:
                print(f"       ⚠️  Low confidence may affect pattern extraction")
    
    # Show pattern preservation
    print("\nPattern preservation across translations:")
    source_patterns = len(analysis.patterns.get("en", []))
    for lang, patterns in analysis.patterns.items():
        if lang != "en":
            preservation = len(patterns) / source_patterns if source_patterns > 0 else 0
            print(f"  {lang}: {preservation:.1%} of original patterns preserved")


async def demo_practical_application():
    """Show practical application for research or content analysis."""
    print("\n" + "="*70)
    print("DEMO 5: Practical Application - Research Paper Analysis")
    print("="*70)
    
    # Simulate analyzing key findings from a research paper
    findings = [
        "Climate change accelerates ecosystem disruption",
        "Economic inequality increases social instability",
        "Quantum entanglement enables instant correlation"
    ]
    
    print("Analyzing research findings for universal patterns...")
    print("-" * 50)
    
    analyzer = MultiLanguageAnalyzer(target_languages=["en", "es", "zh", "ar"])
    
    for finding in findings:
        print(f"\nFinding: '{finding}'")
        analysis = await analyzer.analyze(finding)
        
        # Find the core pattern that survives translation
        core_patterns = {}
        for lang, patterns in analysis.patterns.items():
            for p in patterns:
                if hasattr(p, 'action'):
                    core_patterns[p.action] = core_patterns.get(p.action, 0) + 1
        
        if core_patterns:
            most_universal = max(core_patterns.items(), key=lambda x: x[1])
            print(f"  Universal pattern: {most_universal[0]}")
            print(f"  Preserved in {most_universal[1]}/{len(analysis.patterns)} languages")
        
        # Show how different languages emphasize different aspects
        print("  Language-specific emphasis:")
        for lang in ["es", "zh", "ar"]:
            if lang in analysis.patterns and analysis.patterns[lang]:
                print(f"    {lang}: {len(analysis.patterns[lang])} unique patterns")


async def main():
    """Run all demos."""
    print("\n" + "="*70)
    print("KIMERA MULTI-LANGUAGE ANALYSIS DEMONSTRATION")
    print("="*70)
    print("\nThis demo shows how Kimera can find deep patterns that transcend")
    print("linguistic boundaries, revealing universal structures in knowledge.")
    
    # Note about translation service
    print("\n⚠️  Note: Using mock translations by default.")
    print("   For real results, configure Google Translate or Hugging Face.")
    
    # Run demos
    await demo_basic_translation()
    await demo_linguistic_invariants()
    await demo_cross_domain_multilingual()
    await demo_translation_quality()
    await demo_practical_application()
    
    print("\n" + "="*70)
    print("CONCLUSION")
    print("="*70)
    print("\nMulti-language analysis reveals:")
    print("1. Patterns that transcend linguistic boundaries")
    print("2. Universal structures in human knowledge")
    print("3. How different languages emphasize different aspects")
    print("4. Deep connections between seemingly unrelated domains")
    print("\nThis forms the foundation for true cross-cultural and")
    print("cross-domain knowledge synthesis in the Spherical Word Methodology.")


if __name__ == "__main__":
    asyncio.run(main())
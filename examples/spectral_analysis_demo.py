"""
Spectral Analysis Demonstration
==============================

This demo showcases the spectral analysis capabilities of Kimera SWM,
implementing the mathematical foundations from Section 2.2.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
import matplotlib.pyplot as plt
from kimera.geoid import init_geoid
from kimera.mathematics.spectral import (
    resonance_spectrum,
    compute_spectral_gap,
    spectral_coherence_score
)


def demo_semantic_clusters():
    """Demonstrate spectral analysis on semantic clusters"""
    print("=== Spectral Analysis of Semantic Clusters ===\n")
    
    # Create three distinct semantic clusters
    clusters = {
        "Physics": [
            "Quantum mechanics describes the behavior of particles at atomic scales",
            "Einstein's theory of relativity revolutionized our understanding of space and time",
            "The standard model explains fundamental particles and their interactions",
            "Black holes are regions where gravity is so strong that nothing can escape"
        ],
        "Biology": [
            "DNA contains the genetic instructions for all living organisms",
            "Evolution by natural selection explains the diversity of life",
            "Cells are the basic units of life",
            "Photosynthesis converts light energy into chemical energy"
        ],
        "Literature": [
            "Shakespeare's plays explore universal themes of human nature",
            "Poetry uses language to evoke emotions and create imagery",
            "The novel emerged as a literary form in the 18th century",
            "Metaphors create connections between disparate concepts"
        ]
    }
    
    # Analyze each cluster
    for cluster_name, texts in clusters.items():
        print(f"\n{cluster_name} Cluster:")
        print("-" * 40)
        
        geoids = [init_geoid(text) for text in texts]
        R, eigenvalues, eigenvectors = resonance_spectrum(geoids)
        
        gap = compute_spectral_gap(eigenvalues)
        coherence = spectral_coherence_score(eigenvalues)
        
        print(f"Eigenvalues: {np.round(eigenvalues, 3)}")
        print(f"Spectral gap (Δ): {gap:.4f}")
        print(f"Coherence score: {coherence:.4f}")
        
        # Interpret results
        if coherence > 0.3:
            print("→ High semantic coherence")
        elif coherence > 0.1:
            print("→ Moderate semantic coherence")
        else:
            print("→ Low semantic coherence")
    
    # Mixed cluster analysis
    print("\n\nMixed Cluster (Physics + Biology + Literature):")
    print("-" * 40)
    
    mixed_texts = []
    for texts in clusters.values():
        mixed_texts.extend(texts[:2])  # Take 2 from each cluster
    
    mixed_geoids = [init_geoid(text) for text in mixed_texts]
    R_mixed, ev_mixed, _ = resonance_spectrum(mixed_geoids)
    
    gap_mixed = compute_spectral_gap(ev_mixed)
    coherence_mixed = spectral_coherence_score(ev_mixed)
    
    print(f"Eigenvalues: {np.round(ev_mixed, 3)}")
    print(f"Spectral gap (Δ): {gap_mixed:.4f}")
    print(f"Coherence score: {coherence_mixed:.4f}")
    print("→ Lower coherence due to semantic diversity")


def demo_phase_transition():
    """Demonstrate semantic phase transition detection"""
    print("\n\n=== Semantic Phase Transition Detection ===\n")
    
    # Create a gradual transition from one domain to another
    transition_texts = [
        # Pure physics
        "Quantum mechanics governs atomic behavior",
        "Particles exhibit wave-particle duality",
        "Energy is quantized at small scales",
        # Transition zone
        "Quantum biology studies quantum effects in living systems",
        "Biological processes may use quantum coherence",
        # Pure biology
        "Cells divide through mitosis",
        "DNA replication is essential for life",
        "Proteins fold into specific structures"
    ]
    
    # Analyze windows of texts
    window_size = 4
    gaps = []
    coherences = []
    
    for i in range(len(transition_texts) - window_size + 1):
        window = transition_texts[i:i + window_size]
        geoids = [init_geoid(text) for text in window]
        _, eigenvalues, _ = resonance_spectrum(geoids)
        
        gap = compute_spectral_gap(eigenvalues)
        coherence = spectral_coherence_score(eigenvalues)
        
        gaps.append(gap)
        coherences.append(coherence)
    
    print("Window Analysis (sliding window of 4 texts):")
    print("-" * 40)
    for i, (gap, coherence) in enumerate(zip(gaps, coherences)):
        print(f"Window {i+1}: Δ = {gap:.4f}, Coherence = {coherence:.4f}")
    
    # Identify phase transition
    min_coherence_idx = np.argmin(coherences)
    print(f"\n��� Phase transition detected at window {min_coherence_idx + 1}")
    print("  (Lowest coherence indicates semantic boundary)")


def demo_cross_domain_resonance():
    """Demonstrate cross-domain resonance detection"""
    print("\n\n=== Cross-Domain Resonance Analysis ===\n")
    
    # Pairs with potential cross-domain resonance
    pairs = [
        ("The brain processes information like a computer",
         "Neural networks in AI mimic biological neurons"),
        
        ("Evolution optimizes organisms through natural selection",
         "Genetic algorithms solve optimization problems"),
        
        ("Waves propagate through water",
         "Ideas spread through social networks"),
        
        ("The heart pumps blood through the body",
         "The CPU is the heart of the computer")
    ]
    
    print("Analyzing cross-domain conceptual pairs:")
    print("-" * 40)
    
    for i, (text1, text2) in enumerate(pairs):
        geoids = [init_geoid(text1), init_geoid(text2)]
        R, eigenvalues, _ = resonance_spectrum(geoids)
        
        # For 2 geoids, resonance is simply R[0,1]
        resonance_score = R[0, 1]
        
        print(f"\nPair {i+1}:")
        print(f"  Text 1: {text1[:50]}...")
        print(f"  Text 2: {text2[:50]}...")
        print(f"  Resonance: {resonance_score:.4f}")
        
        if resonance_score > 0.3:
            print("  → Strong cross-domain resonance")
        elif resonance_score > 0.1:
            print("  → Moderate cross-domain resonance")
        else:
            print("  → Weak cross-domain resonance")


def demo_eigenvalue_interpretation():
    """Demonstrate eigenvalue interpretation"""
    print("\n\n=== Eigenvalue Interpretation ===\n")
    
    # Create a hierarchical semantic structure
    texts = [
        # Core concept
        "Machine learning enables computers to learn from data",
        # Related concepts
        "Supervised learning uses labeled training data",
        "Unsupervised learning finds patterns without labels",
        "Reinforcement learning optimizes through trial and error",
        # Specific techniques
        "Neural networks are inspired by biological brains",
        "Decision trees split data based on features",
        "Support vector machines find optimal boundaries"
    ]
    
    geoids = [init_geoid(text) for text in texts]
    R, eigenvalues, eigenvectors = resonance_spectrum(geoids)
    
    print("Eigenvalue Analysis:")
    print("-" * 40)
    
    # Analyze eigenvalue distribution
    total_variance = np.sum(eigenvalues)
    explained_variance = np.cumsum(eigenvalues) / total_variance
    
    for i, (ev, var) in enumerate(zip(eigenvalues, explained_variance)):
        print(f"λ_{i+1} = {ev:.4f} ({var*100:.1f}% cumulative variance)")
    
    # Identify semantic dimensions
    print("\nSemantic Structure Interpretation:")
    n_significant = np.sum(eigenvalues > 0.1)
    print(f"→ {n_significant} significant semantic dimensions detected")
    
    if eigenvalues[0] / total_variance > 0.5:
        print("→ Strong central theme unifies the concepts")
    
    if compute_spectral_gap(eigenvalues) > 0.5:
        print("→ Clear primary semantic axis")
    else:
        print("→ Multiple competing semantic axes")


def main():
    """Run all demonstrations"""
    print("Kimera SWM Spectral Analysis Demonstration")
    print("=" * 50)
    
    demo_semantic_clusters()
    demo_phase_transition()
    demo_cross_domain_resonance()
    demo_eigenvalue_interpretation()
    
    print("\n\nConclusion:")
    print("-" * 40)
    print("Spectral analysis reveals deep semantic structure through:")
    print("• Eigenvalue decomposition of resonance matrices")
    print("• Spectral gap as a coherence indicator")
    print("• Phase transition detection at semantic boundaries")
    print("• Cross-domain resonance identification")
    print("\nThese tools enable Kimera to understand and navigate")
    print("the topology of meaning in high-dimensional semantic space.")


if __name__ == "__main__":
    main()
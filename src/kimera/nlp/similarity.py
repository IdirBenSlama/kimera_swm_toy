"""
Semantic similarity and embedding-based pattern extraction using spaCy.
"""

import spacy
import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from sklearn.metrics.pairwise import cosine_similarity


class SemanticPatternExtractor:
    """Extract patterns based on semantic similarity using spaCy embeddings."""
    
    def __init__(self, model_name: str = "en_core_web_md"):
        """
        Initialize with a spaCy model that includes word vectors.
        Note: Requires a medium or large model (e.g., en_core_web_md or en_core_web_lg).
        """
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            raise RuntimeError(
                f"spaCy model '{model_name}' is not installed. "
                f"Install it with: python -m spacy download {model_name}"
            )
        
        # Check if model has vectors
        if not self.nlp.vocab.vectors_length:
            raise ValueError(
                f"Model '{model_name}' doesn't include word vectors. "
                "Use 'en_core_web_md' or 'en_core_web_lg' for similarity features."
            )
    
    def find_similar_phrases(self, text: str, target_phrase: str, 
                           threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Find phrases in text that are semantically similar to target phrase."""
        doc = self.nlp(text)
        target_doc = self.nlp(target_phrase)
        
        similar_phrases = []
        
        # Check noun chunks
        for chunk in doc.noun_chunks:
            similarity = chunk.similarity(target_doc)
            if similarity >= threshold:
                similar_phrases.append({
                    "text": chunk.text,
                    "similarity": float(similarity),
                    "type": "noun_chunk",
                    "start": chunk.start,
                    "end": chunk.end
                })
        
        # Check sentences
        for sent in doc.sents:
            similarity = sent.similarity(target_doc)
            if similarity >= threshold:
                similar_phrases.append({
                    "text": sent.text.strip(),
                    "similarity": float(similarity),
                    "type": "sentence",
                    "start": sent.start,
                    "end": sent.end
                })
        
        return sorted(similar_phrases, key=lambda x: x["similarity"], reverse=True)
    
    def extract_semantic_clusters(self, text: str, 
                                n_clusters: Optional[int] = None,
                                min_similarity: float = 0.5) -> List[Dict[str, Any]]:
        """Group semantically similar phrases into clusters."""
        doc = self.nlp(text)
        
        # Extract all noun chunks and their vectors
        chunks = []
        vectors = []
        
        for chunk in doc.noun_chunks:
            if chunk.vector_norm > 0:  # Has valid vector
                chunks.append(chunk)
                vectors.append(chunk.vector)
        
        if not vectors:
            return []
        
        # Calculate pairwise similarities
        vectors_array = np.array(vectors)
        similarities = cosine_similarity(vectors_array)
        
        # Simple clustering based on similarity threshold
        clusters = []
        assigned = set()
        
        for i in range(len(chunks)):
            if i in assigned:
                continue
            
            cluster = {
                "center": chunks[i].text,
                "members": [chunks[i].text],
                "indices": [i]
            }
            assigned.add(i)
            
            for j in range(i + 1, len(chunks)):
                if j not in assigned and similarities[i][j] >= min_similarity:
                    cluster["members"].append(chunks[j].text)
                    cluster["indices"].append(j)
                    assigned.add(j)
            
            if len(cluster["members"]) > 1:
                clusters.append(cluster)
        
        return clusters
    
    def find_analogies(self, text: str, 
                      pattern: Tuple[str, str, str]) -> List[Dict[str, Any]]:
        """
        Find analogical patterns in text.
        Pattern format: (A, B, C) -> find X where A:B :: C:X
        """
        doc = self.nlp(text)
        a, b, c = pattern
        
        # Get vectors
        vec_a = self.nlp(a).vector
        vec_b = self.nlp(b).vector
        vec_c = self.nlp(c).vector
        
        # Calculate the relation vector (B - A)
        relation = vec_b - vec_a
        
        # Expected vector for X would be C + relation
        expected_vec = vec_c + relation
        
        # Find tokens/phrases closest to expected vector
        candidates = []
        
        # Check tokens
        for token in doc:
            if token.vector_norm > 0:
                similarity = cosine_similarity(
                    expected_vec.reshape(1, -1),
                    token.vector.reshape(1, -1)
                )[0][0]
                
                if similarity > 0.6:  # Threshold
                    candidates.append({
                        "text": token.text,
                        "similarity": float(similarity),
                        "type": "token",
                        "analogy": f"{a}:{b} :: {c}:{token.text}"
                    })
        
        # Check noun chunks
        for chunk in doc.noun_chunks:
            if chunk.vector_norm > 0:
                similarity = cosine_similarity(
                    expected_vec.reshape(1, -1),
                    chunk.vector.reshape(1, -1)
                )[0][0]
                
                if similarity > 0.6:
                    candidates.append({
                        "text": chunk.text,
                        "similarity": float(similarity),
                        "type": "noun_chunk",
                        "analogy": f"{a}:{b} :: {c}:{chunk.text}"
                    })
        
        return sorted(candidates, key=lambda x: x["similarity"], reverse=True)
    
    def extract_concept_patterns(self, text: str, 
                               concept_seeds: List[str]) -> Dict[str, List[str]]:
        """
        Extract words/phrases related to given concept seeds.
        Uses word embeddings to find semantically related terms.
        """
        doc = self.nlp(text)
        concept_patterns = {}
        
        for concept in concept_seeds:
            concept_vec = self.nlp(concept).vector
            related_terms = []
            
            # Find related tokens
            for token in doc:
                if token.vector_norm > 0:
                    similarity = cosine_similarity(
                        concept_vec.reshape(1, -1),
                        token.vector.reshape(1, -1)
                    )[0][0]
                    
                    if similarity > 0.6:
                        related_terms.append({
                            "text": token.text,
                            "similarity": float(similarity),
                            "pos": token.pos_
                        })
            
            # Sort by similarity and deduplicate
            related_terms = sorted(related_terms, 
                                 key=lambda x: x["similarity"], 
                                 reverse=True)
            
            # Remove duplicates while preserving order
            seen = set()
            unique_terms = []
            for term in related_terms:
                if term["text"].lower() not in seen:
                    seen.add(term["text"].lower())
                    unique_terms.append(term)
            
            concept_patterns[concept] = unique_terms[:10]  # Top 10
        
        return concept_patterns
    
    def extract_all_semantic_patterns(self, text: str) -> Dict[str, Any]:
        """Extract all semantic patterns from text."""
        # Default concept seeds
        concepts = ["technology", "emotion", "action", "location"]
        
        return {
            "semantic_clusters": self.extract_semantic_clusters(text),
            "concept_patterns": self.extract_concept_patterns(text, concepts)
        }
"""
Advanced pattern extraction using spaCy's Matcher and dependency parsing.
"""

import spacy
from spacy.matcher import Matcher, DependencyMatcher
from typing import List, Dict, Any, Optional, Tuple
import json


class PatternExtractor:
    """Advanced pattern extraction using spaCy's matching capabilities."""
    
    def __init__(self, model_name: str = "en_core_web_sm"):
        """Initialize the pattern extractor with a spaCy model."""
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            raise RuntimeError(
                f"spaCy model '{model_name}' is not installed. "
                f"Install it with: python -m spacy download {model_name}"
            )
        
        self.matcher = Matcher(self.nlp.vocab)
        self.dep_matcher = DependencyMatcher(self.nlp.vocab)
        self._init_default_patterns()
    
    def _init_default_patterns(self):
        """Initialize default linguistic patterns."""
        # Token-based patterns
        self.add_token_pattern(
            "VERB_NOUN",
            [{"POS": "VERB"}, {"POS": "NOUN"}],
            "Verb followed by noun"
        )
        
        self.add_token_pattern(
            "ADJ_NOUN",
            [{"POS": "ADJ"}, {"POS": "NOUN"}],
            "Adjective modifying noun"
        )
        
        # Dependency patterns
        self.add_dependency_pattern(
            "SUBJ_VERB_OBJ",
            [
                {"RIGHT_ID": "verb", "RIGHT_ATTRS": {"POS": "VERB"}},
                {"LEFT_ID": "verb", "REL_OP": ">", "RIGHT_ID": "subject", 
                 "RIGHT_ATTRS": {"DEP": "nsubj"}},
                {"LEFT_ID": "verb", "REL_OP": ">", "RIGHT_ID": "object",
                 "RIGHT_ATTRS": {"DEP": {"IN": ["dobj", "obj"]}}}
            ],
            "Subject-Verb-Object pattern"
        )
    
    def add_token_pattern(self, name: str, pattern: List[Dict], description: str = ""):
        """Add a token-based pattern to the matcher."""
        self.matcher.add(name, [pattern])
        if not hasattr(self, 'pattern_descriptions'):
            self.pattern_descriptions = {}
        self.pattern_descriptions[name] = description
    
    def add_dependency_pattern(self, name: str, pattern: List[Dict], description: str = ""):
        """Add a dependency-based pattern to the matcher."""
        self.dep_matcher.add(name, [pattern])
        if not hasattr(self, 'pattern_descriptions'):
            self.pattern_descriptions = {}
        self.pattern_descriptions[name] = description
    
    def extract_token_patterns(self, text: str) -> List[Dict[str, Any]]:
        """Extract token-based patterns from text."""
        doc = self.nlp(text)
        matches = self.matcher(doc)
        
        results = []
        for match_id, start, end in matches:
            pattern_name = self.nlp.vocab.strings[match_id]
            span = doc[start:end]
            results.append({
                "pattern": pattern_name,
                "text": span.text,
                "start": start,
                "end": end,
                "description": self.pattern_descriptions.get(pattern_name, "")
            })
        
        return results
    
    def extract_dependency_patterns(self, text: str) -> List[Dict[str, Any]]:
        """Extract dependency-based patterns from text."""
        doc = self.nlp(text)
        matches = self.dep_matcher(doc)
        
        results = []
        for match_id, token_ids in matches:
            pattern_name = self.nlp.vocab.strings[match_id]
            tokens = [doc[i] for i in token_ids]
            
            results.append({
                "pattern": pattern_name,
                "tokens": [{"text": t.text, "pos": t.pos_, "dep": t.dep_} 
                          for t in tokens],
                "description": self.pattern_descriptions.get(pattern_name, "")
            })
        
        return results
    
    def extract_syntactic_patterns(self, text: str) -> Dict[str, Any]:
        """Extract various syntactic patterns from text."""
        doc = self.nlp(text)
        
        # Extract noun phrases
        noun_phrases = [chunk.text for chunk in doc.noun_chunks]
        
        # Extract verb phrases (simplified)
        verb_phrases = []
        for token in doc:
            if token.pos_ == "VERB":
                phrase_tokens = [token]
                # Add direct objects
                for child in token.children:
                    if child.dep_ in ["dobj", "obj", "attr"]:
                        phrase_tokens.append(child)
                if len(phrase_tokens) > 1:
                    verb_phrases.append(" ".join([t.text for t in phrase_tokens]))
        
        # Extract prepositional phrases
        prep_phrases = []
        for token in doc:
            if token.pos_ == "ADP":
                phrase = token.text
                for child in token.children:
                    if child.dep_ == "pobj":
                        phrase += " " + child.text
                prep_phrases.append(phrase)
        
        return {
            "noun_phrases": noun_phrases,
            "verb_phrases": verb_phrases,
            "prepositional_phrases": prep_phrases
        }
    
    def extract_semantic_roles(self, text: str) -> List[Dict[str, Any]]:
        """Extract semantic roles (simplified version)."""
        doc = self.nlp(text)
        roles = []
        
        for token in doc:
            if token.pos_ == "VERB":
                verb_info = {
                    "verb": token.text,
                    "lemma": token.lemma_,
                    "arguments": {}
                }
                
                for child in token.children:
                    if child.dep_ == "nsubj":
                        verb_info["arguments"]["subject"] = child.text
                    elif child.dep_ in ["dobj", "obj"]:
                        verb_info["arguments"]["object"] = child.text
                    elif child.dep_ == "iobj":
                        verb_info["arguments"]["indirect_object"] = child.text
                    elif child.dep_ == "prep":
                        prep_phrase = child.text
                        for grandchild in child.children:
                            if grandchild.dep_ == "pobj":
                                prep_phrase += " " + grandchild.text
                        verb_info["arguments"][f"prep_{child.text}"] = prep_phrase
                
                if verb_info["arguments"]:
                    roles.append(verb_info)
        
        return roles
    
    def extract_all_patterns(self, text: str) -> Dict[str, Any]:
        """Extract all available patterns from text."""
        return {
            "token_patterns": self.extract_token_patterns(text),
            "dependency_patterns": self.extract_dependency_patterns(text),
            "syntactic_patterns": self.extract_syntactic_patterns(text),
            "semantic_roles": self.extract_semantic_roles(text)
        }
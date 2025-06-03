"""
Visualization utilities for NLP patterns using spaCy's displacy and other tools.
"""

import spacy
from spacy import displacy
from typing import List, Dict, Any, Optional
import json
from pathlib import Path


class PatternVisualizer:
    """Visualize extracted NLP patterns using various methods."""
    
    def __init__(self, model_name: str = "en_core_web_sm"):
        """Initialize the visualizer with a spaCy model."""
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            raise RuntimeError(
                f"spaCy model '{model_name}' is not installed. "
                f"Install it with: python -m spacy download {model_name}"
            )
    
    def visualize_dependencies(self, text: str, 
                             output_path: Optional[str] = None,
                             style: str = "dep") -> str:
        """
        Visualize dependency parse tree.
        Returns HTML string and optionally saves to file.
        """
        doc = self.nlp(text)
        
        options = {
            "compact": True,
            "distance": 100,
            "arrow_stroke": 2,
            "arrow_width": 8
        }
        
        html = displacy.render(doc, style=style, options=options)
        
        if output_path:
            Path(output_path).write_text(html, encoding="utf-8")
        
        return html
    
    def visualize_entities(self, text: str,
                         output_path: Optional[str] = None) -> str:
        """
        Visualize named entities in text.
        Returns HTML string and optionally saves to file.
        """
        doc = self.nlp(text)
        
        options = {
            "ents": None,  # Show all entity types
            "colors": {
                "PERSON": "#ff9999",
                "ORG": "#99ccff",
                "GPE": "#99ff99",
                "DATE": "#ffcc99",
                "MONEY": "#ff99ff"
            }
        }
        
        html = displacy.render(doc, style="ent", options=options)
        
        if output_path:
            Path(output_path).write_text(html, encoding="utf-8")
        
        return html
    
    def generate_pattern_report(self, text: str, patterns: Dict[str, Any],
                              output_path: Optional[str] = None) -> str:
        """
        Generate a comprehensive HTML report of extracted patterns.
        """
        doc = self.nlp(text)
        
        html_parts = [
            """
            <!DOCTYPE html>
            <html>
            <head>
                <title>NLP Pattern Analysis Report</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; }
                    .pattern { background: #f5f5f5; padding: 5px; margin: 5px 0; }
                    h1 { color: #333; }
                    h2 { color: #666; }
                    .highlight { background-color: #ffeb3b; }
                    table { border-collapse: collapse; width: 100%; }
                    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                    th { background-color: #4CAF50; color: white; }
                </style>
            </head>
            <body>
            """
        ]
        
        # Title and original text
        html_parts.append(f"<h1>NLP Pattern Analysis Report</h1>")
        html_parts.append(f"<div class='section'><h2>Original Text</h2><p>{text}</p></div>")
        
        # Token patterns
        if "token_patterns" in patterns:
            html_parts.append("<div class='section'><h2>Token Patterns</h2>")
            html_parts.append("<table><tr><th>Pattern</th><th>Text</th><th>Description</th></tr>")
            for p in patterns["token_patterns"]:
                html_parts.append(
                    f"<tr><td>{p['pattern']}</td><td>{p['text']}</td>"
                    f"<td>{p.get('description', '')}</td></tr>"
                )
            html_parts.append("</table></div>")
        
        # Dependency patterns
        if "dependency_patterns" in patterns:
            html_parts.append("<div class='section'><h2>Dependency Patterns</h2>")
            for p in patterns["dependency_patterns"]:
                tokens_str = ", ".join([f"{t['text']} ({t['pos']})" 
                                      for t in p["tokens"]])
                html_parts.append(
                    f"<div class='pattern'><strong>{p['pattern']}</strong>: "
                    f"{tokens_str} - {p.get('description', '')}</div>"
                )
            html_parts.append("</div>")
        
        # Syntactic patterns
        if "syntactic_patterns" in patterns:
            html_parts.append("<div class='section'><h2>Syntactic Patterns</h2>")
            syn = patterns["syntactic_patterns"]
            
            if syn.get("noun_phrases"):
                html_parts.append("<h3>Noun Phrases</h3><ul>")
                for np in syn["noun_phrases"]:
                    html_parts.append(f"<li>{np}</li>")
                html_parts.append("</ul>")
            
            if syn.get("verb_phrases"):
                html_parts.append("<h3>Verb Phrases</h3><ul>")
                for vp in syn["verb_phrases"]:
                    html_parts.append(f"<li>{vp}</li>")
                html_parts.append("</ul>")
            
            html_parts.append("</div>")
        
        # Semantic roles
        if "semantic_roles" in patterns:
            html_parts.append("<div class='section'><h2>Semantic Roles</h2>")
            html_parts.append("<table><tr><th>Verb</th><th>Arguments</th></tr>")
            for role in patterns["semantic_roles"]:
                args_str = json.dumps(role["arguments"], indent=2)
                html_parts.append(
                    f"<tr><td>{role['verb']}</td><td><pre>{args_str}</pre></td></tr>"
                )
            html_parts.append("</table></div>")
        
        # Dependency visualization
        html_parts.append("<div class='section'><h2>Dependency Visualization</h2>")
        dep_html = displacy.render(doc, style="dep", options={"compact": True})
        html_parts.append(dep_html)
        html_parts.append("</div>")
        
        # Entity visualization
        html_parts.append("<div class='section'><h2>Named Entities</h2>")
        ent_html = displacy.render(doc, style="ent")
        html_parts.append(ent_html)
        html_parts.append("</div>")
        
        html_parts.append("</body></html>")
        
        full_html = "\n".join(html_parts)
        
        if output_path:
            Path(output_path).write_text(full_html, encoding="utf-8")
        
        return full_html
    
    def export_patterns_json(self, patterns: Dict[str, Any], 
                           output_path: str) -> None:
        """Export extracted patterns to JSON format."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(patterns, f, indent=2, ensure_ascii=False)
    
    def generate_pattern_statistics(self, patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Generate statistics about extracted patterns."""
        stats = {
            "total_patterns": 0,
            "pattern_types": {}
        }
        
        for pattern_type, pattern_list in patterns.items():
            if isinstance(pattern_list, list):
                count = len(pattern_list)
                stats["total_patterns"] += count
                stats["pattern_types"][pattern_type] = count
        
        return stats
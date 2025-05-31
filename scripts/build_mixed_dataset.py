#!/usr/bin/env python3
"""
Mixed dataset builder for Kimera-SWM: generates both contradictory and non-contradictory pairs.

Usage:
    poetry run python scripts/build_mixed_dataset.py --rows 5000 --out data/mixed_5k.csv
    poetry run python scripts/build_mixed_dataset.py --rows 1000 --ratio 0.3 --out data/mixed_1k_30pct.csv
"""

import argparse
import csv
import json
import random
import re
import time
from pathlib import Path
from typing import List, Dict, Tuple
try:
    import requests
except ImportError:
    print("Warning: requests not available, using offline mode")
    requests = None


class MixedDatasetBuilder:
    def __init__(self, languages: List[str] = None, contradiction_ratio: float = 0.5):
        self.languages = languages or ["en", "fr", "ar"]
        self.contradiction_ratio = contradiction_ratio
        
        # Templates for generating contradictions
        self.contradiction_templates = {
            "en": [
                ("{statement}", "{statement} is false"),
                ("{statement}", "{statement} is incorrect"),
                ("{statement}", "The opposite of {statement} is true"),
                ("The {noun} is {adj}", "The {noun} is not {adj}"),
                ("{subject} can {verb}", "{subject} cannot {verb}"),
                ("Water boils at 100°C", "Water boils at 50°C"),
                ("The Earth is round", "The Earth is flat"),
                ("Birds can fly", "Birds cannot fly"),
            ],
            "fr": [
                ("{statement}", "{statement} est faux"),
                ("{statement}", "{statement} est incorrect"),
                ("Le {noun} est {adj}", "Le {noun} n'est pas {adj}"),
                ("L'eau bout à 100°C", "L'eau bout à 50°C"),
                ("La Terre est ronde", "La Terre est plate"),
            ],
            "ar": [
                ("{statement}", "{statement} خطأ"),
                ("{statement}", "{statement} غير صحيح"),
                ("الأرض كروية", "الأرض مسطحة"),
                ("الطيور تطير", "الطيور لا تطير"),
            ]
        }
        
        # Templates for generating non-contradictory pairs (neutral/unrelated)
        self.neutral_templates = {
            "en": [
                ("The sky is blue", "Cats are mammals"),
                ("Paris is in France", "Mathematics is useful"),
                ("Water is wet", "Books contain knowledge"),
                ("The sun is hot", "Music is enjoyable"),
                ("Trees have leaves", "Computers process data"),
                ("Fish live in water", "Cars have wheels"),
                ("Snow is cold", "Phones can make calls"),
                ("Flowers bloom in spring", "People need sleep"),
            ],
            "fr": [
                ("Le ciel est bleu", "Les chats sont des mammifères"),
                ("Paris est en France", "Les mathématiques sont utiles"),
                ("L'eau est mouillée", "Les livres contiennent des connaissances"),
                ("Le soleil est chaud", "La musique est agréable"),
                ("Les arbres ont des feuilles", "Les ordinateurs traitent des données"),
            ],
            "ar": [
                ("السماء زرقاء", "القطط من الثدييات"),
                ("باريس في فرنسا", "الرياضيات مفيدة"),
                ("الماء مبلل", "الكتب تحتوي على المعرفة"),
                ("الشمس حارة", "الموسيقى ممتعة"),
            ]
        }
        
        # Wikipedia API endpoints
        self.wiki_apis = {
            "en": "https://en.wikipedia.org/api/rest_v1/page/random/summary",
            "fr": "https://fr.wikipedia.org/api/rest_v1/page/random/summary", 
            "ar": "https://ar.wikipedia.org/api/rest_v1/page/random/summary"
        }

    def fetch_wikipedia_summary(self, lang: str) -> str:
        """Fetch a random Wikipedia article summary."""
        if not requests:
            return None
            
        try:
            response = requests.get(self.wiki_apis[lang], timeout=10)
            if response.status_code == 200:
                data = response.json()
                extract = data.get('extract', '').strip()
                # Clean up the extract - take first sentence
                sentences = re.split(r'[.!?]+', extract)
                if sentences and len(sentences[0]) > 20:
                    return sentences[0].strip() + "."
            return None
        except Exception as e:
            print(f"Error fetching Wikipedia summary for {lang}: {e}")
            return None

    def generate_contradiction_pair(self, lang: str) -> Tuple[str, str]:
        """Generate a contradictory pair."""
        templates = self.contradiction_templates.get(lang, self.contradiction_templates["en"])
        
        # Try to get a Wikipedia-based statement first
        wiki_statement = self.fetch_wikipedia_summary(lang)
        if wiki_statement and len(wiki_statement) > 20:
            # Generate contradiction from Wikipedia content
            contradiction = f"{wiki_statement.rstrip('.')} is false."
            return wiki_statement, contradiction
        
        # Fallback to template-based generation
        template = random.choice(templates)
        if isinstance(template, tuple) and len(template) == 2:
            return template
        
        # Handle parameterized templates
        try:
            original = template[0].format(statement="The Earth is round")
            contradiction = template[1].format(statement="The Earth is round")
            return original, contradiction
        except (KeyError, IndexError):
            return "Water is wet.", "Water is dry."

    def generate_neutral_pair(self, lang: str) -> Tuple[str, str]:
        """Generate a non-contradictory (neutral/unrelated) pair."""
        templates = self.neutral_templates.get(lang, self.neutral_templates["en"])
        
        # Try to get two different Wikipedia statements
        wiki1 = self.fetch_wikipedia_summary(lang)
        wiki2 = self.fetch_wikipedia_summary(lang)
        
        if wiki1 and wiki2 and len(wiki1) > 20 and len(wiki2) > 20:
            return wiki1, wiki2
        
        # Fallback to template-based generation
        return random.choice(templates)

    def build_mixed_dataset(self, target_pairs: int) -> List[Dict]:
        """Build a mixed dataset with contradictory and non-contradictory pairs."""
        dataset = []
        contradiction_pairs = int(target_pairs * self.contradiction_ratio)
        neutral_pairs = target_pairs - contradiction_pairs
        
        print(f"Building mixed dataset: {target_pairs} pairs total")
        print(f"  - {contradiction_pairs} contradictory pairs ({self.contradiction_ratio:.1%})")
        print(f"  - {neutral_pairs} neutral pairs ({1-self.contradiction_ratio:.1%})")
        
        pairs_per_lang = target_pairs // len(self.languages)
        contradiction_per_lang = int(pairs_per_lang * self.contradiction_ratio)
        neutral_per_lang = pairs_per_lang - contradiction_per_lang
        
        pair_id = 0
        
        for lang in self.languages:
            print(f"Generating pairs for {lang}...")
            
            # Generate contradictory pairs
            for i in range(contradiction_per_lang):
                try:
                    text1, text2 = self.generate_contradiction_pair(lang)
                    dataset.append({
                        "pair_id": pair_id,
                        "text1": text1,
                        "text2": text2,
                        "label": True,  # True = contradictory
                        "lang": lang,
                        "type": "contradiction"
                    })
                    pair_id += 1
                    time.sleep(0.1)  # Rate limiting
                except Exception as e:
                    print(f"Error generating contradiction pair: {e}")
                    continue
            
            # Generate neutral pairs
            for i in range(neutral_per_lang):
                try:
                    text1, text2 = self.generate_neutral_pair(lang)
                    dataset.append({
                        "pair_id": pair_id,
                        "text1": text1,
                        "text2": text2,
                        "label": False,  # False = non-contradictory
                        "lang": lang,
                        "type": "neutral"
                    })
                    pair_id += 1
                    time.sleep(0.1)  # Rate limiting
                except Exception as e:
                    print(f"Error generating neutral pair: {e}")
                    continue
        
        # Shuffle the dataset to mix contradictory and neutral pairs
        random.shuffle(dataset)
        
        print(f"Generated {len(dataset)} pairs total")
        contradiction_count = sum(1 for row in dataset if row['label'])
        print(f"  - {contradiction_count} contradictory ({contradiction_count/len(dataset):.1%})")
        print(f"  - {len(dataset)-contradiction_count} neutral ({(len(dataset)-contradiction_count)/len(dataset):.1%})")
        
        return dataset

    def save_dataset(self, dataset: List[Dict], output_path: Path):
        """Save dataset to CSV file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            if dataset:
                writer = csv.DictWriter(f, fieldnames=dataset[0].keys())
                writer.writeheader()
                writer.writerows(dataset)
        
        print(f"Dataset saved to {output_path} ({len(dataset)} rows)")


def main():
    parser = argparse.ArgumentParser(description="Build mixed Kimera-SWM dataset")
    parser.add_argument("--rows", type=int, default=5000, 
                       help="Number of pairs to generate")
    parser.add_argument("--ratio", type=float, default=0.5,
                       help="Ratio of contradictory pairs (0.0-1.0)")
    parser.add_argument("--lang", default="en,fr,ar", 
                       help="Comma-separated language codes")
    parser.add_argument("--out", default="data/mixed_5k.csv", 
                       help="Output CSV path")
    parser.add_argument("--seed", type=int, default=42,
                       help="Random seed for reproducibility")
    
    args = parser.parse_args()
    
    # Set random seed for reproducibility
    random.seed(args.seed)
    
    languages = [lang.strip() for lang in args.lang.split(",")]
    builder = MixedDatasetBuilder(languages=languages, contradiction_ratio=args.ratio)
    
    print(f"Building mixed dataset:")
    print(f"  - {args.rows} pairs")
    print(f"  - {args.ratio:.1%} contradictory ratio")
    print(f"  - Languages: {languages}")
    print(f"  - Random seed: {args.seed}")
    
    dataset = builder.build_mixed_dataset(args.rows)
    builder.save_dataset(dataset, Path(args.out))
    
    print("Mixed dataset build complete!")


if __name__ == "__main__":
    main()
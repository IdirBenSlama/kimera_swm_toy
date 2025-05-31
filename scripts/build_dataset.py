#!/usr/bin/env python3
"""
Dataset builder for Kimera-SWM contradiction pairs.

Usage:
    poetry run python scripts/build_dataset.py --rows 2000 --lang en,fr,ar --mode online --out data/contradictions_2k.csv
    poetry run python scripts/build_dataset.py --mode offline --out data/contradictions_2k.csv
"""

import argparse
import csv
import json
import random
import re
import time
from pathlib import Path
from typing import List, Dict, Tuple
import requests
from urllib.parse import quote


class DatasetBuilder:
    def __init__(self, mode: str = "online", languages: List[str] = None):
        self.mode = mode
        self.languages = languages or ["en", "fr", "ar"]
        self.contradiction_templates = {
            "en": [
                ("{statement}", "{statement} is false"),
                ("{statement}", "{statement} is incorrect"),
                ("{statement}", "The opposite of {statement} is true"),
                ("The {noun} is {adj}", "The {noun} is not {adj}"),
                ("{subject} can {verb}", "{subject} cannot {verb}"),
                ("{location} is in {country}", "{location} is not in {country}"),
            ],
            "fr": [
                ("{statement}", "{statement} est faux"),
                ("{statement}", "{statement} est incorrect"),
                ("Le {noun} est {adj}", "Le {noun} n'est pas {adj}"),
                ("{subject} peut {verb}", "{subject} ne peut pas {verb}"),
            ],
            "ar": [
                ("{statement}", "{statement} خطأ"),
                ("{statement}", "{statement} غير صحيح"),
                ("ال{noun} {adj}", "ال{noun} ليس {adj}"),
            ]
        }
        
        # Wikipedia API endpoints by language
        self.wiki_apis = {
            "en": "https://en.wikipedia.org/api/rest_v1/page/random/summary",
            "fr": "https://fr.wikipedia.org/api/rest_v1/page/random/summary", 
            "ar": "https://ar.wikipedia.org/api/rest_v1/page/random/summary"
        }

    def load_static_seed(self) -> List[Dict]:
        """Load static contradiction pairs from seed file."""
        seed_path = Path(__file__).parent.parent / "static" / "contradictions_seed.json"
        try:
            with open(seed_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {seed_path} not found, generating minimal fallback data")
            return self._generate_fallback_data()

    def _generate_fallback_data(self) -> List[Dict]:
        """Generate minimal fallback data if static seed is missing."""
        fallback = []
        base_facts = {
            "en": [
                "The Earth is round", "Water boils at 100°C", "Paris is the capital of France",
                "The sun rises in the east", "Birds can fly", "Fire is hot"
            ],
            "fr": [
                "La Terre est ronde", "L'eau bout à 100°C", "Paris est la capitale de la France"
            ],
            "ar": [
                "الأرض كروية", "الماء يغلي عند 100 درجة مئوية", "باريس عاصمة فرنسا"
            ]
        }
        
        for lang, facts in base_facts.items():
            for i, fact in enumerate(facts):
                fallback.extend([
                    {"id": f"{lang}_{i}_true", "lang": lang, "text": fact, "label_contradict_id": f"{lang}_{i}_false"},
                    {"id": f"{lang}_{i}_false", "lang": lang, "text": f"{fact} is false", "label_contradict_id": f"{lang}_{i}_true"}
                ])
        
        return fallback

    def fetch_wikipedia_summary(self, lang: str) -> str:
        """Fetch a random Wikipedia article summary."""
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

    def generate_contradiction_pair(self, statement: str, lang: str) -> Tuple[str, str]:
        """Generate a contradiction pair from a base statement."""
        templates = self.contradiction_templates.get(lang, self.contradiction_templates["en"])
        template = random.choice(templates)
        
        try:
            # Simple template substitution
            original = template[0].format(statement=statement)
            contradiction = template[1].format(statement=statement)
            return original, contradiction
        except KeyError:
            # Fallback for complex templates
            return statement, f"{statement} is false"

    def build_online_dataset(self, target_rows: int) -> List[Dict]:
        """Build dataset by scraping Wikipedia."""
        dataset = []
        rows_per_lang = target_rows // len(self.languages)
        
        print(f"Building online dataset: {target_rows} rows ({rows_per_lang} per language)")
        
        for lang in self.languages:
            print(f"Generating {rows_per_lang} pairs for {lang}...")
            lang_pairs = 0
            attempts = 0
            max_attempts = rows_per_lang * 3  # Allow some failures
            
            while lang_pairs < rows_per_lang and attempts < max_attempts:
                attempts += 1
                
                # Fetch base statement
                base_statement = self.fetch_wikipedia_summary(lang)
                if not base_statement or len(base_statement) < 20:
                    continue
                
                # Generate contradiction pair
                original, contradiction = self.generate_contradiction_pair(base_statement, lang)
                
                # Add to dataset
                pair_id = f"{lang}_{lang_pairs}"
                dataset.extend([
                    {
                        "id": f"{pair_id}_orig",
                        "lang": lang,
                        "text": original,
                        "label_contradict_id": f"{pair_id}_contra"
                    },
                    {
                        "id": f"{pair_id}_contra", 
                        "lang": lang,
                        "text": contradiction,
                        "label_contradict_id": f"{pair_id}_orig"
                    }
                ])
                
                lang_pairs += 1
                
                # Rate limiting
                time.sleep(0.1)
        
        return dataset

    def build_dataset(self, target_rows: int) -> List[Dict]:
        """Build dataset using specified mode."""
        if self.mode == "offline":
            print("Using offline mode - loading static seed data")
            seed_data = self.load_static_seed()
            # Sample and expand if needed
            if len(seed_data) >= target_rows:
                return random.sample(seed_data, target_rows)
            else:
                # Duplicate and shuffle if we need more rows
                multiplier = (target_rows // len(seed_data)) + 1
                expanded = (seed_data * multiplier)[:target_rows]
                random.shuffle(expanded)
                return expanded
        else:
            return self.build_online_dataset(target_rows)

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
    parser = argparse.ArgumentParser(description="Build Kimera-SWM contradiction dataset")
    parser.add_argument("--rows", type=int, default=2000, help="Number of rows to generate")
    parser.add_argument("--lang", default="en,fr,ar", help="Comma-separated language codes")
    parser.add_argument("--mode", choices=["online", "offline"], default="online", 
                       help="Data source mode")
    parser.add_argument("--out", default="data/contradictions_2k.csv", 
                       help="Output CSV path")
    
    args = parser.parse_args()
    
    languages = [lang.strip() for lang in args.lang.split(",")]
    builder = DatasetBuilder(mode=args.mode, languages=languages)
    
    print(f"Building dataset: {args.rows} rows, languages: {languages}, mode: {args.mode}")
    
    dataset = builder.build_dataset(args.rows)
    builder.save_dataset(dataset, Path(args.out))
    
    print("Dataset build complete!")


if __name__ == "__main__":
    main()
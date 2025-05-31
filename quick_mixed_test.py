#!/usr/bin/env python3
"""
Mixed dataset builder for Kimera-SWM (balanced contradictions/non-contradictions).

Usage:
    poetry run python scripts/build_mixed_dataset.py --rows 5000 --mode online --out data/mixed_5k.csv
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

class MixedDatasetBuilder:
    def __init__(self, mode: str = "online", languages: List[str] = None):
        self.mode = mode
        self.languages = languages or ["en"]
        self.wiki_api = "https://en.wikipedia.org/api/rest_v1/page/random/summary"

    def fetch_wikipedia_statements(self, count: int) -> List[str]:
        """Fetch multiple random Wikipedia statements."""
        statements = []
        while len(statements) < count:
            try:
                response = requests.get(self.wiki_api, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    extract = data.get('extract', '').strip()
                    sentences = re.split(r'[.!?]+', extract)
                    if sentences and len(sentences[0]) > 20:
                        statements.append(sentences[0].strip() + ".")
                time.sleep(0.1)  # Rate limiting
            except Exception as e:
                print(f"Error fetching Wikipedia summary: {e}")
        return statements

    def generate_contradiction(self, statement: str) -> str:
        """Generate a contradiction for a statement."""
        templates = [
            "{} is false",
            "{} is incorrect",
            "The opposite of {} is true",
            "It is not true that {}"
        ]
        return random.choice(templates).format(statement.lower())

    def build_mixed_dataset(self, target_rows: int) -> List[Dict]:
        """Build dataset with equal contradictions/non-contradictions."""
        pairs_needed = target_rows // 2
        statements = self.fetch_wikipedia_statements(pairs_needed * 2)

        dataset = []

        # Generate contradiction pairs
        for i in range(pairs_needed):
            statement = statements[i]
            contradiction = self.generate_contradiction(statement)
            dataset.extend([
                {
                    "id": f"contra_{i}_orig",
                    "text1": statement,
                    "text2": contradiction,
                    "is_contradiction": True
                }
            ])

        # Generate non-contradiction pairs
        for i in range(pairs_needed):
            text1 = statements[i]
            text2 = statements[i + pairs_needed]
            dataset.extend([
                {
                    "id": f"non_contra_{i}",
                    "text1": text1,
                    "text2": text2,
                    "is_contradiction": False
                }
            ])

        random.shuffle(dataset)
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
    parser.add_argument("--rows", type=int, default=5000, help="Number of rows to generate")
    parser.add_argument("--mode", choices=["online"], default="online", help="Data source mode")
    parser.add_argument("--out", default="data/mixed_5k.csv", help="Output CSV path")

    args = parser.parse_args()
    builder = MixedDatasetBuilder(mode=args.mode)

    print(f"Building mixed dataset: {args.rows} rows ({args.rows//2} contradictions, {args.rows//2} non-contradictions)")
    dataset = builder.build_mixed_dataset(args.rows)
    builder.save_dataset(dataset, Path(args.out))
    print("Dataset build complete!")

if __name__ == "__main__":
    main()#!/usr/bin/env python3
"""
Quick test to generate a small mixed dataset without external dependencies
"""
import csv
import random
from pathlib import Path

def create_quick_mixed_dataset():
    """Create a small mixed dataset for testing."""
    
    # Contradictory pairs
    contradictions = [
        ("The Earth is round", "The Earth is flat"),
        ("Water boils at 100°C", "Water boils at 50°C"),
        ("Birds can fly", "Birds cannot fly"),
        ("The sun is hot", "The sun is cold"),
        ("Fire is hot", "Fire is cold"),
        ("Snow is white", "Snow is black"),
        ("Cats are mammals", "Cats are reptiles"),
        ("Paris is in France", "Paris is in Germany"),
        ("The sky is blue", "The sky is green"),
        ("Fish live in water", "Fish live on land"),
    ]
    
    # Non-contradictory (neutral) pairs
    neutrals = [
        ("The sky is blue", "Cats are mammals"),
        ("Paris is in France", "Mathematics is useful"),
        ("Water is wet", "Books contain knowledge"),
        ("The sun is hot", "Music is enjoyable"),
        ("Trees have leaves", "Computers process data"),
        ("Fish live in water", "Cars have wheels"),
        ("Snow is cold", "Phones can make calls"),
        ("Flowers bloom in spring", "People need sleep"),
        ("Dogs are loyal", "Pizza is delicious"),
        ("Mountains are tall", "Libraries are quiet"),
    ]
    
    dataset = []
    pair_id = 0
    
    # Add contradictory pairs
    for text1, text2 in contradictions:
        dataset.append({
            "pair_id": pair_id,
            "text1": text1,
            "text2": text2,
            "label": True,  # True = contradictory
            "lang": "en",
            "type": "contradiction"
        })
        pair_id += 1
    
    # Add neutral pairs
    for text1, text2 in neutrals:
        dataset.append({
            "pair_id": pair_id,
            "text1": text1,
            "text2": text2,
            "label": False,  # False = non-contradictory
            "lang": "en",
            "type": "neutral"
        })
        pair_id += 1
    
    # Shuffle the dataset
    random.shuffle(dataset)
    
    # Save to CSV
    output_path = Path("data/mixed_quick.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=dataset[0].keys())
        writer.writeheader()
        writer.writerows(dataset)
    
    print(f"Created quick mixed dataset: {len(dataset)} pairs")
    contradiction_count = sum(1 for row in dataset if row['label'])
    print(f"  - {contradiction_count} contradictory ({contradiction_count/len(dataset):.1%})")
    print(f"  - {len(dataset)-contradiction_count} neutral ({(len(dataset)-contradiction_count)/len(dataset):.1%})")
    print(f"Saved to: {output_path}")
    
    return output_path

if __name__ == "__main__":
    random.seed(42)  # For reproducibility
    dataset_path = create_quick_mixed_dataset()
    
    # Also run a quick benchmark test
    print("\n🔬 Running quick benchmark test...")
    import subprocess
    import sys
    
    try:
        cmd = [
            sys.executable, "-m", "benchmarks.llm_compare",
            str(dataset_path),
            "--max-pairs", "20",
            "--stats",
            "--outfile", "mixed_quick_results.csv"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Benchmark completed successfully")
            print("Check mixed_quick_results.csv and metrics.yaml for results!")
        else:
            print(f"❌ Benchmark failed: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error running benchmark: {e}")
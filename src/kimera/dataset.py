import csv
import os
from pathlib import Path
from .geoid import init_geoid

def load_toy_dataset(path: Path = None):
    """Load dataset from CSV file. Supports both old and new formats."""
    if path is None:
        # Default to toy dataset, but check for environment override
        dataset_path = os.getenv('KIMERA_DATASET_PATH')
        if dataset_path:
            path = Path(dataset_path)
        else:
            path = Path(__file__).parent.parent.parent / "data" / "toy_contradictions.csv"
    
    geoids = []
    with path.open(encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Support both old format (text, lang) and new format (id, lang, text, label_contradict_id)
            text = row.get("text", "")
            lang = row.get("lang", "en")
            
            if text and lang:
                geoids.append(init_geoid(text, lang, ["default"]))
    
    return geoids

def load_dataset(path: Path):
    """Load dataset from specified path."""
    return load_toy_dataset(path)
